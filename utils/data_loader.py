"""Data loading utilities for Stack Overflow survey data."""
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import CSV_FILE
from utils.data_processing import canon_mode, clean_company_size, sorted_company_sizes


def load_and_process_data(clean_size_column=False, verbose=True):
    """
    Load and process the Stack Overflow survey CSV file.
    
    Args:
        clean_size_column: Whether to clean the company_size column
        verbose: Whether to print loading information
        
    Returns:
        Processed pandas DataFrame
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns are missing
    """
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    if verbose:
        print(f"Loading data from: {CSV_FILE}")
    
    df = pd.read_csv(CSV_FILE, low_memory=False)

    # Ensure year column is integer
    if "year" not in df.columns:
        raise ValueError("'year' column not found in the CSV file")
    
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype('Int64')

    # Canonicalize work_mode
    if "work_mode" in df.columns:
        df["work_mode"] = df["work_mode"].map(canon_mode)

    # Clean company_size column if requested (for H2)
    if clean_size_column and "company_size" in df.columns:
        df["company_size"] = df["company_size"].apply(clean_company_size)

    if verbose:
        print(f"Loaded {df.shape[0]:,} rows")
        print(f"Columns: {', '.join(df.columns.tolist()[:15])}{'...' if len(df.columns) > 15 else ''}")
        print(f"Years: {sorted(df['year'].dropna().unique().tolist())}")
        
        # Print data coverage summary if company_size exists
        if "company_size" in df.columns:
            sizes = df['company_size'].dropna().unique()
            print(f"Company sizes: {len(sizes)} categories")
            if clean_size_column:
                print(f"  Sizes: {', '.join(sorted_company_sizes(sizes))}")
        
        # Check for hybrid detail columns (for H1B)
        hybrid_cols = [col for col in df.columns if 'hybrid' in col.lower() or 'flex' in col.lower()]
        if hybrid_cols:
            print(f"Hybrid-related columns found: {', '.join(hybrid_cols)}")

    return df


def load_data_for_h1a():
    """Load data specifically for H1A hypothesis (no special processing)."""
    return load_and_process_data(clean_size_column=False)


def load_data_for_h1b():
    """Load data specifically for H1B hypothesis."""
    return load_and_process_data(clean_size_column=False)


def load_data_for_h2():
    """Load data specifically for H2 hypothesis (with company size cleaning)."""
    return load_and_process_data(clean_size_column=True)


def load_data_for_h3():
    """Load data specifically for H3 hypothesis (with job satisfaction processing)."""
    df = load_and_process_data(clean_size_column=False, verbose=True)
    
    # Ensure job_satisfaction is numeric
    if "job_satisfaction" in df.columns:
        df["job_satisfaction"] = pd.to_numeric(df["job_satisfaction"], errors="coerce")
        
        valid_satisfaction = df['job_satisfaction'].notna().sum()
        print(f"Job satisfaction data: {valid_satisfaction:,} valid entries")
        if valid_satisfaction > 0:
            print(f"  Range: {df['job_satisfaction'].min():.1f} - {df['job_satisfaction'].max():.1f}")
    else:
        print("⚠ Warning: job_satisfaction column not found in dataset")
    
    return df
