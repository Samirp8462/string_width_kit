# string_width_kit

Measure the terminal column width of text in a monospace font, accounting for
wide East Asian glyphs and invisible combining characters.

```python
from string_width_kit import string_width, char_width

string_width("hello")          # 5
string_width("\u4e2d\u6587")   # 4  (two wide glyphs)
string_width("e\u0301")        # 1  (combining acute adds no cell)
char_width("\u4e2d")           # 2
```

## Why this exists

Terminals do not lay out text by counting code points.  A CJK ideograph takes
two cells, a combining accent takes none, and most Latin letters take one.
Getting this wrong makes aligned columns drift and progress bars wrap.

The trade-off here is that width classification uses the Unicode tables built
into the running Python interpreter via `unicodedata`, rather than a vendored,
version-pinned table.  That keeps the library dependency-free and small, but the
answer for a newly assigned code point depends on your Python version.  East
Asian Ambiguous characters are treated as one cell, which is the common default
in terminals that do not switch to a CJK locale.

## API

- `string_width(text: str) -> int` — total column width of `text`.
- `char_width(ch: str) -> int` — width of one character; raises `ValueError`
  if `ch` is not exactly one character.
- `is_wide(ch: str) -> bool` — true for East Asian Wide and Fullwidth.
- `is_zero_width(ch: str) -> bool` — true for combining, enclosing, and format
  characters.

## The awkward edge

Control characters are not special-cased.  A newline or tab is counted with its
natural width (one), not as zero or as a tab stop.  Measure one logical line at
a time, or strip control characters yourself first.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

