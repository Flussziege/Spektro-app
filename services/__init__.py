"""Services package exports for the Spectro app."""

from .plotly_nmr import make_interactive_1h_plot
from .plotly_spectra import make_interactive_ir_plot

__all__ = [
    "make_interactive_1h_plot",
    "make_interactive_ir_plot",
]
