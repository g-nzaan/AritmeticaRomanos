import unittest

from src.core.multiplication import multiply_by_addition
from src.core.roman import add_roman, from_roman, to_roman


class RomanArithmeticTests(unittest.TestCase):
    def test_adds_roman_numerals(self) -> None:
        self.assertEqual(add_roman("XIV", "ix"), (23, "XXIII"))

    def test_converts_standard_boundaries(self) -> None:
        self.assertEqual(from_roman("MMMCMXCIX"), 3999)
        self.assertEqual(to_roman(944), "CMXLIV")

    def test_rejects_noncanonical_numerals(self) -> None:
        with self.assertRaises(ValueError):
            from_roman("IIII")

    def test_rejects_sum_above_standard_limit(self) -> None:
        with self.assertRaises(ValueError):
            add_roman("MM", "MM")


class MultiplicationTests(unittest.TestCase):
    def test_multiplies_by_repeated_addition(self) -> None:
        self.assertEqual(multiply_by_addition(7, 4), (28, [7, 14, 21, 28]))

    def test_zero_multiplier_performs_no_additions(self) -> None:
        self.assertEqual(multiply_by_addition(8, 0), (0, []))

    def test_rejects_values_outside_single_digits(self) -> None:
        with self.assertRaises(ValueError):
            multiply_by_addition(10, 2)


if __name__ == "__main__":
    unittest.main()