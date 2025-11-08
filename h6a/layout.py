"""Layout for H6a: Framework Cohorts Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout():
    """
    Create the layout for H6a dashboard.
    
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
                html.H3("H6a: Framework Cohorts - Rise & Fall"),
                html.P("Track the evolution of web frameworks organized by their primary use case", 
                       className="text-muted"),
                html.P("Watch how front-end and back-end frameworks compete within their ecosystems over time.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Key insights card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📊 About Framework Cohorts", className="mb-3"),
                        html.Div([
                            html.P([
                                html.Strong("Front-End Frameworks: "),
                                "React, Angular, Vue.js, Svelte, Ember.js, Next.js, Nuxt.js"
                            ], className="mb-2"),
                            html.P([
                                html.Strong("Back-End Frameworks: "),
                                "Django, Flask, Spring, Express, Laravel, FastAPI, Ruby on Rails, ASP.NET, ASP.NET Core"
                            ], className="mb-2"),
                            html.P([
                                html.Strong("Other: "),
                                "All frameworks not classified in the above categories"
                            ], className="mb-0")
                        ])
                    ])
                ], color="light")
            ], width=12)
        ], className="mb-4"),

        # Controls Card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Cohort selector
                        html.Label("Select Framework Cohort:", className="fw-bold"),
                        dcc.RadioItems(
                            id='h6a-cohort',
                            options=[
                                {'label': ' Front-End', 'value': 'Front-End'},
                                {'label': ' Back-End', 'value': 'Back-End'},
                                {'label': ' Other', 'value': 'Other'},
                                {'label': ' All Frameworks', 'value': 'All'}
                            ],
                            value='All',
                            inline=True,
                            className="mb-4"
                        ),
                        
                        # Top N slider
                        html.Label("Number of Top Frameworks to Display:", className="fw-bold mt-3"),
                        html.P("Show the most-mentioned frameworks in the selected cohort", 
                               className="text-muted small mb-2"),
                        dcc.Slider(
                            id='h6a-topn',
                            min=3,
                            max=15,
                            step=1,
                            value=8,
                            marks={i: str(i) for i in range(3, 16)},
                            className="mb-2"
                        ),
                        html.Small("Tip: Start with 5-8 frameworks for optimal visualization", 
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
                        html.H5("Framework Usage Share Over Time", className="mb-3"),
                        html.P("Rise and fall of frameworks within their cohort. Lines show percentage of developers using each framework.", 
                               className="text-muted small"),
                        dcc.Graph(id='h6a-graph', style={'height': '600px'})
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
                            html.Li("Different cohorts use different color palettes for easy distinction"),
                            html.Li("Rising lines indicate frameworks gaining developer adoption"),
                            html.Li("Falling lines may indicate frameworks losing market share to competitors"),
                            html.Li("Adjust the Top N slider to focus on the most popular frameworks"),
                            html.Li("Click legend items to show/hide specific frameworks for clearer comparison")
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
                    html.A("http://127.0.0.1:8057", href="http://127.0.0.1:8057", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
