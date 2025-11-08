"""Callbacks for H2: The Flexibility Gap Evolution Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import WORK_MODE_COLORS, COVID_YEAR
from utils.data_processing import sorted_company_sizes
from h2.data_processing import (
    calculate_flexibility_by_size_year,
    generate_size_colors,
    calculate_flexibility_gap
)


def register_callbacks(app, df):
    """
    Register all callbacks for the H2 dashboard.
    
    Args:
        app: Dash application instance
        df: Processed DataFrame
    """
    
    # Helper function used by multiple callbacks
    flex_data_cache = {}
    
    def get_flex_data():
        """Get or cache flexibility data."""
        if 'data' not in flex_data_cache:
            flex_data_cache['data'] = calculate_flexibility_by_size_year(df)
        return flex_data_cache['data']
    
    @app.callback(
        [Output('current-gap', 'children'),
         Output('baseline-gap', 'children'),
         Output('fastest-adopter', 'children')],
        [Input('timeline-viz-type', 'value')]
    )
    def update_key_metrics(viz_type):
        """Update key metrics cards."""
        flex_data = get_flex_data()
        
        if len(flex_data) == 0:
            return "N/A", "N/A", "N/A"
        
        # Calculate gaps
        current_gap = calculate_flexibility_gap(flex_data, 2025)
        baseline_gap = calculate_flexibility_gap(flex_data, 2017)
        
        # Find fastest adopter (biggest increase from 2017 to 2025)
        fastest_adopter = "N/A"
        max_increase = 0
        
        for size in flex_data['Company Size'].unique():
            size_data = flex_data[flex_data['Company Size'] == size]
            baseline = size_data[size_data['Year'] == 2017]['Flexibility %'].values
            current = size_data[size_data['Year'] == 2025]['Flexibility %'].values
            
            if len(baseline) > 0 and len(current) > 0:
                increase = current[0] - baseline[0]
                if increase > max_increase:
                    max_increase = increase
                    fastest_adopter = size
        
        current_gap_str = f"{current_gap:.1f}pp" if current_gap is not None else "N/A"
        baseline_gap_str = f"{baseline_gap:.1f}pp" if baseline_gap is not None else "N/A"
        
        return current_gap_str, baseline_gap_str, fastest_adopter
    
    @app.callback(
        Output('timeline-chart', 'figure'),
        [Input('timeline-viz-type', 'value')]
    )
    def update_timeline_chart(viz_type):
        """Update main timeline chart based on visualization type."""
        flex_data = get_flex_data()
        
        if len(flex_data) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        sizes = flex_data['Company Size'].unique()
        size_colors = generate_size_colors(sizes)
        
        if viz_type == 'line':
            fig = px.line(flex_data,
                         x='Year',
                         y='Flexibility %',
                         color='Company Size',
                         title='Flexibility Evolution by Company Size',
                         labels={'Flexibility %': 'Percentage with Flexible Work (%)'},
                         markers=True,
                         color_discrete_map=size_colors,
                         hover_data={'Count': ':,', 'Flexibility %': ':.1f'})
        
        elif viz_type == 'area':
            fig = px.area(flex_data,
                         x='Year',
                         y='Flexibility %',
                         color='Company Size',
                         title='Flexibility Evolution (Stacked Area)',
                         labels={'Flexibility %': 'Cumulative Flexibility (%)'},
                         color_discrete_map=size_colors,
                         hover_data={'Count': ':,', 'Flexibility %': ':.1f'})
        
        elif viz_type == 'bar_race':
            fig = px.bar(flex_data,
                        x='Flexibility %',
                        y='Company Size',
                        animation_frame='Year',
                        title='Flexibility Evolution (Animated)',
                        labels={'Flexibility %': 'Percentage with Flexible Work (%)'},
                        color='Company Size',
                        color_discrete_map=size_colors,
                        text='Flexibility %',
                        orientation='h',
                        range_x=[0, 100])
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        
        else:  # facet
            fig = px.line(flex_data,
                         x='Year',
                         y='Flexibility %',
                         facet_col='Company Size',
                         facet_col_wrap=2,
                         title='Flexibility Evolution (Individual Panels)',
                         labels={'Flexibility %': 'Percentage (%)'},
                         markers=True,
                         hover_data={'Count': ':,', 'Flexibility %': ':.1f'})
        
        # Add COVID marker for non-animated charts
        if viz_type != 'bar_race':
            fig.add_vline(x=COVID_YEAR, line_dash="dash", line_color="red", opacity=0.5,
                          annotation_text="COVID-19",
                          annotation_position="top right",
                          annotation=dict(font_size=10, font_color="red"))
        
        fig.update_layout(hovermode='x unified' if viz_type == 'line' else 'closest')
        
        return fig
    
    @app.callback(
        Output('gap-evolution-chart', 'figure'),
        [Input('timeline-viz-type', 'value')]
    )
    def update_gap_evolution(viz_type):
        """Show how the flexibility gap evolved over time."""
        flex_data = get_flex_data()
        
        if len(flex_data) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate gap for each year
        gap_data = []
        for year in sorted(flex_data['Year'].unique()):
            gap = calculate_flexibility_gap(flex_data, year)
            if gap is not None:
                gap_data.append({'Year': year, 'Gap': gap})
        
        if gap_data:
            gap_df = pd.DataFrame(gap_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=gap_df['Year'],
                y=gap_df['Gap'],
                mode='lines+markers',
                name='Flexibility Gap',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=10),
                hovertemplate='<b>Year: %{x}</b><br>Gap: %{y:.1f}pp<extra></extra>'))
            
            # Add COVID marker
            fig.add_vline(x=COVID_YEAR, line_dash="dash", line_color="red", opacity=0.5,
                          annotation_text="COVID-19",
                          annotation_position="top right",
                          annotation=dict(font_size=10, font_color="red"))
            
            fig.update_layout(
                title='Evolution of Flexibility Gap (Max - Min)',
                xaxis_title='Year',
                yaxis_title='Gap (percentage points)',
                hovermode='x unified')
        else:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
    
    @app.callback(
        Output('flexibility-heatmap', 'figure'),
        [Input('timeline-viz-type', 'value')]
    )
    def update_flexibility_heatmap(viz_type):
        """Show heatmap of all years and sizes."""
        flex_data = get_flex_data()
        
        if len(flex_data) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Pivot data for heatmap
        pivot_data = flex_data.pivot(index='Company Size', columns='Year', values='Flexibility %')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn',
            text=pivot_data.values.round(1),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorbar=dict(title="Flexibility %"),
            hovertemplate='<b>Year: %{x}</b><br>Company Size: %{y}<br>Flexibility: %{z:.1f}%<extra></extra>'))
        
        fig.update_layout(
            title='Flexibility Heatmap: All Years × All Sizes',
            xaxis_title='Year',
            yaxis_title='Company Size')
        
        return fig
    
    @app.callback(
        [Output('year-compare-1', 'options'),
         Output('year-compare-2', 'options'),
         Output('company-size-selector', 'options')],
        [Input('timeline-viz-type', 'value')]
    )
    def update_dropdown_options(viz_type):
        """Populate dropdown options."""
        years = sorted(df['year'].dropna().unique())
        year_options = [{'label': str(year), 'value': year} for year in years]
        
        if 'company_size' in df.columns:
            sizes = df['company_size'].dropna().unique()
            sorted_sizes = sorted_company_sizes(sizes)
            size_options = [{'label': str(size), 'value': str(size)} for size in sorted_sizes]
        else:
            size_options = []
        
        return year_options, year_options, size_options
    
    @app.callback(
        Output('year-comparison-chart', 'figure'),
        [Input('year-compare-1', 'value'),
         Input('year-compare-2', 'value')]
    )
    def update_year_comparison(year1, year2):
        """Compare two specific years."""
        if year1 is None or year2 is None:
            fig = go.Figure()
            fig.add_annotation(text="Select two years to compare",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        flex_data = get_flex_data()
        
        if len(flex_data) == 0:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        data_year1 = flex_data[flex_data['Year'] == year1]
        data_year2 = flex_data[flex_data['Year'] == year2]
        
        # Merge data
        comparison = data_year1.merge(data_year2, on='Company Size', suffixes=(f' ({year1})', f' ({year2})'))
        
        if len(comparison) > 0:
            # Calculate change
            comparison['Change'] = comparison[f'Flexibility % ({year2})'] - comparison[f'Flexibility % ({year1})']
            comparison = comparison.sort_values('Change', ascending=True)
            
            fig = go.Figure()
            
            # Add bars for both years
            fig.add_trace(go.Bar(
                name=str(year1),
                y=comparison['Company Size'],
                x=comparison[f'Flexibility % ({year1})'],
                orientation='h',
                marker_color='#3498db',
                text=comparison[f'Flexibility % ({year1})'].round(1),
                texttemplate='%{text}%',
                textposition='outside'))
            
            fig.add_trace(go.Bar(
                name=str(year2),
                y=comparison['Company Size'],
                x=comparison[f'Flexibility % ({year2})'],
                orientation='h',
                marker_color='#e74c3c',
                text=comparison[f'Flexibility % ({year2})'].round(1),
                texttemplate='%{text}%',
                textposition='outside'))
            
            fig.update_layout(
                title=f'Flexibility Comparison: {year1} vs {year2}',
                xaxis_title='Flexibility (Remote + Hybrid) %',
                yaxis_title='Company Size',
                barmode='group',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        else:
            fig = go.Figure()
            fig.add_annotation(text="No overlapping company sizes in selected years",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
    
    @app.callback(
        Output('company-size-detail-chart', 'figure'),
        [Input('company-size-selector', 'value')]
    )
    def update_company_size_detail(selected_size):
        """Show detailed work mode breakdown for selected company size."""
        if selected_size is None:
            fig = go.Figure()
            fig.add_annotation(text="Select a company size to see its work mode evolution",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Filter data for selected size
        size_data = df[df['company_size'] == selected_size].copy()
        
        if len(size_data) == 0:
            fig = go.Figure()
            fig.add_annotation(text=f"No data available for {selected_size}",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Calculate work mode distribution by year
        mode_by_year = []
        for year in sorted(size_data['year'].dropna().unique()):
            year_data = size_data[size_data['year'] == year]
            mode_counts = year_data['work_mode'].value_counts()
            total = mode_counts.sum()
            
            for mode, count in mode_counts.items():
                mode_by_year.append({
                    'Year': int(year),
                    'Work Mode': mode.replace('_', ' ').title(),
                    'Percentage': (count / total * 100) if total > 0 else 0,
                    'Count': count
                })
        
        if mode_by_year:
            mode_df = pd.DataFrame(mode_by_year)
            
            fig = px.area(mode_df,
                         x='Year',
                         y='Percentage',
                         color='Work Mode',
                         title=f'Work Mode Evolution: {selected_size}',
                         labels={'Percentage': 'Percentage (%)'},
                         color_discrete_map={'Remote': '#45B7D1', 'Hybrid': '#FFA07A', 'On Site': '#95A5A6'},
                         hover_data={'Count': ':,', 'Percentage': ':.1f'})
            
            # Add COVID marker
            fig.add_vline(x=COVID_YEAR, line_dash="dash", line_color="red", opacity=0.5,
                          annotation_text="COVID-19")
            
            fig.update_layout(hovermode='x unified')
        else:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for visualization",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        return fig
