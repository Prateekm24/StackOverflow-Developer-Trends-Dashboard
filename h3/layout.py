"""Layout for H3: The Flexibility Dividend Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(df):
    """
    Create the layout for H3 dashboard.
    
    Args:
        df: Processed DataFrame
        
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
                html.H3("H3: The Flexibility Dividend - Does Work Mode Impact Well-being?"),
                html.P("Beyond location and logistics: Explore whether flexible work arrangements actually improve developer satisfaction.", 
                       className="text-muted"),
                html.P("Comparing job satisfaction across remote, hybrid, and on-site workers before and after the COVID-19 pandemic.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Key metrics row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Highest Satisfaction", className="text-center"),
                        html.H2(id="highest-satisfaction-mode", className="text-center text-success"),
                        html.P("Work mode (Post-COVID)", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Satisfaction Gain", className="text-center"),
                        html.H2(id="biggest-gain", className="text-center text-primary"),
                        html.P("Biggest improvement", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Pre-COVID Average", className="text-center"),
                        html.H2(id="pre-covid-avg", className="text-center text-info"),
                        html.P("Overall satisfaction", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Post-COVID Average", className="text-center"),
                        html.H2(id="post-covid-avg", className="text-center text-danger"),
                        html.P("Overall satisfaction", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3)
        ], className="mb-4"),

        # Main comparison visualization
        dbc.Row([
            dbc.Col([
                html.H4("Pre-COVID vs Post-COVID: Job Satisfaction by Work Mode"),
                html.P("Select visualization type to explore satisfaction differences:", className="text-muted"),
                dcc.RadioItems(
                    id='comparison-viz-type',
                    options=[
                        {'label': ' Box Plot (Distribution)', 'value': 'box'},
                        {'label': ' Violin Plot (Density)', 'value': 'violin'},
                        {'label': ' Bar Chart (Averages)', 'value': 'bar'},
                        {'label': ' Line Chart (Trend)', 'value': 'line'}
                    ],
                    value='box',
                    inline=True,
                    className="mb-3"
                ),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='main-comparison-chart', style={'height': '600px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Detailed analysis row
        dbc.Row([
            dbc.Col([
                html.H4("Satisfaction Change: Pre to Post-COVID", className="mb-3"),
                html.P("How much did satisfaction change for each work mode?", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='change-analysis-chart', style={'height': '450px'})
                    ])
                ])
            ], width=6),
            dbc.Col([
                html.H4("Work Mode Rankings", className="mb-3"),
                html.P("Current satisfaction rankings (Post-COVID)", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='rankings-chart', style={'height': '450px'})
                    ])
                ])
            ], width=6)
        ], className="mb-4"),

        # Timeline evolution
        dbc.Row([
            dbc.Col([
                html.H4("Satisfaction Evolution Over Time (2017-2025)"),
                html.P("Track how satisfaction changed year-by-year for each work mode", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='timeline-chart', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Interactive deep dive
        dbc.Row([
            dbc.Col([
                html.H4("Interactive Deep Dive", className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Work Mode:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='work-mode-selector',
                                    options=[
                                        {'label': 'All Work Modes', 'value': 'all'},
                                        {'label': 'Remote', 'value': 'remote'},
                                        {'label': 'Hybrid', 'value': 'hybrid'},
                                        {'label': 'On-site', 'value': 'on_site'}
                                    ],
                                    value='all',
                                    className="mb-3"
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Select Period:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='period-selector',
                                    options=[
                                        {'label': 'Both Periods', 'value': 'both'},
                                        {'label': 'Pre-COVID Only (2017-2019)', 'value': 'pre'},
                                        {'label': 'Post-COVID Only (2024-2025)', 'value': 'post'}
                                    ],
                                    value='both',
                                    className="mb-3"
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Compare By:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='compare-dimension',
                                    options=[
                                        {'label': 'Work Mode', 'value': 'work_mode'},
                                        {'label': 'Year', 'value': 'year'},
                                        {'label': 'Company Size', 'value': 'company_size'}
                                    ],
                                    value='work_mode',
                                    className="mb-3"
                                )
                            ], width=4)
                        ])
                    ])
                ])
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='filtered-analysis-chart', style={'height': '500px'})
            ], width=12)
        ], className="mt-3 mb-5"),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P([
                    "Dashboard running on ",
                    html.A("http://127.0.0.1:8053", href="http://127.0.0.1:8053", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
