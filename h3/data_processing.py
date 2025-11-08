"""H3-specific data processing functions for satisfaction analysis."""
import pandas as pd
import numpy as np


def get_satisfaction_stats(df, work_mode=None, period=None):
    """
    Calculate satisfaction statistics for a given work mode and/or period.
    
    Args:
        df: DataFrame with job_satisfaction and work_mode columns
        work_mode: Optional work mode to filter by ('remote', 'hybrid', 'on_site')
        period: Optional period to filter by ('pre' for 2017-2019, 'post' for 2024-2025)
        
    Returns:
        Dictionary with mean, median, std, count statistics
    """
    df_filtered = df.copy()
    
    # Filter by work mode
    if work_mode:
        df_filtered = df_filtered[df_filtered['work_mode'] == work_mode]
    
    # Filter by period
    if period == 'pre':
        df_filtered = df_filtered[(df_filtered['year'] >= 2017) & (df_filtered['year'] <= 2019)]
    elif period == 'post':
        df_filtered = df_filtered[(df_filtered['year'] >= 2024) & (df_filtered['year'] <= 2025)]
    
    # Calculate statistics
    satisfaction_data = df_filtered['job_satisfaction'].dropna()
    
    if len(satisfaction_data) == 0:
        return {
            'mean': 0,
            'median': 0,
            'std': 0,
            'count': 0,
            'min': 0,
            'max': 0
        }
    
    return {
        'mean': satisfaction_data.mean(),
        'median': satisfaction_data.median(),
        'std': satisfaction_data.std(),
        'count': len(satisfaction_data),
        'min': satisfaction_data.min(),
        'max': satisfaction_data.max()
    }


def calculate_satisfaction_change(df, work_mode):
    """
    Calculate the change in satisfaction from pre-COVID to post-COVID for a work mode.
    
    Args:
        df: DataFrame with job_satisfaction, work_mode, and year columns
        work_mode: Work mode to analyze ('remote', 'hybrid', 'on_site')
        
    Returns:
        Dictionary with pre, post, and change values
    """
    pre_stats = get_satisfaction_stats(df, work_mode=work_mode, period='pre')
    post_stats = get_satisfaction_stats(df, work_mode=work_mode, period='post')
    
    change = post_stats['mean'] - pre_stats['mean'] if (pre_stats['count'] > 0 and post_stats['count'] > 0) else 0
    
    return {
        'work_mode': work_mode,
        'pre_mean': pre_stats['mean'],
        'post_mean': post_stats['mean'],
        'change': change,
        'pre_count': pre_stats['count'],
        'post_count': post_stats['count']
    }


def get_period_label(period):
    """
    Get a human-readable label for a period code.
    
    Args:
        period: Period code ('pre', 'post', or 'both')
        
    Returns:
        Human-readable period label
    """
    period_labels = {
        'pre': 'Pre-COVID (2017-2019)',
        'post': 'Post-COVID (2024-2025)',
        'both': 'Pre vs Post-COVID'
    }
    return period_labels.get(period, 'All Years')


def prepare_comparison_data(df):
    """
    Prepare data for pre/post COVID comparison across all work modes.
    
    Args:
        df: DataFrame with job_satisfaction, work_mode, and year columns
        
    Returns:
        DataFrame with work mode, period, and satisfaction data
    """
    # Filter for pre and post COVID periods
    pre_covid = df[(df['year'] >= 2017) & (df['year'] <= 2019)].copy()
    post_covid = df[(df['year'] >= 2024) & (df['year'] <= 2025)].copy()
    
    # Add period labels
    pre_covid['Period'] = 'Pre-COVID'
    post_covid['Period'] = 'Post-COVID'
    
    # Combine
    comparison_df = pd.concat([pre_covid, post_covid], ignore_index=True)
    
    # Clean work mode labels
    comparison_df['Work Mode'] = comparison_df['work_mode'].str.replace('_', ' ').str.title()
    
    return comparison_df


def calculate_all_mode_changes(df):
    """
    Calculate satisfaction changes for all work modes.
    
    Args:
        df: DataFrame with job_satisfaction, work_mode, and year columns
        
    Returns:
        DataFrame with changes for each work mode
    """
    changes = []
    for mode in ['remote', 'hybrid', 'on_site']:
        change_data = calculate_satisfaction_change(df, mode)
        changes.append(change_data)
    
    return pd.DataFrame(changes)
