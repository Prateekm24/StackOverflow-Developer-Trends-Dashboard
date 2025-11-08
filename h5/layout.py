"""Layout for H5: Programming Language Evolution Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(available_languages, default_selection):
    """
    Create the layout for H5 dashboard.
    
    Args:
        available_languages: List of available programming languages
        default_selection: Default languages to show
        
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
                html.H3("H5: Programming Language Evolution (2017-2025)"),
                html.P("Track the rise and fall of programming languages over time based on developer usage", 
                       className="text-muted"),
                html.P("Watch how language popularity shifts as new technologies emerge and older ones fade.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Key insights card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📊 About This Analysis", className="mb-3"),
                        html.Ul([
                            html.Li("Shows the percentage of developers using each language per year"),
                            html.Li("Data is based on the 'Languages Worked With' question from Stack Overflow surveys"),
                            html.Li("Developers can select multiple languages, so percentages don't sum to 100%"),
                            html.Li("Only the top 12 most-mentioned languages are available for selection")
                        ], className="mb-0")
                    ])
                ], color="light")
            ], width=12)
        ], className="mb-4"),

        # Language selector
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Languages to Compare:", className="fw-bold"),
                        html.P("Choose up to 10 languages to see their evolution over time", 
                               className="text-muted small mb-2"),
                        dcc.Dropdown(
                            id='h5-langs',
                            options=[
                                {'label': lang, 'value': lang} 
                                for lang in sorted(available_languages)
                            ],
                            value=default_selection,
                            multi=True,
                            placeholder="Select languages...",
                            className="mb-2"
                        ),
                        html.Small("Tip: Start with 3-5 languages for clearer visualization. Add more to compare trends.", 
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
                        html.H5("Language Usage Share Over Time", className="mb-3"),
                        html.P("Each line represents the percentage of survey respondents who reported using that language", 
                               className="text-muted small"),
                        dcc.Graph(id='h5-graph', style={'height': '600px'})
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
                            html.Li("Click on legend items to show/hide specific languages"),
                            html.Li("Hover over lines to see exact percentages for each year"),
                            html.Li("Sharp increases often indicate growing ecosystems (e.g., JavaScript frameworks)"),
                            html.Li("Gradual declines may show languages being replaced by newer alternatives"),
                            html.Li("Stable lines indicate mature, established languages with consistent usage")
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
                    html.A("http://127.0.0.1:8056", href="http://127.0.0.1:8056", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
