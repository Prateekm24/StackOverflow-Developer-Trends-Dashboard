"""Layout for H4: Experience vs Compensation Dashboard."""
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(df, years_all, years_valid, default_year, work_modes, company_sizes):
    """
    Create the layout for H4 dashboard.
    
    Args:
        df: Processed DataFrame
        years_all: All years available in dataset
        years_valid: Years with valid experience and compensation data
        default_year: Default year to display
        work_modes: Available work modes
        company_sizes: Available company sizes
        
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
                html.H3("H4: Experience vs Compensation Analysis"),
                html.P("Exploring the relationship between years of professional coding experience and annual compensation", 
                       className="text-muted"),
                html.P("Filter by work mode and company size to see how these factors influence the experience-compensation relationship.", 
                       className="text-muted fst-italic")
            ], width=12)
        ]),

        # Controls Card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Year Slider
                        html.Label("Select Year:", className="fw-bold"),
                        dcc.Slider(
                            id='h4-year',
                            min=int(min(years_all)),
                            max=int(max(years_all)),
                            step=1,
                            value=int(default_year),
                            marks={int(y): str(int(y)) for y in years_all},
                            className="mb-4"
                        ),
                        
                        # Work Mode Filter
                        html.Label("Work Mode Filter:", className="fw-bold mt-3"),
                        dcc.Checklist(
                            id='h4-workmode',
                            options=[
                                {'label': f' {w.replace("_", " ").title()}', 'value': w} 
                                for w in sorted(work_modes)
                            ],
                            value=sorted(work_modes),
                            inline=True,
                            className="mb-3"
                        ),
                        
                        # Company Size Filter
                        html.Label("Company Size Filter:", className="fw-bold mt-3"),
                        dcc.Checklist(
                            id='h4-cosize',
                            options=[
                                {'label': f' {s}', 'value': s} 
                                for s in sorted(company_sizes)
                            ],
                            value=sorted(company_sizes),
                            inline=True,
                            className="mb-2"
                        ),
                        
                        html.Small("Note: Compensation values are clipped at 1st-99th percentiles to remove extreme outliers", 
                                 className="text-muted fst-italic")
                    ])
                ], className="mb-4")
            ], width=12)
        ]),

        # Main scatter plot with trendline
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Experience vs Compensation Scatter Plot", className="mb-3"),
                        html.P("Each point represents a survey respondent. Trendlines show the overall relationship for each work mode.", 
                               className="text-muted small"),
                        dcc.Graph(id='h4-graph', style={'height': '600px'})
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
                            html.Li("Hover over points to see detailed information including company size and job satisfaction"),
                            html.Li("Trendlines (when available) show the average relationship between experience and compensation"),
                            html.Li("Different work modes may show different compensation patterns"),
                            html.Li("Use filters to explore specific combinations of work mode and company size")
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
                    html.A("http://127.0.0.1:8055", href="http://127.0.0.1:8055", target="_blank"),
                    " | Press Ctrl+C in terminal to stop"
                ], className="text-center text-muted mb-3")
            ], width=12)
        ])

    ], fluid=True)
