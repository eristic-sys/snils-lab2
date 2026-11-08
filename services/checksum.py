"""Контрольное число СНИЛС."""
import re

# Для номеров не больше 001-001-998 контрольное число не проверяется.
MIN_CHECKED_NUMBER = 1001998
WEIGHTS = range(9, 0, -1)  # веса разрядов: 9, 8, ..., 1


def split_snils(text: str) -> tuple:
    """Делит СНИЛС на номер (9 цифр) и контрольное число."""
    digits = re.sub(r"\D", "", text)
    return digits[:9], int(digits[9:])


def needs_check(number: str) -> bool:
    """Нужно ли проверять контрольное число для этого номера."""
    return int(number) > MIN_CHECKED_NUMBER


def calc_control(number: str) -> int:
    """Вычисляет контрольное число по первым 9 цифрам."""
    total = sum(int(d) * w for d, w in zip(number, WEIGHTS))
    if total < 100:
        return total
    if total in (100, 101):
        return 0
    remainder = total % 101
    return 0 if remainder == 100 else remainder