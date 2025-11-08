"""Callbacks for H1A: Global Shift in Work Mode Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import COVID_YEAR


def register_callbacks(app, df, color_map):
    """
    Register all callbacks for the H1A dashboard.
    
    Args:
        app: Dash application instance
        df: Processed DataFrame
        color_map: Dictionary mapping work modes to colors
    """
    
    @app.callback(
        [Output('pre-covid-remote', 'children'),
         Output('post-covid-remote', 'children'),
         Output('change-remote', 'children')],
        [Input('year-slider', 'value')]
    )
    def update_covid_stats(year_range):
        """Update pre/post COVID statistics cards."""
        # Pre-COVID (2017-2019)
        pre_covid = df[(df['year'] >= 2017) & (df['year'] <= 2019)]
        pre_remote = (pre_covid['work_mode'] == 'remote').sum()
        pre_total = len(pre_covid[pre_covid['work_mode'].notna()])
        pre_pct = (pre_remote / pre_total * 100) if pre_total > 0 else 0
        
        # Post-COVID (2021-2025)
        post_covid = df[(df['year'] >= 2021) & (df['year'] <= 2025)]
        post_remote = (post_covid['work_mode'] == 'remote').sum()
        post_total = len(post_covid[post_covid['work_mode'].notna()])
        post_pct = (post_remote / post_total * 100) if post_total > 0 else 0
        
        change = post_pct - pre_pct
        
        return (
            f"{pre_pct:.1f}%",
            f"{post_pct:.1f}%",
            f"+{change:.1f}pp" if change >= 0 else f"{change:.1f}pp"
        )
    
    @app.callback(
        Output('work-mode-chart', 'figure'),
        [Input('chart-type', 'value'),
         Input('year-slider', 'value'),
         Input('story-mode', 'value')]
    )
    def update_work_mode_chart(chart_type, year_range, story_mode):
        """Update the main work mode chart based on selections."""
        # Filter data
        filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].copy()
        
        # Calculate percentages by year and work mode
        tab = (filtered_df[['year', 'work_mode']]
               .dropna()
               .groupby(['year', 'work_mode'], as_index=False)
               .size())
        
        tab['percentage'] = tab['size'] / tab.groupby('year')['size'].transform('sum') * 100
        
        # Create appropriate chart
        if chart_type == 'line':
            fig = px.line(tab, x='year', y='percentage', color='work_mode',
                        title='Work Mode Distribution Over Time',
                        labels={'percentage': 'Percentage (%)', 'year': 'Year', 'work_mode': 'Work Mode'},
                        color_discrete_map=color_map,
                        markers=True,
                        hover_data={'percentage': ':.1f'})
        
        elif chart_type == 'area':
            fig = px.area(tab, x='year', y='percentage', color='work_mode',
                         title='Work Mode Distribution Over Time (Stacked Area)',
                         labels={'percentage': 'Percentage (%)', 'year': 'Year', 'work_mode': 'Work Mode'},
                         color_discrete_map=color_map,
                         hover_data={'percentage': ':.1f'})
        
        elif chart_type == 'bar':
            fig = px.bar(tab, x='year', y='percentage', color='work_mode',
                        title='Work Mode Distribution Over Time (Stacked Bar)',
                        labels={'percentage': 'Percentage (%)', 'year': 'Year', 'work_mode': 'Work Mode'},
                        color_discrete_map=color_map,
                        hover_data={'percentage': ':.1f'})
        
        else:  # grouped_bar
            fig = px.bar(tab, x='year', y='percentage', color='work_mode',
                        title='Work Mode Distribution Over Time (Grouped)',
                        labels={'percentage': 'Percentage (%)', 'year': 'Year', 'work_mode': 'Work Mode'},
                        color_discrete_map=color_map,
                        barmode='group',
                        hover_data={'percentage': ':.1f'})
        
        # Add COVID-19 pandemic marker if 2020 is in range
        if year_range[0] <= COVID_YEAR <= year_range[1]:
            fig.add_vline(x=COVID_YEAR, line_dash="dash", line_color="red", opacity=0.5,
                          annotation_text="COVID-19 Pandemic", 
                          annotation_position="top right",
                          annotation=dict(font_size=10, font_color="red"))
        
        # Add annotations for key insights (only in story mode)
        if 'story' in story_mode and chart_type in ['line', 'area']:
            remote_data = tab[tab['work_mode'] == 'remote'].sort_values('year')
            if len(remote_data) > 1:
                remote_data = remote_data.copy()
                remote_data['change'] = remote_data['percentage'].diff()
                
                if not remote_data['change'].isna().all():
                    max_change_idx = remote_data['change'].idxmax()
                    if pd.notna(max_change_idx):
                        max_change_year = remote_data.loc[max_change_idx, 'year']
                        max_change_val = remote_data.loc[max_change_idx, 'change']
                        max_change_pct = remote_data.loc[max_change_idx, 'percentage']
                        
                        fig.add_annotation(
                            x=max_change_year,
                            y=max_change_pct,
                            text=f"Biggest shift: +{max_change_val:.1f}pp",
                            showarrow=True,
                            arrowhead=2,
                            bgcolor="yellow",
                            opacity=0.8,
                            font=dict(size=10)
                        )
        
        fig.update_layout(
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title=dict(text="Work Mode")
            )
        )
        
        return fig
    
    @app.callback(
        Output('summary-stats', 'figure'),
        [Input('year-slider', 'value')]
    )
    def update_summary_stats(year_range):
        """Show summary statistics for the selected period with interactive click."""
        filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].copy()
        
        # Calculate overall percentages for the period
        mode_counts = filtered_df['work_mode'].value_counts()
        mode_percentages = (mode_counts / mode_counts.sum() * 100).round(1)
        
        # Create labels with both count and percentage
        labels = [f"{mode}<br>{mode_counts[mode]:,} responses<br>({mode_percentages[mode]:.1f}%)" 
                  for mode in mode_counts.index]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=mode_counts.values,
                hole=0.4,
                marker=dict(colors=[color_map.get(mode, '#95A5A6') for mode in mode_counts.index]),
                textinfo='label',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.05] * len(mode_counts)
            )
        ])
        
        fig.update_layout(
            title=dict(
                text=f"Overall Work Mode Distribution ({year_range[0]}-{year_range[1]})",
                x=0.5,
                xanchor='center',
                font=dict(size=16)
            ),
            showlegend=False,
            margin=dict(t=80, b=20, l=20, r=20),
            height=600,
            annotations=[dict(
                text=f'Total:<br>{mode_counts.sum():,}<br>responses',
                x=0.5, y=0.5,
                font_size=14,
                showarrow=False
            )]
        )
        
        return fig
    
    @app.callback(
        Output('year-over-year-change', 'figure'),
        [Input('year-slider', 'value')]
    )
    def update_year_over_year_change(year_range):
        """Show year-over-year percentage point changes in work modes."""
        filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].copy()
        
        # Calculate percentages by year and work mode
        tab = (filtered_df[['year', 'work_mode']]
               .dropna()
               .groupby(['year', 'work_mode'], as_index=False)
               .size())
        
        tab['percentage'] = tab['size'] / tab.groupby('year')['size'].transform('sum') * 100
        
        # Calculate year-over-year change
        yoy_changes = []
        for mode in tab['work_mode'].unique():
            mode_data = tab[tab['work_mode'] == mode].sort_values('year')
            for i in range(1, len(mode_data)):
                prev_year = mode_data.iloc[i-1]['year']
                curr_year = mode_data.iloc[i]['year']
                prev_pct = mode_data.iloc[i-1]['percentage']
                curr_pct = mode_data.iloc[i]['percentage']
                change = curr_pct - prev_pct
                
                yoy_changes.append({
                    'year': f"{prev_year}-{curr_year}",
                    'work_mode': mode,
                    'change': change,
                    'year_sort': curr_year
                })
        
        if yoy_changes:
            yoy_df = pd.DataFrame(yoy_changes)
            
            fig = px.bar(yoy_df, x='year', y='change', color='work_mode',
                        title='Year-over-Year Change in Work Mode Share',
                        labels={'change': 'Percentage Point Change', 
                               'year': 'Year Transition', 
                               'work_mode': 'Work Mode'},
                        color_discrete_map=color_map,
                        barmode='group')
            
            # Add a horizontal line at zero
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add COVID annotation if relevant
            if any('2019-2020' in y or '2020-2021' in y for y in yoy_df['year'].unique()):
                fig.add_annotation(
                    x='2019-2020' if '2019-2020' in yoy_df['year'].unique() else '2020-2021',
                    y=yoy_df['change'].max(),
                    text="COVID Impact",
                    showarrow=True,
                    arrowhead=2,
                    bgcolor="rgba(255,0,0,0.1)",
                    font=dict(size=10, color="red")
                )
            
            fig.update_layout(
                hovermode='x unified',
                xaxis_tickangle=-45,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(t=80, b=100)
            )
        else:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for year-over-year comparison",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
