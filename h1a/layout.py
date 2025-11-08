"""Layout for H1A: Global Shift in Work Mode Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(df, color_map):
    """
    Create the layout for H1A dashboard.
    
    Args:
        df: Processed DataFrame
        color_map: Dictionary mapping work modes to colors
        
    Returns:
        Dash layout component
    """
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Stack Overflow Developer Survey Analysis",
                       className="text-center mb-4 mt-4"),
                html.Hr()
            ])
        ]),

        # Title and description
        dbc.Row([
            dbc.Col([
                html.H3("H1A: Global Shift in Work Mode (2017-2025)"),
                html.P("How the COVID-19 pandemic transformed where developers work", 
                       className="text-muted"),
                html.P("Notice the dramatic shift beginning in 2020, when remote work became the new normal.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Pre/Post COVID Comparison Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Remote Work Pre-COVID", className="text-center"),
                        html.H2(id="pre-covid-remote", className="text-center", 
                               style={'color': '#e74c3c'}),
                        html.P("(2017-2019 Average)", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Remote Work Post-COVID", className="text-center"),
                        html.H2(id="post-covid-remote", className="text-center", 
                               style={'color': '#27ae60'}),
                        html.P("(2021-2025 Average)", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Change", className="text-center"),
                        html.H2(id="change-remote", className="text-center", 
                               style={'color': '#3498db'}),
                        html.P("Percentage Points", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4)
        ], className="mb-4"),

        # Controls
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Visualization Type:", className="fw-bold"),
                        dcc.RadioItems(
                            id='chart-type',
                            options=[
                                {'label': ' Line Chart (Best for trends)', 'value': 'line'},
                                {'label': ' Stacked Area Chart', 'value': 'area'},
                                {'label': ' Stacked Bar Chart', 'value': 'bar'},
                                {'label': ' Grouped Bar Chart', 'value': 'grouped_bar'}
                            ],
                            value='line',
                            inline=True,
                            className="mb-3"
                        ),

                        html.Label("Select Years:", className="fw-bold mt-3"),
                        dcc.RangeSlider(
                            id='year-slider',
                            min=df['year'].min(),
                            max=df['year'].max(),
                            value=[df['year'].min(), df['year'].max()],
                            marks={str(year): str(year) for year in sorted(df['year'].dropna().unique())},
                            step=1,
                            className="mb-3"
                        ),

                        html.Div([
                            dcc.Checklist(
                                id='story-mode',
                                options=[{'label': ' Story Mode (Focus on 2018-2022 shift)', 'value': 'story'}],
                                value=[],
                                className="mb-2"
                            ),
                            html.Small("Story Mode highlights the critical transition period", 
                                     className="text-muted fst-italic")
                        ])
                    ])
                ], className="mb-4")
            ], width=12)
        ]),

        # Main chart
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='work-mode-chart', style={'height': '500px'})
            ], width=12)
        ]),

        # Summary statistics
        dbc.Row([
            dbc.Col([
                html.H3("Overall Work Mode Distribution", className="mt-4"),
                html.P("Click on a work mode to see its detailed trend over time", 
                       className="text-muted fst-italic"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='summary-stats', style={'height': '600px'})
                    ])
                ])
            ], width=6),
            dbc.Col([
                html.H3("Year-over-Year Growth Rates", className="mt-4"),
                html.P("Percentage point change in each work mode from previous year", 
                       className="text-muted fst-italic"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='year-over-year-change', style={'height': '600px'})
                    ])
                ])
            ], width=6)
        ], className="mb-5"),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P([
                    "Dashboard running on ",
                    html.A("http://127.0.0.1:8050", href="http://127.0.0.1:8050", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
