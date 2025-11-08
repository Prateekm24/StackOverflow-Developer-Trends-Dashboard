"""
Run the H6b: Framework Lifecycles dashboard.

This script initializes and runs the H6b hypothesis dashboard on port 8058.

Usage:
    python h6b/run_h6b.py
    
Then open: http://127.0.0.1:8058
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
from h6b.layout import create_layout
from h6b.callbacks import register_callbacks
from h6b.data_processing import prepare_framework_lifecycle_data


def main():
    """Initialize and run the H6b dashboard."""
    print("\n" + "="*70)
    print("H6b: FRAMEWORK LIFECYCLES ANALYSIS (ENTRY & PEAK)")
    print("="*70 + "\n")
    
    # Load and process data
    print("Loading data...")
    df = load_and_process_data(clean_size_column=False, verbose=True)
    
    # Validate required columns
    required_cols = ["year", "framework_worked_with"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Prepare framework lifecycle data
    fw_data, lifecycle_stats = prepare_framework_lifecycle_data(df, verbose=True)
    
    # Get available frameworks
    available_frameworks = sorted(fw_data["framework_worked_with"].unique().tolist())
    
    # Set default selection (first 5 frameworks)
    default_selection = sorted(available_frameworks)[:5]
    print(f"✓ Default selection: {', '.join(default_selection)}")
    print(f"✓ Total frameworks available: {len(available_frameworks)}")
    
    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "H6b – Framework Lifecycles"
    
    # Create layout
    app.layout = create_layout(
        available_frameworks=available_frameworks,
        default_selection=default_selection
    )
    
    # Register callbacks
    register_callbacks(app, fw_data, lifecycle_stats)
    
    # Schedule browser to open
    port = PORTS['h6b']
    #schedule_browser_open(port, delay=1.5)
    
    # Run server
    print(f"\n{'='*70}")
    print(f" Starting H6b dashboard on http://127.0.0.1:{port}")
    print(f"{'='*70}\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    main()
