"""Layout for H1B: Flexibility by Organization Size Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(df):
    """
    Create the layout for H1B dashboard.
    
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
                html.H3("H1B: Who Gets Hybrid? Flexibility by Organization Size (2025)"),
                html.P("Not all companies offer the same work flexibility. Discover how organization size shapes access to remote, hybrid, and on-site work.", 
                       className="text-muted"),
                html.P("From startups to enterprises: Does company size determine your work location?", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Key metrics row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total 2025 Responses", className="text-center"),
                        html.H2(id="total-2025", className="text-center text-primary"),
                        html.P("Survey respondents", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Company Sizes", className="text-center"),
                        html.H2(id="num-company-sizes", className="text-center", style={'color': '#FFA07A'}),
                        html.P("Organization categories", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Most Flexible Size", className="text-center"),
                        html.H2(id="most-flexible-size", className="text-center text-success"),
                        html.P("Highest remote/hybrid %", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Least Flexible Size", className="text-center"),
                        html.H2(id="least-flexible-size", className="text-center text-danger"),
                        html.P("Highest on-site %", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=3)
        ], className="mb-4"),

        # Main visualization section
        dbc.Row([
            dbc.Col([
                html.H4("2025 Work Mode Distribution Across Company Sizes"),
                html.P("Select visualization type to explore the data:", className="text-muted"),
                dcc.RadioItems(
                    id='viz-type',
                    options=[
                        {'label': ' Grouped Bar Chart (Side-by-side comparison)', 'value': 'grouped_bar'},
                        {'label': ' Stacked Bar Chart (100% view)', 'value': 'stacked_bar'},
                        {'label': ' Heatmap (Pattern recognition)', 'value': 'heatmap'},
                        {'label': ' Multiple Pie Charts (Individual breakdowns)', 'value': 'multi_pie'}
                    ],
                    value='grouped_bar',
                    inline=True,
                    className="mb-3"
                ),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='main-hybrid-chart', style={'height': '600px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Detailed breakdown section
        dbc.Row([
            dbc.Col([
                html.H4("Remote + Hybrid Adoption by Company Size", className="mb-3"),
                html.P("Percentage of flexible work options across organization sizes", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='hybrid-comparison-bars', style={'height': '500px'})
                    ])
                ])
            ], width=8),
            dbc.Col([
                html.H4("Work Mode Mix", className="mb-3"),
                html.P("Distribution across all modes", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='hybrid-donut', style={'height': '500px'})
                    ])
                ])
            ], width=4)
        ], className="mb-4"),

        # Evolution section
        dbc.Row([
            dbc.Col([
                html.H4("Evolution of Flexibility: Company Size Trends (2020-2025)"),
                html.P("Track how different organization sizes adopted remote/hybrid work arrangements", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='hybrid-evolution', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Interactive filter section
        dbc.Row([
            dbc.Col([
                html.H4("Deep Dive: Select a Company Size", className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Company Size to Explore:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='company-size-h1b',
                                    options=[{'label': 'All Sizes (Overview)', 'value': 'all'}],
                                    value='all',
                                    className="mb-3"
                                ),
                                html.P("Shows work mode distribution for selected company size compared to the overall average", 
                                       className="text-muted small fst-italic")
                            ], width=6),
                            dbc.Col([
                                html.Label("Additional Filter by Experience:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='experience-level-h1b',
                                    options=[
                                        {'label': 'All Experience Levels', 'value': 'all'},
                                        {'label': 'Junior (0-3 years)', 'value': 'junior'},
                                        {'label': 'Mid (4-7 years)', 'value': 'mid'},
                                        {'label': 'Senior (8-15 years)', 'value': 'senior'},
                                        {'label': 'Expert (15+ years)', 'value': 'expert'}
                                    ],
                                    value='all',
                                    className="mb-3"
                                ),
                                html.P("Refine analysis by combining company size with seniority level", 
                                       className="text-muted small fst-italic")
                            ], width=6)
                        ])
                    ])
                ])
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='filtered-hybrid-chart', style={'height': '500px'})
            ], width=12)
        ], className="mt-3 mb-5"),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P([
                    "Dashboard running on ",
                    html.A("http://127.0.0.1:8051", href="http://127.0.0.1:8051", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
