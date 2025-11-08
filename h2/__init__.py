"""H2: The Flexibility Gap Evolution Dashboard module."""
from .layout import create_layout
from .callbacks import register_callbacks
from .data_processing import (
    calculate_flexibility_by_size_year,
    generate_size_colors,
    calculate_flexibility_gap
)

__all__ = [
    'create_layout',
    'register_callbacks',
    'calculate_flexibility_by_size_year',
    'generate_size_colors',
    'calculate_flexibility_gap'
]
