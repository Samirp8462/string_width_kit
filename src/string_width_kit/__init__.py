"""Terminal column width calculation for monospace text.

This package exposes a small, dependency-free API for measuring how many
terminal cells a string occupies when rendered in a monospace font.  It
handles East Asian wide characters and ignores zero-width combining marks.
"""

from .core import string_width, char_width, is_wide, is_zero_width

__all__ = ["string_width", "char_width", "is_wide", "is_zero_width"]
