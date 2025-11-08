"""Data processing utilities specific to H5: Programming Language Evolution."""
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


def calculate_language_shares(df):
    """
    Calculate language usage share by year.
    
    Args:
        df: DataFrame with year and language_worked_with columns (exploded)
        
    Returns:
        DataFrame with columns: year, language_worked_with, count, share
    """
    # Count occurrences by year and language
    lang_counts = (
        df.groupby(["year", "language_worked_with"])
        .size()
        .reset_index(name="count")
    )
    
    # Calculate total responses per year
    year_totals = (
        lang_counts.groupby("year")["count"]
        .sum()
        .rename("year_total")
    )
    
    # Merge and calculate share
    lang_counts = lang_counts.merge(year_totals, on="year", how="left")
    lang_counts["share"] = (lang_counts["count"] / lang_counts["year_total"]) * 100
    
    return lang_counts


def get_top_languages(lang_counts, n=12):
    """
    Get the top N languages by total mentions across all years.
    
    Args:
        lang_counts: DataFrame with language counts
        n: Number of top languages to return
        
    Returns:
        List of top N language names
    """
    top_langs = (
        lang_counts.groupby("language_worked_with")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .index.tolist()
    )
    
    return top_langs


def prepare_language_data(df, verbose=True):
    """
    Complete pipeline to prepare language evolution data.
    
    Args:
        df: Raw DataFrame with year and language_worked_with columns
        verbose: Whether to print progress information
        
    Returns:
        Tuple of (lang_counts_df, top_languages_list)
    """
    if verbose:
        print("\nPreparing language data...")
    
    # Filter to rows with year and language data
    lang_df = df[["year", "language_worked_with"]].dropna(subset=["year"]).copy()
    
    if verbose:
        print(f"  • Starting with {len(lang_df):,} rows")
    
    # Explode multi-value language column
    lang_df = explode_multi_value_column(lang_df, "language_worked_with")
    
    if verbose:
        print(f"  • After exploding: {len(lang_df):,} language mentions")
        print(f"  • Unique languages: {lang_df['language_worked_with'].nunique()}")
    
    # Calculate shares
    lang_counts = calculate_language_shares(lang_df)
    
    # Get top languages
    top_langs = get_top_languages(lang_counts, n=12)
    
    if verbose:
        print(f"  • Top 12 languages: {', '.join(top_langs[:5])}...")
    
    # Filter to top languages
    lang_top = lang_counts[lang_counts["language_worked_with"].isin(top_langs)].copy()
    
    if verbose:
        print(f"✓ Language data prepared: {len(lang_top):,} records")
    
    return lang_top, top_langs
