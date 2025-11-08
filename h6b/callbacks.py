"""Callbacks for H6b: Framework Lifecycles Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dash_table
import sys
from pathlib import Path
from dash import html

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def register_callbacks(app, fw_data, lifecycle_stats):
    """
    Register all callbacks for the H6b dashboard.
    
    Args:
        app: Dash application instance
        fw_data: DataFrame with framework share data (columns: year, framework_worked_with, count, share)
        lifecycle_stats: DataFrame with lifecycle statistics (columns: framework, first_year, peak_year, peak_share)
    """
    
    @app.callback(
        [Output('h6b-graph', 'figure'),
         Output('h6b-table', 'children')],
        [Input('h6b-fw', 'value')]
    )
    def update_framework_lifecycle_chart_and_table(framework_selection):
        """
        Update the framework lifecycle chart and statistics table.
        
        Args:
            framework_selection: List of selected frameworks
            
        Returns:
            Tuple of (figure, table_component)
        """
        # Handle empty or None selection
        if not framework_selection:
            # Show empty state
            fig = go.Figure()
            fig.add_annotation(
                text="Select one or more frameworks to view their lifecycles.<br>Use the dropdown above to make a selection.",
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
            
            # Return empty figure and empty div
            return fig, html.Div()
        
        # Filter data to selected frameworks
        dplot = fw_data[fw_data["framework_worked_with"].isin(framework_selection)].copy()
        
        # Check if we have data
        if dplot.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected frameworks.<br>Try selecting different frameworks.",
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
            return fig, html.Div()
        
        # Sort data for proper line plotting
        dplot = dplot.sort_values(["framework_worked_with", "year"])
        
        # Create line chart
        fig = px.line(
            dplot,
            x="year",
            y="share",
            color="framework_worked_with",
            color_discrete_sequence=px.colors.qualitative.Safe,
            markers=True,
            labels={
                "share": "Share of Responses (%)",
                "year": "Year",
                "framework_worked_with": "Framework"
            },
            title="Framework Lifecycles (Entry & Peak)",
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
        
        # Add peak markers for selected frameworks
        for framework in framework_selection:
            # Get lifecycle stats for this framework
            fw_stats = lifecycle_stats[lifecycle_stats["framework"] == framework]
            
            if not fw_stats.empty:
                peak_year = fw_stats.iloc[0]["peak_year"]
                peak_share = fw_stats.iloc[0]["peak_share"]
                
                # Add annotation for peak
                fig.add_annotation(
                    x=peak_year,
                    y=peak_share,
                    text=f"Peak: {peak_share:.1f}%",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#666",
                    ax=0,
                    ay=-40,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#666",
                    borderwidth=1,
                    font=dict(size=10)
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
        
        # Create lifecycle statistics table
        lifecycle_filtered = lifecycle_stats[
            lifecycle_stats["framework"].isin(framework_selection)
        ].sort_values("peak_share", ascending=False)
        
        # Format the table data
        table_data = lifecycle_filtered.copy()
        table_data["peak_share"] = table_data["peak_share"].round(2)
        
        # Create Dash DataTable
        table = dash_table.DataTable(
            columns=[
                {"name": "Framework", "id": "framework"},
                {"name": "First Year", "id": "first_year"},
                {"name": "Peak Year", "id": "peak_year"},
                {"name": "Peak Share (%)", "id": "peak_share"}
            ],
            data=table_data.to_dict("records"),
            style_table={
                "overflowX": "auto",
                "borderRadius": "10px",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.06)"
            },
            style_cell={
                "padding": "12px",
                "fontFamily": "Inter, Arial, sans-serif",
                "fontSize": "14px",
                "textAlign": "left"
            },
            style_header={
                "fontWeight": 700,
                "backgroundColor": "rgba(44, 62, 80, 0.05)",
                "borderBottom": "2px solid rgba(44, 62, 80, 0.2)"
            },
            style_data={
                "backgroundColor": "white",
                "borderBottom": "1px solid rgba(200, 200, 200, 0.3)"
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgba(250, 250, 250, 0.5)"
                }
            ]
        )
        
        return fig, table
