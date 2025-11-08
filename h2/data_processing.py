"""H2-specific data processing functions."""
import pandas as pd
import plotly.express as px


def calculate_flexibility_by_size_year(df):
    """
    Calculate flexibility percentage (remote + hybrid) by company size and year.
    
    Args:
        df: DataFrame with year, company_size, and work_mode columns
        
    Returns:
        DataFrame with Year, Company Size, Flexibility %, Count, and Total columns
    """
    if 'company_size' not in df.columns:
        return pd.DataFrame()
    
    flex_data = []
    
    for year in sorted(df['year'].dropna().unique()):
        year_data = df[df['year'] == year]
        
        for size in year_data['company_size'].dropna().unique():
            size_data = year_data[year_data['company_size'] == size]
            total = len(size_data[size_data['work_mode'].notna()])
            flexible_count = len(size_data[size_data['work_mode'].isin(['remote', 'hybrid'])])
            flexibility_pct = (flexible_count / total * 100) if total > 0 else 0
            
            flex_data.append({
                'Year': int(year),
                'Company Size': str(size),
                'Flexibility %': flexibility_pct,
                'Count': flexible_count,
                'Total': total
            })
    
    return pd.DataFrame(flex_data) if flex_data else pd.DataFrame()


def generate_size_colors(sizes):
    """
    Generate distinct colors for each company size.
    
    Args:
        sizes: List of company size strings
        
    Returns:
        Dictionary mapping size to color
    """
    colors = px.colors.qualitative.Set2 + px.colors.qualitative.Pastel
    return {str(size): colors[i % len(colors)] for i, size in enumerate(sizes)}


def calculate_flexibility_gap(df, year):
    """
    Calculate the flexibility gap (max - min) for a specific year.
    
    Args:
        df: DataFrame with flexibility data
        year: Year to calculate gap for
        
    Returns:
        Gap value in percentage points, or None if insufficient data
    """
    year_data = df[df['Year'] == year]
    
    if len(year_data) < 2:
        return None
    
    max_flex = year_data['Flexibility %'].max()
    min_flex = year_data['Flexibility %'].min()
    
    return max_flex - min_flex
