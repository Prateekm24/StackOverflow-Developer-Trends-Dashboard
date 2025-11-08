"""
Setup script to ensure proper Python path configuration.
Run this once before running any dashboard, or import it in each run script.
"""
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Add to Python path if not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f" Added {project_root} to Python path")

# Verify imports work
try:
    from config import CSV_FILE
    from utils import data_loader
    print(" Import paths configured successfully")
except ImportError as e:
    print(f" Import error: {e}")
    print(f"  Please ensure you're running from the project root: {project_root}")
