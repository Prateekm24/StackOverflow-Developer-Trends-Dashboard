"""Callbacks for H6a: Framework Cohorts Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from h6a.data_processing import get_top_frameworks_by_cohort


# Define color palettes for different cohorts
COHORT_PALETTES = {
    'Front-End': px.colors.qualitative.Set1,
    'Back-End': px.colors.qualitative.Pastel1,
    'Other': px.colors.qualitative.Safe,
    'All': px.colors.qualitative.Safe
}


def register_callbacks(app, fw_data):
    """
    Register all callbacks for the H6a dashboard.
    
    Args:
        app: Dash application instance
        fw_data: DataFrame with framework share data (columns: year, framework_worked_with, count, share, cohort)
    """
    
    @app.callback(
        Output('h6a-graph', 'figure'),
        [Input('h6a-cohort', 'value'),
         Input('h6a-topn', 'value')]
    )
    def update_framework_cohort_chart(cohort_selection, top_n):
        """
        Update the framework cohort evolution line chart.
        
        Args:
            cohort_selection: Selected cohort ("Front-End", "Back-End", "Other", or "All")
            top_n: Number of top frameworks to display
            
        Returns:
            Plotly figure object
        """
        # Ensure top_n has a valid value
        top_n = int(top_n or 8)
        
        # Filter data by cohort if not "All"
        if cohort_selection != "All":
            base_data = fw_data[fw_data["cohort"] == cohort_selection].copy()
        else:
            base_data = fw_data.copy()
        
        # Get top frameworks for the selected cohort
        top_frameworks = get_top_frameworks_by_cohort(
            fw_counts=fw_data,
            cohort=cohort_selection,
            n=top_n
        )
        
        # Filter to top frameworks
        dplot = base_data[base_data["framework_worked_with"].isin(top_frameworks)].copy()
        
        # Check if we have data
        if dplot.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"No data available for {cohort_selection} frameworks.<br>Try selecting a different cohort.",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666")
            )
            fig.update_layout(
                xaxis={'visible': False},
                yaxis={'visible': False},
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            return fig
        
        # Sort data for proper line plotting
        dplot = dplot.sort_values(["framework_worked_with", "year"])
        
        # Get appropriate color palette for cohort
        color_palette = COHORT_PALETTES.get(cohort_selection, px.colors.qualitative.Safe)
        
        # Create line chart
        fig = px.line(
            dplot,
            x="year",
            y="share",
            color="framework_worked_with",
            color_discrete_sequence=color_palette,
            markers=True,
            labels={
                "share": "Share of Responses (%)",
                "year": "Year",
                "framework_worked_with": "Framework"
            },
            title=f"Framework Cohorts: {cohort_selection} (Top {top_n} by Mentions)",
            hover_data={
                "share": ":.2f",
                "framework_worked_with": False,
                "year": True
            }
        )
        
        # Update line styling
        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(size=8)
        )
        
        # Update layout
        fig.update_layout(
            hovermode='x unified',
            legend=dict(
                title=dict(text="Framework"),
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.2)",
                borderwidth=1
            ),
            plot_bgcolor='rgba(250, 250, 250, 0.5)',
            xaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zeroline=False,
                dtick=1  # Show every year
            ),
            yaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zeroline=False,
                title="Share of Responses (%)"
            ),
            margin=dict(t=80, b=60, l=80, r=180)
        )
        
        # Add cohort-specific annotation
        cohort_descriptions = {
            'Front-End': 'UI/UX frameworks for browser-based applications',
            'Back-End': 'Server-side frameworks for business logic and APIs',
            'Other': 'Frameworks not categorized as Front-End or Back-End',
            'All': 'All frameworks across all categories'
        }
        
        fig.add_annotation(
            text=cohort_descriptions.get(cohort_selection, ''),
            xref="paper", yref="paper",
            x=0.5, y=-0.12,
            showarrow=False,
            font=dict(size=11, color="#666", style="italic"),
            xanchor="center"
        )
        
        return fig
