import unittest

from src.gui.calculations import DIGIT_ERROR, ERROR_TITLE, multiplication, roman_sum


class RomanSumOutcomeTests(unittest.TestCase):
    def test_shows_numeral_and_detail(self) -> None:
        outcome = roman_sum(" xiv ", "IX")
        self.assertEqual(outcome.value, "XXIII")
        self.assertEqual(outcome.detail, "XIV + IX = 23")
        self.assertFalse(outcome.is_error)

    def test_invalid_numeral_becomes_error(self) -> None:
        outcome = roman_sum("IIII", "I")
        self.assertTrue(outcome.is_error)
        self.assertEqual(outcome.value, ERROR_TITLE)
        self.assertIn("IIII", outcome.detail)

    def test_empty_field_becomes_error(self) -> None:
        self.assertTrue(roman_sum("", "I").is_error)

    def test_sum_above_limit_becomes_error(self) -> None:
        outcome = roman_sum("MM", "MM")
        self.assertTrue(outcome.is_error)
        self.assertIn("3999", outcome.detail)


class MultiplicationOutcomeTests(unittest.TestCase):
    def test_shows_repeated_addition(self) -> None:
        outcome = multiplication("7", "4")
        self.assertEqual(outcome.value, "28")
        self.assertEqual(outcome.detail, "7 × 4 = 7 + 7 + 7 + 7")

    def test_zero_multiplier_has_no_additions(self) -> None:
        outcome = multiplication("8", "0")
        self.assertEqual(outcome.value, "0")
        self.assertEqual(outcome.detail, "8 × 0 = sin sumas (factor cero)")

    def test_non_numeric_text_becomes_error(self) -> None:
        for text in ("", "a", "7.5"):
            with self.subTest(text=text):
                outcome = multiplication(text, "2")
                self.assertTrue(outcome.is_error)
                self.assertEqual(outcome.detail, DIGIT_ERROR)

    def test_out_of_range_becomes_error(self) -> None:
        for first, second in (("10", "2"), ("3", "-1")):
            with self.subTest(first=first, second=second):
                self.assertTrue(multiplication(first, second).is_error)


if __name__ == "__main__":
    unittest.main()
