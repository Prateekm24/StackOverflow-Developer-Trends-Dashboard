"""Callbacks for H3: The Flexibility Dividend Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import WORK_MODE_COLORS, PERIOD_COLORS
from h3.data_processing import (
    get_satisfaction_stats,
    calculate_satisfaction_change,
    prepare_comparison_data,
    calculate_all_mode_changes
)


def register_callbacks(app, df):
    """
    Register all callbacks for the H3 dashboard.
    
    Args:
        app: Dash application instance
        df: Processed DataFrame
    """
    
    @app.callback(
        [Output('highest-satisfaction-mode', 'children'),
         Output('biggest-gain', 'children'),
         Output('pre-covid-avg', 'children'),
         Output('post-covid-avg', 'children')],
        [Input('comparison-viz-type', 'value')]
    )
    def update_key_metrics(viz_type):
        """Update key metrics cards."""
        # Calculate post-COVID satisfaction for each mode
        post_satisfaction = {}
        for mode in ['remote', 'hybrid', 'on_site']:
            stats = get_satisfaction_stats(df, work_mode=mode, period='post')
            if stats['count'] > 0:
                post_satisfaction[mode] = stats['mean']
        
        # Find highest satisfaction mode
        if post_satisfaction:
            highest_mode = max(post_satisfaction, key=post_satisfaction.get)
            highest_mode_label = highest_mode.replace('_', ' ').title()
        else:
            highest_mode_label = "N/A"
        
        # Calculate gains for each mode
        changes = calculate_all_mode_changes(df)
        if len(changes) > 0:
            biggest_gain_row = changes.loc[changes['change'].idxmax()]
            biggest_gain_mode = biggest_gain_row['work_mode'].replace('_', ' ').title()
            biggest_gain = biggest_gain_row['change']
            biggest_gain_text = f"{biggest_gain_mode} (+{biggest_gain:.2f})"
        else:
            biggest_gain_text = "N/A"
        
        # Overall averages
        pre_stats = get_satisfaction_stats(df, period='pre')
        post_stats = get_satisfaction_stats(df, period='post')
        
        pre_avg = f"{pre_stats['mean']:.2f}" if pre_stats['count'] > 0 else "N/A"
        post_avg = f"{post_stats['mean']:.2f}" if post_stats['count'] > 0 else "N/A"
        
        return highest_mode_label, biggest_gain_text, pre_avg, post_avg
    
    @app.callback(
        Output('main-comparison-chart', 'figure'),
        [Input('comparison-viz-type', 'value')]
    )
    def update_main_comparison(viz_type):
        """Update main comparison chart based on visualization type."""
        comparison_df = prepare_comparison_data(df)
        
        if len(comparison_df) == 0:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for comparison",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        if viz_type == 'box':
            fig = px.box(comparison_df,
                        x='Work Mode',
                        y='job_satisfaction',
                        color='Period',
                        title='Job Satisfaction Distribution: Pre-COVID vs Post-COVID',
                        labels={'job_satisfaction': 'Job Satisfaction Score'},
                        color_discrete_map=PERIOD_COLORS,
                        category_orders={'Work Mode': ['Remote', 'Hybrid', 'On Site'],
                                       'Period': ['Pre-COVID', 'Post-COVID']})
        
        elif viz_type == 'violin':
            fig = px.violin(comparison_df,
                           x='Work Mode',
                           y='job_satisfaction',
                           color='Period',
                           title='Job Satisfaction Density: Pre-COVID vs Post-COVID',
                           labels={'job_satisfaction': 'Job Satisfaction Score'},
                           color_discrete_map=PERIOD_COLORS,
                           category_orders={'Work Mode': ['Remote', 'Hybrid', 'On Site'],
                                          'Period': ['Pre-COVID', 'Post-COVID']},
                           box=True)
        
        elif viz_type == 'bar':
            # Calculate means
            means = comparison_df.groupby(['Work Mode', 'Period'])['job_satisfaction'].mean().reset_index()
            
            fig = px.bar(means,
                        x='Work Mode',
                        y='job_satisfaction',
                        color='Period',
                        title='Average Job Satisfaction: Pre-COVID vs Post-COVID',
                        labels={'job_satisfaction': 'Average Satisfaction Score'},
                        color_discrete_map=PERIOD_COLORS,
                        category_orders={'Work Mode': ['Remote', 'Hybrid', 'On Site'],
                                       'Period': ['Pre-COVID', 'Post-COVID']},
                        barmode='group',
                        text='job_satisfaction')
            
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        
        else:  # line
            # Calculate means by year
            comparison_df['Year'] = comparison_df['year']
            yearly_means = comparison_df.groupby(['Year', 'Work Mode'])['job_satisfaction'].mean().reset_index()
            
            fig = px.line(yearly_means,
                         x='Year',
                         y='job_satisfaction',
                         color='Work Mode',
                         title='Job Satisfaction Trend Over Time',
                         labels={'job_satisfaction': 'Average Satisfaction Score'},
                         color_discrete_map={'Remote': WORK_MODE_COLORS['remote'],
                                           'Hybrid': WORK_MODE_COLORS['hybrid'],
                                           'On Site': WORK_MODE_COLORS['on_site']},
                         markers=True)
            
            # Add shading for excluded years
            fig.add_vrect(x0=2019.5, x1=2023.5, fillcolor="gray", opacity=0.1,
                         annotation_text="2020-2023 Excluded",
                         annotation_position="top")
        
        fig.update_layout(
            hovermode='x unified' if viz_type in ['line'] else 'closest',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @app.callback(
        Output('change-analysis-chart', 'figure'),
        [Input('comparison-viz-type', 'value')]
    )
    def update_change_analysis(viz_type):
        """Show satisfaction changes from pre to post COVID."""
        changes_df = calculate_all_mode_changes(df)
        
        if len(changes_df) == 0:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for change analysis",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        changes_df['Work Mode'] = changes_df['work_mode'].str.replace('_', ' ').str.title()
        changes_df['Color'] = changes_df['change'].apply(lambda x: '#27ae60' if x > 0 else '#e74c3c')
        
        fig = go.Figure(data=[go.Bar(
            x=changes_df['Work Mode'],
            y=changes_df['change'],
            marker_color=changes_df['Color'],
            text=changes_df['change'].round(2),
            texttemplate='%{text:+.2f}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Change: %{y:.2f}<extra></extra>'
        )])
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title='Satisfaction Change by Work Mode (Post-COVID minus Pre-COVID)',
            xaxis_title='Work Mode',
            yaxis_title='Change in Satisfaction Score',
            showlegend=False
        )
        
        return fig
    
    @app.callback(
        Output('rankings-chart', 'figure'),
        [Input('comparison-viz-type', 'value')]
    )
    def update_rankings(viz_type):
        """Show current satisfaction rankings."""
        post_covid = df[(df['year'] >= 2024) & (df['year'] <= 2025)].copy()
        
        rankings = []
        for mode in ['remote', 'hybrid', 'on_site']:
            stats = get_satisfaction_stats(post_covid, work_mode=mode)
            rankings.append({
                'Work Mode': mode.replace('_', ' ').title(),
                'Satisfaction': stats['mean'],
                'Count': stats['count']
            })
        
        ranking_df = pd.DataFrame(rankings).sort_values('Satisfaction', ascending=True)
        
        fig = px.bar(ranking_df,
                    y='Work Mode',
                    x='Satisfaction',
                    orientation='h',
                    title='Post-COVID Satisfaction Rankings',
                    labels={'Satisfaction': 'Average Satisfaction Score'},
                    text='Satisfaction',
                    color='Satisfaction',
                    color_continuous_scale='RdYlGn')
        
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        
        return fig
    
    @app.callback(
        Output('timeline-chart', 'figure'),
        [Input('comparison-viz-type', 'value')]
    )
    def update_timeline(viz_type):
        """Show satisfaction evolution over time."""
        # Filter for only Pre-COVID and Post-COVID
        df_timeline = df[((df['year'] >= 2017) & (df['year'] <= 2019)) | 
                        ((df['year'] >= 2024) & (df['year'] <= 2025))].copy()
        df_timeline['Work Mode'] = df_timeline['work_mode'].str.replace('_', ' ').str.title()
        
        yearly_means = df_timeline.groupby(['year', 'Work Mode'])['job_satisfaction'].mean().reset_index()
        
        fig = px.line(yearly_means,
                     x='year',
                     y='job_satisfaction',
                     color='Work Mode',
                     title='Job Satisfaction Evolution (Pre-COVID: 2017-2019 vs Post-COVID: 2024-2025)',
                     labels={'job_satisfaction': 'Average Satisfaction Score', 'year': 'Year'},
                     color_discrete_map={'Remote': WORK_MODE_COLORS['remote'],
                                        'Hybrid': WORK_MODE_COLORS['hybrid'],
                                        'On Site': WORK_MODE_COLORS['on_site']},
                     markers=True)
        
        # Add shading to indicate missing years
        fig.add_vrect(x0=2019.5, x1=2023.5, fillcolor="gray", opacity=0.1,
                      annotation_text="2020-2023 Excluded (No Data)", 
                      annotation_position="top",
                      annotation=dict(font_size=10))
        
        fig.update_layout(
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @app.callback(
        Output('filtered-analysis-chart', 'figure'),
        [Input('work-mode-selector', 'value'),
         Input('period-selector', 'value'),
         Input('compare-dimension', 'value')]
    )
    def update_filtered_analysis(work_mode, period, dimension):
        """Update filtered analysis based on user selections."""
        df_filtered = df.copy()
        
        # Apply work mode filter
        if work_mode != 'all':
            df_filtered = df_filtered[df_filtered['work_mode'] == work_mode]
        
        # Apply period filter
        if period == 'pre':
            df_filtered = df_filtered[(df_filtered['year'] >= 2017) & (df_filtered['year'] <= 2019)]
            title_period = " (Pre-COVID: 2017-2019)"
        elif period == 'post':
            df_filtered = df_filtered[(df_filtered['year'] >= 2024) & (df_filtered['year'] <= 2025)]
            title_period = " (Post-COVID: 2024-2025)"
        else:
            df_filtered = df_filtered[((df_filtered['year'] >= 2017) & (df_filtered['year'] <= 2019)) | 
                                     ((df_filtered['year'] >= 2024) & (df_filtered['year'] <= 2025))]
            title_period = " (Pre vs Post-COVID)"
        
        if len(df_filtered) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No data available for selected filters",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Create visualization based on comparison dimension
        if dimension == 'work_mode':
            df_filtered['Work Mode'] = df_filtered['work_mode'].str.replace('_', ' ').str.title()
            
            fig = px.box(df_filtered,
                        x='Work Mode',
                        y='job_satisfaction',
                        title=f'Satisfaction by Work Mode{title_period}',
                        labels={'job_satisfaction': 'Job Satisfaction Score'},
                        color='Work Mode',
                        color_discrete_map={'Remote': WORK_MODE_COLORS['remote'],
                                           'Hybrid': WORK_MODE_COLORS['hybrid'],
                                           'On Site': WORK_MODE_COLORS['on_site']},
                        category_orders={'Work Mode': ['Remote', 'Hybrid', 'On Site']})
            
        elif dimension == 'year':
            yearly_stats = df_filtered.groupby('year')['job_satisfaction'].agg(['mean', 'std', 'count']).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=yearly_stats['year'],
                y=yearly_stats['mean'],
                mode='lines+markers',
                name='Mean Satisfaction',
                line=dict(color='#3498db', width=3),
                marker=dict(size=8)
            ))
            
            # Add error bands
            fig.add_trace(go.Scatter(
                x=yearly_stats['year'].tolist() + yearly_stats['year'].tolist()[::-1],
                y=(yearly_stats['mean'] + yearly_stats['std']).tolist() + 
                  (yearly_stats['mean'] - yearly_stats['std']).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(52, 152, 219, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Standard Deviation',
                showlegend=True
            ))
            
            fig.update_layout(
                title=f'Satisfaction Over Time{title_period}',
                xaxis_title='Year',
                yaxis_title='Job Satisfaction Score',
                hovermode='x unified'
            )
            
        elif dimension == 'company_size':
            if 'company_size' in df_filtered.columns:
                df_filtered['Company Size'] = df_filtered['company_size'].astype(str)
                
                fig = px.box(df_filtered,
                            x='Company Size',
                            y='job_satisfaction',
                            title=f'Satisfaction by Company Size{title_period}',
                            labels={'job_satisfaction': 'Job Satisfaction Score'},
                            color='Company Size')
            else:
                fig = go.Figure()
                fig.add_annotation(text="Company size data not available",
                                 xref="paper", yref="paper",
                                 x=0.5, y=0.5, showarrow=False)
        
        return fig
