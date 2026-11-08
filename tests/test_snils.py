"""Unit-тесты проверки и поиска СНИЛС."""
import unittest

from models.check_result import CheckResult, Status
from services.checksum import calc_control, needs_check, split_snils
from services.finder import check_all, find_all
from services.patterns import SNILS_FULL, SNILS_SEARCH
from services.validator import check, is_valid, is_valid_format


class TestPatterns(unittest.TestCase):
    """Регулярные выражения."""

    def test_full_accepts_space_and_dash(self):
        self.assertTrue(SNILS_FULL.fullmatch("112-233-445 95"))
        self.assertTrue(SNILS_FULL.fullmatch("112-233-445-95"))

    def test_full_rejects_wrong_format(self):
        for text in ["11223344595", "112 233 445 95", "112-233-445 9",
                     "1234-567-890 12", "abc-def-ghi jk", "", "112-233-445 95x"]:
            with self.subTest(text=text):
                self.assertIsNone(SNILS_FULL.fullmatch(text))

    def test_search_ignores_longer_digit_chains(self):
        self.assertEqual(SNILS_SEARCH.findall("9112-233-445 95"), [])
        self.assertEqual(SNILS_SEARCH.findall("112-233-445 957"), [])

    def test_search_finds_several(self):
        text = "a 112-233-445 95, b 123-456-789 64."
        self.assertEqual(SNILS_SEARCH.findall(text),
                         ["112-233-445 95", "123-456-789 64"])


class TestChecksum(unittest.TestCase):
    """Контрольное число."""

    def test_split(self):
        self.assertEqual(split_snils("112-233-445 95"), ("112233445", 95))

    def test_needs_check_boundary(self):
        self.assertFalse(needs_check("001001998"))
        self.assertTrue(needs_check("001001999"))
        self.assertFalse(needs_check("000000001"))

    def test_calc_less_than_100(self):
        self.assertEqual(calc_control("112233445"), 95)

    def test_calc_mod_101(self):
        self.assertEqual(calc_control("123456789"), 64)

    def test_calc_total_100_gives_zero(self):
        self.assertEqual(calc_control("001019989"), 0)  # сумма 100

    def test_calc_total_101_gives_zero(self):
        self.assertEqual(calc_control("001019998"), 0)  # сумма 101

    def test_calc_remainder_100_gives_zero(self):
        self.assertEqual(calc_control("002999989"), 0)  # 201 % 101 == 100


class TestValidator(unittest.TestCase):
    """Проверка формата и контрольного числа."""

    def test_valid(self):
        self.assertTrue(is_valid("112-233-445 95"))
        self.assertEqual(check("112-233-445 95").status, Status.VALID)

    def test_bad_format(self):
        result = check("12345")
        self.assertEqual(result.status, Status.BAD_FORMAT)
        self.assertFalse(is_valid_format("12345"))
        self.assertFalse(result.is_valid)

    def test_bad_control(self):
        result = check("123-456-789 00")
        self.assertEqual(result.status, Status.BAD_CONTROL)
        self.assertEqual(result.expected_control, 64)

    def test_small_number_not_checked(self):
        self.assertTrue(is_valid("001-001-998 00"))

    def test_result_is_immutable(self):
        result = CheckResult("x", Status.VALID)
        with self.assertRaises(Exception):
            result.value = "y"


class TestFinder(unittest.TestCase):
    """Поиск в тексте."""

    TEXT = ("Иванов 112-233-445 95; Петров 123-456-789 64; "
            "Сидоров 123-456-789 00; мусор 1234-567-890 12")

    def test_find_all(self):
        self.assertEqual(len(find_all(self.TEXT)), 3)

    def test_find_only_valid(self):
        self.assertEqual(find_all(self.TEXT, only_valid=True),
                         ["112-233-445 95", "123-456-789 64"])

    def test_check_all(self):
        results = check_all(self.TEXT)
        self.assertEqual([r.is_valid for r in results], [True, True, False])

    def test_empty_text(self):
        self.assertEqual(check_all(""), [])


if __name__ == "__main__":
    unittest.main()
