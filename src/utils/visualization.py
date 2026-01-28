"""
Visualization Utilities

This module provides functions for setting up and creating visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional


def setup_plotting_style(
    style: str = 'whitegrid',
    context: str = 'notebook',
    font_scale: float = 1.2,
    palette: str = 'deep'
) -> None:
    """
    Configure the default plotting style.
    
    Args:
        style: Seaborn style name
        context: Seaborn context for scaling
        font_scale: Font scaling factor
        palette: Color palette name
    """
    sns.set_style(style)
    sns.set_context(context, font_scale=font_scale)
    sns.set_palette(palette)
    
    # Additional matplotlib configurations
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    
    print("🎨 Plotting style configured")


def create_figure(
    nrows: int = 1,
    ncols: int = 1,
    figsize: Optional[Tuple[int, int]] = None,
    squeeze: bool = True
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a figure with subplots.
    
    Args:
        nrows: Number of rows of subplots
        ncols: Number of columns of subplots
        figsize: Figure size (width, height)
        squeeze: If True, squeeze extra dimensions
        
    Returns:
        Tuple of (Figure, Axes)
    """
    if figsize is None:
        figsize = (6 * ncols, 4 * nrows)
    
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=squeeze)
    return fig, axes


def save_figure(
    fig: plt.Figure,
    path: str,
    dpi: int = 300,
    transparent: bool = False
) -> None:
    """
    Save a figure to disk.
    
    Args:
        fig: Matplotlib figure to save
        path: Output file path
        dpi: Resolution in dots per inch
        transparent: Whether to use transparent background
    """
    fig.savefig(path, dpi=dpi, bbox_inches='tight', transparent=transparent)
    print(f"📊 Figure saved to {path}")
