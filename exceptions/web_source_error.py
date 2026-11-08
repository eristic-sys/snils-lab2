"""Ошибка загрузки веб-страницы."""
from exceptions.app_error import AppError


class WebSourceError(AppError):
    """Страница недоступна или адрес некорректен."""