"""Callbacks for H4: Experience vs Compensation Dashboard."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from h4.data_processing import prepare_experience_compensation_data


def register_callbacks(app, df, color_map):
    """
    Register all callbacks for the H4 dashboard.
    
    Args:
        app: Dash application instance
        df: Processed DataFrame with comp_clipped column
        color_map: Dictionary mapping work modes to colors
    """
    
    @app.callback(
        Output('h4-graph', 'figure'),
        [Input('h4-year', 'value'),
         Input('h4-workmode', 'value'),
         Input('h4-cosize', 'value')]
    )
    def update_experience_compensation_chart(year, workmodes, cosizes):
        """
        Update the experience vs compensation scatter plot.
        
        Args:
            year: Selected year
            workmodes: List of selected work modes
            cosizes: List of selected company sizes
            
        Returns:
            Plotly figure object
        """
        # Handle empty selections
        workmodes = workmodes or []
        cosizes = cosizes or []
        
        # Prepare filtered data
        dff = prepare_experience_compensation_data(
            df=df,
            year=year,
            work_modes=workmodes if workmodes else None,
            company_sizes=cosizes if cosizes else None
        )
        
        # Check if we have data
        if dff.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected filters/year.<br>Try adjusting your filters.",
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
        
        # Create scatter plot with trendline
        try:
            # Try to create plot with OLS trendline
            fig = px.scatter(
                dff,
                x="experience_years_code_pro",
                y="comp_clipped",
                color="work_mode",
                color_discrete_map=color_map,
                hover_data={
                    "company_size": True,
                    "job_satisfaction": True,
                    "experience_years_code_pro": ':.1f',
                    "comp_clipped": ':,.0f',
                    "work_mode": False
                },
                trendline="ols",
                labels={
                    "experience_years_code_pro": "Years of Professional Coding Experience",
                    "comp_clipped": "Annual Compensation (USD, clipped 1-99%)",
                    "work_mode": "Work Mode"
                },
                title=f"Experience vs Compensation ({year})"
            )
        except Exception as e:
            # Fallback to plot without trendline if OLS fails
            print(f"Trendline calculation failed: {e}. Creating plot without trendline.")
            fig = px.scatter(
                dff,
                x="experience_years_code_pro",
                y="comp_clipped",
                color="work_mode",
                color_discrete_map=color_map,
                hover_data={
                    "company_size": True,
                    "job_satisfaction": True,
                    "experience_years_code_pro": ':.1f',
                    "comp_clipped": ':,.0f',
                    "work_mode": False
                },
                labels={
                    "experience_years_code_pro": "Years of Professional Coding Experience",
                    "comp_clipped": "Annual Compensation (USD, clipped 1-99%)",
                    "work_mode": "Work Mode"
                },
                title=f"Experience vs Compensation ({year})"
            )
        
        # Update marker styling
        fig.update_traces(
            marker=dict(
                size=7,
                opacity=0.7,
                line=dict(width=0.5, color='white')
            )
        )
        
        # Update layout
        fig.update_layout(
            hovermode='closest',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title=dict(text="Work Mode")
            ),
            plot_bgcolor='rgba(250, 250, 250, 0.5)',
            xaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(200, 200, 200, 0.3)',
                zeroline=False
            ),
            margin=dict(t=60, b=60, l=80, r=40)
        )
        
        return fig
