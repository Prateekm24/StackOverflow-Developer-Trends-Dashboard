"""Data processing utilities for canonicalization and cleaning."""
import pandas as pd


def canon_mode(s):
    """
    Canonicalize work mode values to standard format.
    
    Args:
        s: Work mode string value
        
    Returns:
        Canonicalized work mode string
    """
    if pd.isna(s):
        return s
    s = str(s).strip().lower()
    return {
        "onsite": "on_site",
        "on-site": "on_site",
        "office": "on_site",
        "on_site": "on_site",
        "hybrid": "hybrid",
        "remote": "remote",
        "fully remote": "remote"
    }.get(s, s)


def clean_company_size(size_str):
    """
    Clean up company size encoding issues with dashes.
    
    Args:
        size_str: Company size string with potential encoding issues
        
    Returns:
        Cleaned company size string
    """
    if pd.isna(size_str):
        return size_str
    # Fix various dash encodings (em dash, en dash, etc.)
    size_str = str(size_str).replace('â€"', '-').replace('–', '-').replace('—', '-').replace('�', '-')
    return size_str.strip()


def sorted_company_sizes(sizes):
    """
    Sort company sizes by actual size order.
    
    Args:
        sizes: List of company size strings
        
    Returns:
        Sorted list of company sizes
    """
    size_order = {
        '1-9': 1,
        '10-99': 2,
        '100-999': 3,
        '1000+': 4
    }
    
    # Handle variations and return sorted
    cleaned_sizes = [clean_company_size(s) for s in sizes]
    return sorted(cleaned_sizes, key=lambda x: size_order.get(x, 999))
