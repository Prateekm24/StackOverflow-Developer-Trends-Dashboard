"""Layout for H6b: Framework Lifecycles Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(available_frameworks, default_selection):
    """
    Create the layout for H6b dashboard.
    
    Args:
        available_frameworks: List of available frameworks
        default_selection: Default frameworks to show
        
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
                html.H3("H6b: Framework Lifecycles - Entry & Peak Analysis"),
                html.P("Track when frameworks first appeared and when they reached peak popularity", 
                       className="text-muted"),
                html.P("Understand the lifecycle stages of web frameworks: entry, growth, peak, and decline.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Key insights card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📊 About Framework Lifecycles", className="mb-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("First Year: "),
                                "When the framework first appeared in Stack Overflow survey data"
                            ]),
                            html.Li([
                                html.Strong("Peak Year: "),
                                "The year when the framework reached its highest usage share"
                            ]),
                            html.Li([
                                html.Strong("Peak Share: "),
                                "The maximum percentage of developers using the framework"
                            ]),
                            html.Li([
                                "The lifecycle table below shows detailed statistics for selected frameworks"
                            ])
                        ], className="mb-0")
                    ])
                ], color="light")
            ], width=12)
        ], className="mb-4"),

        # Framework selector
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Frameworks to Analyze:", className="fw-bold"),
                        html.P("Choose frameworks to see their complete lifecycle trajectories", 
                               className="text-muted small mb-2"),
                        dcc.Dropdown(
                            id='h6b-fw',
                            options=[
                                {'label': fw, 'value': fw} 
                                for fw in sorted(available_frameworks)
                            ],
                            value=default_selection,
                            multi=True,
                            placeholder="Select frameworks...",
                            className="mb-2"
                        ),
                        html.Small("Tip: Start with 3-5 frameworks for optimal comparison", 
                                 className="text-muted fst-italic")
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Main line chart
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Framework Lifecycle Trajectories", className="mb-3"),
                        html.P("Track each framework from entry through peak and beyond", 
                               className="text-muted small"),
                        dcc.Graph(id='h6b-graph', style={'height': '600px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Lifecycle statistics table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📋 Framework Lifecycle Statistics", className="mb-3"),
                        html.P("Detailed entry and peak information for selected frameworks", 
                               className="text-muted small"),
                        html.Div(id='h6b-table')
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Insights section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("💡 Key Insights", className="mb-3"),
                        html.Ul([
                            html.Li("Frameworks with earlier first years are more established technologies"),
                            html.Li("Time between first year and peak year indicates growth rate"),
                            html.Li("Frameworks still at their peak may be currently dominant"),
                            html.Li("Frameworks past their peak may be in decline or stabilization"),
                            html.Li("Use the table to compare lifecycle metrics across frameworks")
                        ], className="mb-0")
                    ])
                ], color="light")
            ], width=12)
        ]),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(className="mt-4"),
                html.P([
                    "Dashboard running on ",
                    html.A("http://127.0.0.1:8058", href="http://127.0.0.1:8058", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
