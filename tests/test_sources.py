"""Unit-тесты источников данных (файл и веб-страница)."""
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import requests

from exceptions.file_source_error import FileSourceError
from exceptions.web_source_error import WebSourceError
from sources.file_source import FileSource
from sources.web_source import WebSource


class TestFileSource(unittest.TestCase):
    """Чтение из файла."""

    def test_read_ok(self):
        with tempfile.NamedTemporaryFile(
                "w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
            tmp.write("112-233-445 95")
        try:
            self.assertEqual(FileSource(tmp.name).read(), "112-233-445 95")
        finally:
            os.remove(tmp.name)

    def test_file_not_found(self):
        with self.assertRaises(FileSourceError):
            FileSource("no_such_file.txt").read()

    def test_wrong_encoding(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
            tmp.write(b"\xff\xfe\xfa")
        try:
            with self.assertRaises(FileSourceError):
                FileSource(tmp.name).read()
        finally:
            os.remove(tmp.name)


class TestWebSource(unittest.TestCase):
    """Загрузка страницы (requests подменяется заглушкой)."""

    def test_bad_url(self):
        with self.assertRaises(WebSourceError):
            WebSource("example.com").read()

    @patch("sources.web_source.requests.get")
    def test_read_ok(self, mock_get):
        response = MagicMock()
        response.text = "<p>112-233-445 95</p>"
        mock_get.return_value = response
        self.assertEqual(WebSource("https://x.ru").read(),
                         "<p>112-233-445 95</p>")
        mock_get.assert_called_once_with("https://x.ru", timeout=10)

    @patch("sources.web_source.requests.get")
    def test_http_error(self, mock_get):
        response = MagicMock()
        response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = response
        with self.assertRaises(WebSourceError):
            WebSource("https://x.ru").read()

    @patch("sources.web_source.requests.get",
           side_effect=requests.ConnectionError("нет сети"))
    def test_connection_error(self, _mock_get):
        with self.assertRaises(WebSourceError):
            WebSource("https://x.ru").read()


if __name__ == "__main__":
    unittest.main()
