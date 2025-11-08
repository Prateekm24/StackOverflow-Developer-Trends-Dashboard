"""Data processing utilities specific to H6b: Framework Lifecycles."""
import pandas as pd
import re
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def explode_multi_value_column(df, column_name):
    """
    Explode a column containing multiple delimited values into separate rows.
    
    Handles various delimiters: semicolon, comma, pipe, forward slash.
    
    Args:
        df: DataFrame with multi-value column
        column_name: Name of column to explode
        
    Returns:
        DataFrame with one row per value
    """
    out = df.copy()
    
    # Fill NaN and convert to string
    out[column_name] = out[column_name].fillna("").astype(str)
    
    # Split on common delimiters and clean
    out[column_name] = out[column_name].apply(
        lambda s: [x.strip() for x in re.split(r";|,|\||/", s) if x.strip()] if s else []
    )
    
    # Explode the list into separate rows
    out = out.explode(column_name)
    
    # Remove empty values
    out = out[out[column_name].notna() & (out[column_name] != "")]
    
    return out


def calculate_framework_shares(df):
    """
    Calculate framework usage share by year.
    
    Args:
        df: DataFrame with year and framework_worked_with columns (exploded)
        
    Returns:
        DataFrame with columns: year, framework_worked_with, count, share
    """
    # Count occurrences by year and framework
    fw_counts = (
        df.groupby(["year", "framework_worked_with"])
        .size()
        .reset_index(name="count")
    )
    
    # Calculate total responses per year
    year_totals = (
        fw_counts.groupby("year")["count"]
        .sum()
        .rename("year_total")
    )
    
    # Merge and calculate share
    fw_counts = fw_counts.merge(year_totals, on="year", how="left")
    fw_counts["share"] = (fw_counts["count"] / fw_counts["year_total"]) * 100
    
    return fw_counts


def calculate_lifecycle_statistics(fw_counts):
    """
    Calculate lifecycle statistics for each framework.
    
    For each framework, calculates:
    - First year of appearance
    - Peak year (year with highest share)
    - Peak share percentage
    
    Args:
        fw_counts: DataFrame with framework counts and shares
        
    Returns:
        DataFrame with lifecycle statistics
    """
    lifecycle_stats = []
    
    for framework, group in fw_counts.groupby("framework_worked_with"):
        # Sort by year
        group_sorted = group.sort_values("year")
        
        # First year of appearance
        first_year = int(group_sorted["year"].min())
        
        # Find peak year and share
        peak_idx = group_sorted["share"].idxmax()
        peak_year = int(group_sorted.loc[peak_idx, "year"])
        peak_share = float(group_sorted.loc[peak_idx, "share"])
        
        lifecycle_stats.append({
            "framework": framework,
            "first_year": first_year,
            "peak_year": peak_year,
            "peak_share": peak_share
        })
    
    return pd.DataFrame(lifecycle_stats)


def prepare_framework_lifecycle_data(df, verbose=True):
    """
    Complete pipeline to prepare framework lifecycle data.
    
    Args:
        df: Raw DataFrame with year and framework_worked_with columns
        verbose: Whether to print progress information
        
    Returns:
        Tuple of (fw_counts_df, lifecycle_stats_df)
    """
    if verbose:
        print("\nPreparing framework lifecycle data...")
    
    # Filter to rows with year and framework data
    fw_df = df[["year", "framework_worked_with"]].dropna(subset=["year"]).copy()
    
    if verbose:
        print(f"  • Starting with {len(fw_df):,} rows")
    
    # Explode multi-value framework column
    fw_df = explode_multi_value_column(fw_df, "framework_worked_with")
    
    if verbose:
        print(f"  • After exploding: {len(fw_df):,} framework mentions")
        print(f"  • Unique frameworks: {fw_df['framework_worked_with'].nunique()}")
    
    # Calculate shares
    fw_counts = calculate_framework_shares(fw_df)
    
    # Calculate lifecycle statistics
    lifecycle_stats = calculate_lifecycle_statistics(fw_counts)
    
    if verbose:
        print(f"  • Lifecycle stats calculated for {len(lifecycle_stats)} frameworks")
        
        # Show some example stats
        top_by_peak = lifecycle_stats.nlargest(3, "peak_share")
        print(f"  • Top 3 frameworks by peak share:")
        for _, row in top_by_peak.iterrows():
            print(f"    - {row['framework']}: {row['peak_share']:.2f}% in {row['peak_year']}")
    
    if verbose:
        print(f"✓ Framework lifecycle data prepared")
    
    return fw_counts, lifecycle_stats
