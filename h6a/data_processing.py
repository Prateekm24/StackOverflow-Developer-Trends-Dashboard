"""Data processing utilities specific to H6a: Framework Cohorts."""
import pandas as pd
import re
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import FRONT_END_FRAMEWORKS, BACK_END_FRAMEWORKS


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


def classify_framework_cohort(framework_name):
    """
    Classify a framework into Front-End, Back-End, or Other cohort.
    
    Args:
        framework_name: Name of the framework
        
    Returns:
        Cohort string: "Front-End", "Back-End", or "Other"
    """
    if not framework_name:
        return "Other"
    
    # Normalize for comparison
    name_lower = framework_name.strip().lower()
    
    # Check Front-End frameworks
    if name_lower in {x.lower() for x in FRONT_END_FRAMEWORKS}:
        return "Front-End"
    
    # Check Back-End frameworks
    if name_lower in {x.lower() for x in BACK_END_FRAMEWORKS}:
        return "Back-End"
    
    return "Other"


def calculate_framework_shares(df):
    """
    Calculate framework usage share by year.
    
    Args:
        df: DataFrame with year and framework_worked_with columns (exploded)
        
    Returns:
        DataFrame with columns: year, framework_worked_with, count, share, cohort
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
    
    # Add cohort classification
    fw_counts["cohort"] = fw_counts["framework_worked_with"].apply(classify_framework_cohort)
    
    return fw_counts


def get_top_frameworks_by_cohort(fw_counts, cohort, n=8):
    """
    Get the top N frameworks for a specific cohort by total mentions.
    
    Args:
        fw_counts: DataFrame with framework counts and cohorts
        cohort: Cohort to filter ("Front-End", "Back-End", "Other", or "All")
        n: Number of top frameworks to return
        
    Returns:
        List of top N framework names for the cohort
    """
    # Filter by cohort if not "All"
    if cohort != "All":
        cohort_data = fw_counts[fw_counts["cohort"] == cohort]
    else:
        cohort_data = fw_counts
    
    # Get top frameworks by total mentions
    top_frameworks = (
        cohort_data.groupby("framework_worked_with")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )
    
    return top_frameworks


def prepare_framework_cohort_data(df, verbose=True):
    """
    Complete pipeline to prepare framework cohort data.
    
    Args:
        df: Raw DataFrame with year and framework_worked_with columns
        verbose: Whether to print progress information
        
    Returns:
        DataFrame with framework counts, shares, and cohort classifications
    """
    if verbose:
        print("\nPreparing framework cohort data...")
    
    # Filter to rows with year and framework data
    fw_df = df[["year", "framework_worked_with"]].dropna(subset=["year"]).copy()
    
    if verbose:
        print(f"  • Starting with {len(fw_df):,} rows")
    
    # Explode multi-value framework column
    fw_df = explode_multi_value_column(fw_df, "framework_worked_with")
    
    if verbose:
        print(f"  • After exploding: {len(fw_df):,} framework mentions")
        print(f"  • Unique frameworks: {fw_df['framework_worked_with'].nunique()}")
    
    # Calculate shares and classify cohorts
    fw_counts = calculate_framework_shares(fw_df)
    
    # Count cohorts
    cohort_counts = fw_counts.groupby("cohort")["framework_worked_with"].nunique()
    
    if verbose:
        print(f"  • Front-End frameworks: {cohort_counts.get('Front-End', 0)}")
        print(f"  • Back-End frameworks: {cohort_counts.get('Back-End', 0)}")
        print(f"  • Other frameworks: {cohort_counts.get('Other', 0)}")
        print(f"✓ Framework cohort data prepared: {len(fw_counts):,} records")
    
    return fw_counts
