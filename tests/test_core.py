import unittest

from string_width_kit import char_width, is_wide, is_zero_width, string_width


class TestCharWidth(unittest.TestCase):
    def test_ascii_letter_is_one(self):
        self.assertEqual(char_width("a"), 1)

    def test_space_is_one(self):
        self.assertEqual(char_width(" "), 1)

    def test_combining_acute_is_zero(self):
        # U+0301 COMBINING ACUTE ACCENT
        self.assertEqual(char_width("\u0301"), 0)

    def test_zero_width_joiner_is_zero(self):
        # U+200D ZERO WIDTH JOINER
        self.assertEqual(char_width("\u200d"), 0)

    def test_cjk_ideograph_is_two(self):
        self.assertEqual(char_width("\u4e2d"), 2)

    def test_fullwidth_latin_is_two(self):
        self.assertEqual(char_width("\uff21"), 2)

    def test_ambiguous_is_narrow(self):
        # U+00B1 PLUS-MINUS SIGN is East Asian Ambiguous; we treat it as one.
        self.assertEqual(char_width("\u00b1"), 1)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            char_width("")

    def test_rejects_multiple_characters(self):
        with self.assertRaises(ValueError):
            char_width("ab")


class TestPredicates(unittest.TestCase):
    def test_is_wide_for_cjk(self):
        self.assertTrue(is_wide("\u4e2d"))

    def test_is_wide_false_for_ascii(self):
        self.assertFalse(is_wide("a"))

    def test_is_wide_empty_is_false(self):
        self.assertFalse(is_wide(""))

    def test_is_zero_width_for_combining(self):
        self.assertTrue(is_zero_width("\u0301"))

    def test_is_zero_width_false_for_ascii(self):
        self.assertFalse(is_zero_width("a"))

    def test_is_zero_width_empty_is_false(self):
        self.assertFalse(is_zero_width(""))


class TestStringWidth(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(string_width(""), 0)

    def test_pure_ascii(self):
        self.assertEqual(string_width("hello"), 5)

    def test_mixed_ascii_and_cjk(self):
        self.assertEqual(string_width("a\u4e2db"), 4)

    def test_combining_mark_does_not_add_width(self):
        # "e" followed by a combining acute accent is one cell wide.
        self.assertEqual(string_width("e\u0301"), 1)

    def test_multiple_combining_marks(self):
        self.assertEqual(string_width("a\u0301\u0302"), 1)

    def test_fullwidth_string(self):
        self.assertEqual(string_width("\uff21\uff22"), 4)

    def test_mixed_with_zero_width_joiner(self):
        # ZWJ sequences still count base characters; the joiner itself is zero.
        self.assertEqual(string_width("\U0001f468\u200d\U0001f469"), 4)

    def test_newline_counts_as_one(self):
        # We document that control characters are counted with their natural
        # width rather than special-cased.  Newline is not zero-width.
        self.assertEqual(string_width("a\nb"), 3)

    def test_tab_counts_as_one(self):
        self.assertEqual(string_width("\t"), 1)


if __name__ == "__main__":
    unittest.main()
