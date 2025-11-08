"""Callbacks for H1B: Flexibility by Organization Size Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import WORK_MODE_COLORS, COVID_YEAR


def register_callbacks(app, df):
    """
    Register all callbacks for the H1B dashboard.
    
    Args:
        app: Dash application instance
        df: Processed DataFrame
    """
    
    @app.callback(
        [Output('total-2025', 'children'),
         Output('num-company-sizes', 'children'),
         Output('most-flexible-size', 'children'),
         Output('least-flexible-size', 'children')],
        [Input('viz-type', 'value')]
    )
    def update_key_metrics(viz_type):
        """Update key metrics cards for 2025."""
        df_2025 = df[df['year'] == 2025].copy()
        
        total_responses = len(df_2025[df_2025['work_mode'].notna()])
        
        if 'company_size' in df_2025.columns:
            num_sizes = df_2025['company_size'].nunique()
            
            # Calculate flexibility by size
            flex_by_size = {}
            for size in df_2025['company_size'].dropna().unique():
                size_data = df_2025[df_2025['company_size'] == size]
                total = len(size_data[size_data['work_mode'].notna()])
                flexible = len(size_data[size_data['work_mode'].isin(['remote', 'hybrid'])])
                flex_pct = (flexible / total * 100) if total > 0 else 0
                flex_by_size[size] = flex_pct
            
            if flex_by_size:
                most_flex = max(flex_by_size, key=flex_by_size.get)
                least_flex = min(flex_by_size, key=flex_by_size.get)
            else:
                most_flex = "N/A"
                least_flex = "N/A"
        else:
            num_sizes = "N/A"
            most_flex = "N/A"
            least_flex = "N/A"
        
        return f"{total_responses:,}", str(num_sizes), str(most_flex), str(least_flex)
    
    @app.callback(
        Output('main-hybrid-chart', 'figure'),
        [Input('viz-type', 'value')]
    )
    def update_main_hybrid_chart(viz_type):
        """Update main hybrid breakdown chart based on visualization type."""
        df_2025 = df[df['year'] == 2025].copy()
        
        if 'company_size' not in df_2025.columns:
            fig = go.Figure()
            fig.add_annotation(text="Company size data not available for 2025",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate distribution
        size_mode_counts = df_2025.groupby(['company_size', 'work_mode']).size().reset_index(name='count')
        size_totals = df_2025.groupby('company_size').size().reset_index(name='total')
        merged = size_mode_counts.merge(size_totals, on='company_size')
        merged['percentage'] = (merged['count'] / merged['total'] * 100).round(1)
        
        if viz_type == 'grouped_bar':
            fig = px.bar(merged, x='company_size', y='percentage', color='work_mode',
                        title='Work Mode Distribution by Company Size (2025)',
                        labels={'percentage': 'Percentage (%)', 'company_size': 'Company Size'},
                        color_discrete_map=WORK_MODE_COLORS,
                        barmode='group',
                        text='percentage')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        
        elif viz_type == 'stacked_bar':
            fig = px.bar(merged, x='company_size', y='percentage', color='work_mode',
                        title='Work Mode Distribution by Company Size (2025) - Stacked',
                        labels={'percentage': 'Percentage (%)', 'company_size': 'Company Size'},
                        color_discrete_map=WORK_MODE_COLORS,
                        text='percentage')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        
        elif viz_type == 'heatmap':
            pivot_data = merged.pivot(index='work_mode', columns='company_size', values='percentage')
            fig = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='RdYlGn',
                text=pivot_data.values.round(1),
                texttemplate='%{text}%',
                textfont={"size": 12},
                colorbar=dict(title="Percentage")))
            fig.update_layout(title='Work Mode Distribution Heatmap (2025)',
                            xaxis_title='Company Size',
                            yaxis_title='Work Mode')
        
        else:  # multi_pie
            sizes = merged['company_size'].unique()
            n_sizes = len(sizes)
            cols = min(3, n_sizes)
            rows = (n_sizes + cols - 1) // cols
            
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=[str(size) for size in sizes],
                specs=[[{'type': 'pie'}] * cols for _ in range(rows)])
            
            for idx, size in enumerate(sizes):
                size_data = merged[merged['company_size'] == size]
                row = idx // cols + 1
                col = idx % cols + 1
                
                fig.add_trace(go.Pie(
                    labels=size_data['work_mode'],
                    values=size_data['percentage'],
                    marker=dict(colors=[WORK_MODE_COLORS.get(mode, '#95A5A6') for mode in size_data['work_mode']]),
                    textinfo='label+percent',
                    hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'),
                    row=row, col=col)
            
            fig.update_layout(title_text='Work Mode Distribution by Company Size (2025)',
                            showlegend=False)
        
        return fig
    
    @app.callback(
        Output('hybrid-comparison-bars', 'figure'),
        [Input('viz-type', 'value')]
    )
    def update_hybrid_comparison(viz_type):
        """Show remote + hybrid adoption by company size."""
        df_2025 = df[df['year'] == 2025].copy()
        
        if 'company_size' not in df_2025.columns:
            fig = go.Figure()
            fig.add_annotation(text="Company size data not available",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate flexibility percentage
        flex_data = []
        for size in df_2025['company_size'].dropna().unique():
            size_data = df_2025[df_2025['company_size'] == size]
            total = len(size_data[size_data['work_mode'].notna()])
            flexible = len(size_data[size_data['work_mode'].isin(['remote', 'hybrid'])])
            flex_pct = (flexible / total * 100) if total > 0 else 0
            
            flex_data.append({
                'Company Size': str(size),
                'Flexibility %': flex_pct,
                'Count': flexible
            })
        
        if flex_data:
            flex_df = pd.DataFrame(flex_data).sort_values('Flexibility %', ascending=False)
            
            fig = px.bar(flex_df, x='Company Size', y='Flexibility %',
                        title='Remote + Hybrid Work Adoption by Company Size',
                        labels={'Flexibility %': 'Percentage with Flexible Work (%)'},
                        text='Flexibility %',
                        color='Flexibility %',
                        color_continuous_scale='RdYlGn',
                        hover_data={'Count': ':,'})
            
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(showlegend=False)
        else:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
    
    @app.callback(
        Output('hybrid-donut', 'figure'),
        [Input('viz-type', 'value')]
    )
    def update_hybrid_donut(viz_type):
        """Show overall work mode distribution as donut chart."""
        df_2025 = df[df['year'] == 2025].copy()
        
        mode_counts = df_2025['work_mode'].value_counts()
        mode_percentages = (mode_counts / mode_counts.sum() * 100).round(1)
        
        fig = go.Figure(data=[go.Pie(
            labels=mode_counts.index,
            values=mode_counts.values,
            hole=0.4,
            marker=dict(colors=[WORK_MODE_COLORS.get(mode, '#95A5A6') for mode in mode_counts.index]),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>')])
        
        fig.update_layout(
            title='Overall Work Mode Distribution (2025)',
            showlegend=True,
            annotations=[dict(text=f'Total:<br>{mode_counts.sum():,}',
                            x=0.5, y=0.5,
                            font_size=14,
                            showarrow=False)])
        
        return fig
    
    @app.callback(
        Output('hybrid-evolution', 'figure'),
        [Input('viz-type', 'value')]
    )
    def update_hybrid_evolution(viz_type):
        """Show evolution of flexibility by company size from 2020-2025."""
        df_recent = df[(df['year'] >= 2020) & (df['year'] <= 2025)].copy()
        
        if 'company_size' not in df_recent.columns:
            fig = go.Figure()
            fig.add_annotation(text="Company size data not available",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate flexibility percentage by year and company size
        evolution_data = []
        for year in sorted(df_recent['year'].unique()):
            year_data = df_recent[df_recent['year'] == year]
            
            for size in year_data['company_size'].dropna().unique():
                size_data = year_data[year_data['company_size'] == size]
                total = len(size_data[size_data['work_mode'].notna()])
                flexible_count = len(size_data[size_data['work_mode'].isin(['remote', 'hybrid'])])
                flexibility_pct = (flexible_count / total * 100) if total > 0 else 0
                
                evolution_data.append({
                    'Year': year,
                    'Company Size': str(size),
                    'Flexibility %': flexibility_pct,
                    'Count': flexible_count
                })
        
        if evolution_data:
            evolution_df = pd.DataFrame(evolution_data)
            
            fig = px.line(evolution_df,
                         x='Year',
                         y='Flexibility %',
                         color='Company Size',
                         title='Evolution of Flexible Work by Company Size (2020-2025)',
                         labels={'Flexibility %': 'Percentage with Flexible Work (%)'},
                         markers=True,
                         hover_data={'Count': ':,', 'Flexibility %': ':.1f'})
            
            # Add COVID marker
            fig.add_vline(x=COVID_YEAR, line_dash="dash", line_color="red", opacity=0.5,
                          annotation_text="COVID-19", 
                          annotation_position="top right",
                          annotation=dict(font_size=10, font_color="red"))
            
            fig.update_layout(
                hovermode='x unified',
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02))
        else:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for evolution chart",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
    
    @app.callback(
        Output('company-size-h1b', 'options'),
        [Input('viz-type', 'value')]
    )
    def update_company_size_options(viz_type):
        """Populate company size dropdown."""
        df_2025 = df[df['year'] == 2025].copy()
        
        if 'company_size' in df_2025.columns:
            sizes = df_2025['company_size'].dropna().unique()
            options = [{'label': 'All Sizes', 'value': 'all'}] + \
                      [{'label': str(size), 'value': size} for size in sorted(sizes)]
        else:
            options = [{'label': 'All Sizes', 'value': 'all'}]
        
        return options
    
    @app.callback(
        Output('filtered-hybrid-chart', 'figure'),
        [Input('company-size-h1b', 'value'),
         Input('experience-level-h1b', 'value')]
    )
    def update_filtered_chart(company_size, experience_level):
        """Update chart based on filters - compare selected size to overall."""
        df_2025 = df[df['year'] == 2025].copy()
        
        # Calculate overall distribution
        overall_mode_counts = df_2025['work_mode'].value_counts()
        overall_pct = (overall_mode_counts / overall_mode_counts.sum() * 100).round(1)
        
        # Apply filters
        filtered_df = df_2025.copy()
        
        if company_size != 'all' and 'company_size' in df_2025.columns:
            filtered_df = filtered_df[filtered_df['company_size'] == company_size]
        
        if experience_level != 'all' and 'experience_years_code' in df_2025.columns:
            exp_ranges = {
                'junior': (0, 3),
                'mid': (4, 7),
                'senior': (8, 15),
                'expert': (16, 100)
            }
            if experience_level in exp_ranges:
                min_exp, max_exp = exp_ranges[experience_level]
                filtered_df = filtered_df[
                    (filtered_df['experience_years_code'] >= min_exp) &
                    (filtered_df['experience_years_code'] <= max_exp)
                ]
        
        # Calculate filtered distribution
        if len(filtered_df) > 0:
            filtered_mode_counts = filtered_df['work_mode'].value_counts()
            filtered_pct = (filtered_mode_counts / filtered_mode_counts.sum() * 100).round(1)
            
            # Create comparison data
            comparison_data = []
            for mode in ['remote', 'hybrid', 'on_site']:
                overall = overall_pct.get(mode, 0)
                filtered = filtered_pct.get(mode, 0)
                
                comparison_data.append({
                    'Work Mode': mode.replace('_', ' ').title(),
                    'Group': 'Overall Average',
                    'Percentage': overall
                })
                comparison_data.append({
                    'Work Mode': mode.replace('_', ' ').title(),
                    'Group': 'Selected Filter',
                    'Percentage': filtered
                })
            
            comp_df = pd.DataFrame(comparison_data)
            
            # Create title based on filters
            title_parts = []
            if company_size != 'all':
                title_parts.append(f"Company Size: {company_size}")
            if experience_level != 'all':
                title_parts.append(f"Experience: {experience_level.title()}")
            
            title = f"Work Mode Distribution Comparison (n={len(filtered_df):,})"
            if title_parts:
                title += f" - {' & '.join(title_parts)}"
            
            fig = px.bar(comp_df,
                        x='Work Mode',
                        y='Percentage',
                        color='Group',
                        title=title,
                        labels={'Percentage': 'Percentage of Respondents (%)'},
                        text='Percentage',
                        barmode='group',
                        color_discrete_map={'Overall Average': '#BDC3C7', 'Selected Filter': '#3498DB'})
            
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            
            # Add annotations if there's a significant difference
            for mode in ['remote', 'hybrid', 'on_site']:
                overall = overall_pct.get(mode, 0)
                filtered = filtered_pct.get(mode, 0)
                diff = filtered - overall
                
                if abs(diff) > 5:  # Only annotate if difference > 5%
                    fig.add_annotation(
                        x=mode.replace('_', ' ').title(),
                        y=max(overall, filtered) + 2,
                        text=f"{'+' if diff > 0 else ''}{diff:.1f}pp",
                        showarrow=False,
                        font=dict(size=10, color='red' if diff < 0 else 'green')
                    )
        else:
            fig = go.Figure()
            fig.add_annotation(text="No data available for selected filters",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
