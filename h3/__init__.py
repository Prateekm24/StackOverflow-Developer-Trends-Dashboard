"""H3: The Flexibility Dividend Dashboard module."""
from .layout import create_layout
from .callbacks import register_callbacks
from .data_processing import (
    get_satisfaction_stats,
    calculate_satisfaction_change,
    prepare_comparison_data,
    calculate_all_mode_changes
)

__all__ = [
    'create_layout',
    'register_callbacks',
    'get_satisfaction_stats',
    'calculate_satisfaction_change',
    'prepare_comparison_data',
    'calculate_all_mode_changes'
]
