"""Проверка СНИЛС: формат и контрольное число."""
from models.check_result import CheckResult, Status
from services.checksum import calc_control, needs_check, split_snils
from services.patterns import SNILS_FULL


def is_valid_format(text: str) -> bool:
    """Проверяет, что вся строка является СНИЛС по формату."""
    return SNILS_FULL.fullmatch(text) is not None


def check(text: str) -> CheckResult:
    """Полная проверка СНИЛС с подробным результатом."""
    if not is_valid_format(text):
        return CheckResult(text, Status.BAD_FORMAT)
    number, control = split_snils(text)
    if not needs_check(number):
        return CheckResult(text, Status.VALID)
    expected = calc_control(number)
    if expected == control:
        return CheckResult(text, Status.VALID)
    return CheckResult(text, Status.BAD_CONTROL, expected)


def is_valid(text: str) -> bool:
    """Короткая проверка: True, если СНИЛС корректен."""
    return check(text).is_valid