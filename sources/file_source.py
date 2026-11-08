"""Чтение текста из файла."""
from exceptions.file_source_error import FileSourceError
from sources.base import BaseSource


class FileSource(BaseSource):
    """Источник: текстовый файл."""

    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        self.path = path
        self.encoding = encoding

    def read(self) -> str:
        try:
            with open(self.path, "r", encoding=self.encoding) as file:
                return file.read()
        except FileNotFoundError as err:
            raise FileSourceError(f"Файл не найден: {self.path}") from err
        except (OSError, UnicodeDecodeError) as err:
            raise FileSourceError(
                f"Не удалось прочитать файл: {err}") from err