"""Layout for H2: The Flexibility Gap Evolution Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(df):
    """
    Create the layout for H2 dashboard.
    
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

        # Title and info box
        dbc.Row([
            dbc.Col([
                html.H3("H2: The Flexibility Gap - How Company Size Differences Evolved (2017-2025)"),
                html.P("Not all organizations moved to flexible work at the same pace. Explore how the flexibility gap between company sizes developed over 8 years.", 
                       className="text-muted"),
                html.P("From the pre-COVID baseline to today: Did large and small companies converge or diverge in their work arrangements?", 
                       className="text-muted fst-italic")
            ], width=9),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-info-circle me-2"),
                        html.Strong("Key Terms Explained")
                    ], className="bg-info text-white"),
                    dbc.CardBody([
                        html.P([
                            html.Strong("Flexibility %: "),
                            "Percentage of workers with remote or hybrid arrangements. ",
                            html.Br(),
                            html.Small("Formula: (Remote + Hybrid) ÷ Total × 100", className="text-muted fst-italic")
                        ], className="mb-2 small"),
                        html.P([
                            html.Strong("Gap: "),
                            "Difference between most and least flexible company sizes. ",
                            html.Br(),
                            html.Small("Formula: Max Flexibility % − Min Flexibility %", className="text-muted fst-italic")
                        ], className="mb-2 small"),
                        html.P([
                            html.Strong("pp (percentage points): "),
                            "Unit for comparing percentages. A change from 20% to 30% is +10pp, not +10%."
                        ], className="mb-2 small"),
                        html.P([
                            html.Strong("Company Sizes: "),
                            "Four categories from smallest (1-9 employees) to largest (1000+ employees)."
                        ], className="mb-0 small")
                    ], style={'padding': '0.75rem'})
                ], className="shadow-sm")
            ], width=3)
        ]),

        # Key metrics row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Flexibility Gap (2025)", className="text-center"),
                        html.H2(id="current-gap", className="text-center text-danger"),
                        html.P("pp difference (max-min)", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Flexibility Gap (2017)", className="text-center"),
                        html.H2(id="baseline-gap", className="text-center text-info"),
                        html.P("pp difference (max-min)", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Fastest Adopter", className="text-center"),
                        html.H2(id="fastest-adopter", className="text-center text-success"),
                        html.P("Biggest flexibility gain", className="text-center text-muted small")
                    ])
                ], color="light")
            ], width=4)
        ], className="mb-4"),

        # Main timeline visualization
        dbc.Row([
            dbc.Col([
                html.H4("Flexibility Over Time: Company Size Trajectories (2017-2025)"),
                html.P("Select visualization to explore the evolution:", className="text-muted"),
                dcc.RadioItems(
                    id='timeline-viz-type',
                    options=[
                        {'label': ' Line Chart with Markers', 'value': 'line'},
                        {'label': ' Area Chart (Stacked)', 'value': 'area'},
                        {'label': ' Animated Bar Race', 'value': 'bar_race'},
                        {'label': ' Small Multiples (Faceted)', 'value': 'facet'}
                    ],
                    value='line',
                    inline=True,
                    className="mb-3"
                ),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='timeline-chart', style={'height': '500px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Gap evolution chart
        dbc.Row([
            dbc.Col([
                html.H4("Flexibility Gap Evolution (2017-2025)"),
                html.P("Tracking the difference between most and least flexible company sizes over time", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='gap-evolution-chart', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Heatmap section
        dbc.Row([
            dbc.Col([
                html.H4("Flexibility Heatmap: Complete View"),
                html.P("All years and company sizes at a glance", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='flexibility-heatmap', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Year comparison section
        dbc.Row([
            dbc.Col([
                html.H4("Year-to-Year Comparison Tool"),
                html.P("Select two years to compare flexibility patterns", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("First Year:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='year-compare-1',
                                    options=[],
                                    value=2017,
                                    className="mb-3"
                                )
                            ], width=6),
                            dbc.Col([
                                html.Label("Second Year:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='year-compare-2',
                                    options=[],
                                    value=2025,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        dcc.Graph(id='year-comparison-chart', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-4"),

        # Company size detail section
        dbc.Row([
            dbc.Col([
                html.H4("Deep Dive: Individual Company Size Analysis"),
                html.P("Select a company size to see its complete work mode evolution", className="text-muted"),
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Company Size:", className="fw-bold"),
                        dcc.Dropdown(
                            id='company-size-selector',
                            options=[],
                            value=None,
                            placeholder="Choose a company size...",
                            className="mb-3"
                        ),
                        dcc.Graph(id='company-size-detail-chart', style={'height': '400px'})
                    ])
                ])
            ], width=12)
        ], className="mb-5"),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P([
                    "Dashboard running on ",
                    html.A("http://127.0.0.1:8052", href="http://127.0.0.1:8052", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
