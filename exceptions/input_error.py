"""Ошибка пользовательского ввода."""
from exceptions.app_error import AppError


class InputError(AppError):
    """Некорректный ввод пользователя."""