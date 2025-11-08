"""
Run the H4: Experience vs Compensation dashboard.

This script initializes and runs the H4 hypothesis dashboard on port 8055.

Usage:
    python h4/run_h4.py
    
Then open: http://127.0.0.1:8055
"""
import sys
from pathlib import Path
import dash
import dash_bootstrap_components as dbc

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import PORTS, WORK_MODE_COLORS
from utils.data_loader import load_and_process_data
from utils.browser_utils import schedule_browser_open
from h4.layout import create_layout
from h4.callbacks import register_callbacks
from h4.data_processing import clip_compensation, get_valid_years_for_analysis


def main():
    """Initialize and run the H4 dashboard."""
    print("\n" + "="*70)
    print("H4: EXPERIENCE VS COMPENSATION ANALYSIS")
    print("="*70 + "\n")
    
    # Load and process data
    print("Loading data...")
    df = load_and_process_data(clean_size_column=False, verbose=True)
    
    # Validate required columns
    required_cols = ["year", "work_mode", "company_size", "compensation_annual", 
                     "experience_years_code_pro", "job_satisfaction"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Process compensation data (clip outliers)
    print("\nProcessing compensation data...")
    df = clip_compensation(df, lower_percentile=0.01, upper_percentile=0.99)
    print(f"✓ Compensation clipped at 1st-99th percentiles")
    
    # Get valid years for analysis
    years_all, years_valid = get_valid_years_for_analysis(df)
    default_year = int(years_valid[-1] if years_valid else years_all[-1])
    
    print(f"✓ Years with valid data: {len(years_valid)}")
    print(f"✓ Default year: {default_year}")
    
    # Get available work modes and company sizes
    work_modes = df["work_mode"].dropna().unique().tolist()
    company_sizes = df["company_size"].dropna().unique().tolist()
    
    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "H4 – Experience vs Compensation"
    
    # Create layout
    app.layout = create_layout(
        df=df,
        years_all=years_all,
        years_valid=years_valid,
        default_year=default_year,
        work_modes=work_modes,
        company_sizes=company_sizes
    )
    
    # Register callbacks
    register_callbacks(app, df, WORK_MODE_COLORS)
    
    # Schedule browser to open
    port = PORTS['h4']
    # schedule_browser_open(port, delay=1.5)
    
    # Run server
    print(f"\n{'='*70}")
    print(f" Starting H4 dashboard on http://127.0.0.1:{port}")
    print(f"{'='*70}\n")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    main()
