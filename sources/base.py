"""Базовый класс источника данных."""
from abc import ABC, abstractmethod


class BaseSource(ABC):
    """Общий интерфейс: любой источник умеет вернуть текст."""

    @abstractmethod
    def read(self) -> str:
        """Возвращает текст из источника."""