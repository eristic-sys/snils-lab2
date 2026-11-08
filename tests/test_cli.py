"""Unit-тесты консольного интерфейса."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import cli
from exceptions.input_error import InputError
from models.check_result import CheckResult, Status


def run(choice, *inputs):
    """Выполняет пункт меню с подменённым вводом, возвращает (флаг, вывод)."""
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=list(inputs)):
        with redirect_stdout(buffer):
            flag = cli.handle_choice(choice)
    return flag, buffer.getvalue()


class TestCli(unittest.TestCase):
    """Меню, форматирование, обработка ошибок."""

    def test_read_input_empty(self):
        with patch("builtins.input", return_value="  "):
            with self.assertRaises(InputError):
                cli.read_input("> ")

    def test_describe_all_statuses(self):
        self.assertIn("корректен",
                      cli.describe(CheckResult("a", Status.VALID)))
        self.assertIn("формат",
                      cli.describe(CheckResult("a", Status.BAD_FORMAT)))
        self.assertIn("64", cli.describe(
            CheckResult("a", Status.BAD_CONTROL, 64)))

    def test_format_results(self):
        self.assertEqual(cli.format_results([]), "СНИЛС не найдены.")
        text = cli.format_results([
            CheckResult("1", Status.VALID),
            CheckResult("2", Status.BAD_CONTROL, 5)])
        self.assertIn("[OK]", text)
        self.assertIn("(должно быть 05)", text)

    def test_choice_1(self):
        flag, out = run("1", "112-233-445 95")
        self.assertTrue(flag)
        self.assertIn("корректен", out)

    def test_choice_1_empty_input(self):
        _, out = run("1", "")
        self.assertIn("Ошибка", out)

    def test_choice_2_file_missing(self):
        _, out = run("2", "nope.txt")
        self.assertIn("Файл не найден", out)

    def test_choice_2_ok(self):
        with patch("cli.FileSource") as src:
            src.return_value.read.return_value = "x 112-233-445 95"
            _, out = run("2", "f.txt")
        self.assertIn("Найдено СНИЛС: 1", out)

    def test_choice_3_bad_url(self):
        _, out = run("3", "site.ru")
        self.assertIn("http", out)

    def test_exit_and_unknown(self):
        self.assertFalse(run("0")[0])
        self.assertIn("Неизвестная", run("9")[1])

    def test_main_loop_exits(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["9", "0"]):
            with redirect_stdout(buffer):
                cli.main()
        self.assertIn("Неизвестная", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
