"""Загрузка текста с веб-страницы."""
import requests

from exceptions.web_source_error import WebSourceError
from sources.base import BaseSource


class WebSource(BaseSource):
    """Источник: веб-страница по URL."""

    def __init__(self, url: str, timeout: int = 10) -> None:
        self.url = url
        self.timeout = timeout

    def read(self) -> str:
        if not self.url.startswith(("http://", "https://")):
            raise WebSourceError(
                "Адрес должен начинаться с http:// или https://")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()  # ошибка при кодах 4xx/5xx
        except requests.RequestException as err:
            raise WebSourceError(f"Ошибка запроса: {err}") from err
        return response.text