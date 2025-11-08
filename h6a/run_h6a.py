"""
Run the H6a: Framework Cohorts dashboard.

This script initializes and runs the H6a hypothesis dashboard on port 8057.

Usage:
    python h6a/run_h6a.py
    
Then open: http://127.0.0.1:8057
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
from h6a.layout import create_layout
from h6a.callbacks import register_callbacks
from h6a.data_processing import prepare_framework_cohort_data


def main():
    """Initialize and run the H6a dashboard."""
    print("\n" + "="*70)
    print("H6a: FRAMEWORK COHORTS ANALYSIS (RISE & FALL)")
    print("="*70 + "\n")
    
    # Load and process data
    print("Loading data...")
    df = load_and_process_data(clean_size_column=False, verbose=True)
    
    # Validate required columns
    required_cols = ["year", "framework_worked_with"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Prepare framework cohort data
    fw_data = prepare_framework_cohort_data(df, verbose=True)
    
    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "H6a – Framework Cohorts"
    
    # Create layout
    app.layout = create_layout()
    
    # Register callbacks
    register_callbacks(app, fw_data)
    
    # Schedule browser to open
    port = PORTS['h6a']
    #schedule_browser_open(port, delay=1.5)
    
    # Run server
    print(f"\n{'='*70}")
    print(f" Starting H6a dashboard on http://127.0.0.1:{port}")
    print(f"{'='*70}\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    main()
