"""Ошибка чтения файла."""
from exceptions.app_error import AppError


class FileSourceError(AppError):
    """Файл не найден или не читается."""