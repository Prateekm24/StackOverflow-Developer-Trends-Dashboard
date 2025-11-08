"""
Configuration settings for the Stack Overflow Dashboard project.
Update the CSV_FILE path to match your local setup.
"""
from pathlib import Path

# ========== DATA CONFIGURATION ==========
# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Path to the dataset
CSV_FILE = project_root.parent / "dataset" / "stackoverflow_harmonized_core_all.csv"

# ========== SERVER CONFIGURATION ==========
# Ports for each hypothesis dashboard
PORTS = {
    'h1a': 8050,
    'h1b': 8051,
    'h2': 8052,
    'h3': 8053,
    'h4': 8054,
    'h5': 8055,
    'h6a': 8056,
    'h6b': 8057
}

HOST = '127.0.0.1'

# ========== COLOR SCHEMES ==========
# Color schemes for visualizations
WORK_MODE_COLORS = {
    'remote': '#45B7D1',      # Blue = freedom/flexibility
    'hybrid': '#FFA07A',      # Orange = middle ground
    'on_site': '#95A5A6',     # Gray = traditional/legacy
    'other': '#D3D3D3'        # Light gray
}

# Period colors (for H3 pre/post COVID comparison)
PERIOD_COLORS = {
    'Pre-COVID': '#3498db',
    'Post-COVID': '#e74c3c'
}

# Alternative color map for different visualizations
ALTERNATIVE_COLORS = {
    'Overall Average': '#BDC3C7',
    'Selected Filter': '#3498DB'
}

FRAMEWORK_COHORT_COLORS = {
    'Front-End': '#1f77b4',
    'Back-End': '#ff7f0e', 
    'Other': '#2ca02c',
    'All': '#9467bd'
}

# ========== DISPLAY SETTINGS ==========
# Default chart heights
CHART_HEIGHTS = {
    'main': '500px',
    'summary': '600px',
    'detail': '400px'
}

# ========== COVID-19 MARKER ==========
COVID_YEAR = 2020

# ========== FRAMEWORK COHORT CLASSIFICATION ==========
# Add framework cohort classification
FRONT_END_FRAMEWORKS = {"React", "Angular", "Vue.js", "Svelte", "Ember.js", "Next.js", "Nuxt.js"}
BACK_END_FRAMEWORKS = {"Django", "Flask", "Spring", "Express", "Laravel", "FastAPI", "Ruby on Rails", "ASP.NET", "ASP.NET Core"}