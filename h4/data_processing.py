"""Data processing utilities specific to H4: Experience vs Compensation."""
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def clip_compensation(df, lower_percentile=0.01, upper_percentile=0.99):
    """
    Clip compensation values to remove extreme outliers.
    
    Args:
        df: DataFrame with compensation_annual column
        lower_percentile: Lower percentile for clipping (default 1%)
        upper_percentile: Upper percentile for clipping (default 99%)
        
    Returns:
        DataFrame with comp_clipped column added
    """
    if "compensation_annual" not in df.columns:
        raise ValueError("compensation_annual column not found")
    
    # Convert to numeric
    df["compensation_annual"] = pd.to_numeric(df["compensation_annual"], errors="coerce")
    
    # Calculate percentiles
    low_q = df["compensation_annual"].quantile(lower_percentile)
    high_q = df["compensation_annual"].quantile(upper_percentile)
    
    # Clip values
    df["comp_clipped"] = df["compensation_annual"].clip(lower=low_q, upper=high_q)
    
    return df


def prepare_experience_compensation_data(df, year, work_modes=None, company_sizes=None):
    """
    Prepare data for experience vs compensation analysis.
    
    Args:
        df: Source DataFrame
        year: Year to filter
        work_modes: List of work modes to include (None = all)
        company_sizes: List of company sizes to include (None = all)
        
    Returns:
        Filtered DataFrame ready for plotting
    """
    # Filter by year
    dff = df[df["year"] == year].copy()
    
    # Apply work mode filter
    if work_modes:
        dff = dff[dff["work_mode"].isin(work_modes)]
    
    # Apply company size filter
    if company_sizes:
        dff = dff[dff["company_size"].isin(company_sizes)]
    
    # Keep only rows with valid experience and compensation data
    dff = dff.dropna(subset=["experience_years_code_pro", "comp_clipped"])
    
    return dff


def get_valid_years_for_analysis(df):
    """
    Get years that have sufficient data for experience vs compensation analysis.
    
    Args:
        df: Source DataFrame
        
    Returns:
        Tuple of (all_years, valid_years) where valid_years have experience and compensation data
    """
    # All years in dataset
    all_years = sorted(df["year"].dropna().unique().tolist())
    
    # Years with both experience and compensation data
    valid_years = sorted(
        df.loc[
            df["experience_years_code_pro"].notna() & 
            df["compensation_annual"].notna(), 
            "year"
        ].dropna().unique().tolist()
    )
    
    return all_years, valid_years
