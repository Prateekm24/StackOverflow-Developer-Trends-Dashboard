"""Main runner for H2: The Flexibility Gap Evolution Dashboard."""
import sys
from pathlib import Path

# CRITICAL: Add project root to Python path FIRST
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dash import Dash
import dash_bootstrap_components as dbc

# Now import from our modules
from config import PORTS, HOST
from utils import load_data_for_h2, schedule_browser_open
from h2.layout import create_layout
from h2.callbacks import register_callbacks


def main():
    """Initialize and run the H2 dashboard."""
    # Load data
    print("Loading Stack Overflow survey data for H2...")
    df = load_data_for_h2()
    
    # Initialize Dash App
    app = Dash(__name__, 
               external_stylesheets=[dbc.themes.BOOTSTRAP],
               suppress_callback_exceptions=True)
    
    # Set up layout
    app.layout = create_layout(df)
    
    # Register callbacks
    register_callbacks(app, df)
    
    # Print startup info
    port = PORTS['h2']
    print("\n" + "="*60)
    print(" Starting H2: The Flexibility Gap Evolution Dashboard")
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
