"""Core width logic for :mod:`string_width_kit`.

The implementation deliberately avoids third-party Unicode tables.  Instead
it uses the standard library's :mod:`unicodedata` module, which is present in
all supported Python versions and ships with the interpreter.  The trade-off is
that width classification follows the Unicode version bundled with the running
interpreter; that is the interpretation this library documents and tests.
"""

from __future__ import annotations

import unicodedata

__all__ = ["string_width", "char_width", "is_wide", "is_zero_width"]


def is_zero_width(ch: str) -> bool:
    """Return ``True`` if *ch* occupies no terminal cells.

    Combining marks, enclosing marks, and format characters are invisible when
the terminal renders the base character.  This function treats them as zero
width so callers do not have to strip them before measuring.
    """
    if not ch:
        return False
    return unicodedata.category(ch) in {"Mn", "Me", "Cf"}


def is_wide(ch: str) -> bool:
    """Return ``True`` if *ch* occupies two terminal cells.

    East Asian Wide (W) and Fullwidth (F) characters are the two categories
    that require two cells in a monospace terminal.  Ambiguous characters are
    intentionally treated as narrow, matching the common default in terminals
    that do not switch to a CJK locale.
    """
    if not ch:
        return False
    return unicodedata.east_asian_width(ch) in {"W", "F"}


def char_width(ch: str) -> int:
    """Return the number of terminal cells occupied by a single character.

    Raises :class:`ValueError` if *ch* is not exactly one character.  Callers
    that need to iterate over a string should use :func:`string_width`.
    """
    if len(ch) != 1:
        raise ValueError("char_width expects exactly one character")
    if is_zero_width(ch):
        return 0
    if is_wide(ch):
        return 2
    return 1


def string_width(text: str) -> int:
    """Return the total terminal column width of *text*.

    The result is the sum of :func:`char_width` over every character.  Control
    characters such as newline and tab are not given special treatment; they
    are counted with their natural width (zero for combining marks and format
    characters, one for most others).  Callers measuring a single logical line
    should pass a string that does not contain newlines.
    """
    total = 0
    for ch in text:
        total += char_width(ch)
    return total
