"""Main runner for H1A: Global Shift in Work Mode Dashboard."""
import sys
from pathlib import Path

# CRITICAL: Add project root to Python path FIRST
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dash import html, Dash
import dash_bootstrap_components as dbc

# Now import from our modules
from config import PORTS, HOST, WORK_MODE_COLORS
from utils import load_data_for_h1a, schedule_browser_open
from h1a.layout import create_layout
from h1a.callbacks import register_callbacks


def main():
    """Initialize and run the H1A dashboard."""
    # Load data
    print("Loading Stack Overflow survey data for H1A...")
    df = load_data_for_h1a()
    
    # Initialize Dash App
    app = Dash(__name__, 
               external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True
               )
    
    
    color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)
    
    # Set up layout
    app.layout = create_layout(df, WORK_MODE_COLORS)
    
    # Register callbacks
    register_callbacks(app, df, WORK_MODE_COLORS)
    
    # Print startup info
    port = PORTS['h1a']
    print("\n" + "="*60)
    print("Starting Stack Overflow Dashboard Server - H1A Enhanced")
    print("="*60)
    print(f"\n Dashboard will be available at: http://{HOST}:{port}/")
    print(" Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    # Open browser after delay (Uncomment for automatic browser launch)
    # schedule_browser_open(port)
    
    # Run the server
    app.run(debug=True, port=port, host=HOST)


if __name__ == '__main__':
    main()
