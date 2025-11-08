"""
Run the H5: Programming Language Evolution dashboard.

This script initializes and runs the H5 hypothesis dashboard on port 8056.

Usage:
    python h5/run_h5.py
    
Then open: http://127.0.0.1:8056
"""
import sys
from pathlib import Path
import dash
import dash_bootstrap_components as dbc

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import PORTS
from utils.data_loader import load_and_process_data
from utils.browser_utils import schedule_browser_open
from h5.layout import create_layout
from h5.callbacks import register_callbacks
from h5.data_processing import prepare_language_data


def main():
    """Initialize and run the H5 dashboard."""
    print("\n" + "="*70)
    print("H5: PROGRAMMING LANGUAGE EVOLUTION ANALYSIS")
    print("="*70 + "\n")
    
    # Load and process data
    print("Loading data...")
    df = load_and_process_data(clean_size_column=False, verbose=True)
    
    # Validate required columns
    required_cols = ["year", "language_worked_with"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Prepare language evolution data
    lang_data, top_languages = prepare_language_data(df, verbose=True)
    
    # Set default selection (first 6 languages)
    default_selection = sorted(top_languages)[:6]
    print(f"✓ Default selection: {', '.join(default_selection)}")
    
    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "H5 – Programming Language Evolution"
    
    # Create layout
    app.layout = create_layout(
        available_languages=top_languages,
        default_selection=default_selection
    )
    
    # Register callbacks
    register_callbacks(app, lang_data)
    
    # Schedule browser to open
    port = PORTS['h5']
    #schedule_browser_open(port, delay=1.5)
    
    # Run server
    print(f"\n{'='*70}")
    print(f" Starting H5 dashboard on http://127.0.0.1:{port}")
    print(f"{'='*70}\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    main()
