"""Callbacks for H5: Programming Language Evolution Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def register_callbacks(app, lang_data):
    """
    Register all callbacks for the H5 dashboard.
    
    Args:
        app: Dash application instance
        lang_data: DataFrame with language share data (columns: year, language_worked_with, count, share)
    """
    
    @app.callback(
        Output('h5-graph', 'figure'),
        [Input('h5-langs', 'value')]
    )
    def update_language_evolution_chart(lang_selection):
        """
        Update the language evolution line chart.
        
        Args:
            lang_selection: List of selected languages
            
        Returns:
            Plotly figure object
        """
        # Handle empty or None selection
        if not lang_selection:
            # If no selection, use all available languages (but show message)
            dplot = lang_data.copy()
        else:
            # Filter to selected languages
            dplot = lang_data[lang_data["language_worked_with"].isin(lang_selection)].copy()
        
        # Check if we have data
        if dplot.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected languages.<br>Please select at least one language.",
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
        dplot = dplot.sort_values(["language_worked_with", "year"])
        
        # Create line chart
        fig = px.line(
            dplot,
            x="year",
            y="share",
            color="language_worked_with",
            color_discrete_sequence=px.colors.qualitative.Bold,
            markers=True,
            labels={
                "share": "Share of Responses (%)",
                "year": "Year",
                "language_worked_with": "Language"
            },
            title="Programming Language Evolution (Share by Year)",
            hover_data={
                "share": ":.2f",
                "language_worked_with": False,
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
                title=dict(text="Programming Language"),
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
        
        # Add informative subtitle if showing all languages
        if not lang_selection or len(lang_selection) > 8:
            fig.add_annotation(
                text="Tip: Select fewer languages for a clearer view",
                xref="paper", yref="paper",
                x=0.5, y=-0.12,
                showarrow=False,
                font=dict(size=11, color="#666"),
                xanchor="center"
            )
        
        return fig
