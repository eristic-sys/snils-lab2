"""Модель результата проверки СНИЛС."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Status(Enum):
    """Статус проверки СНИЛС."""

    VALID = "корректен"
    BAD_FORMAT = "неверный формат"
    BAD_CONTROL = "неверное контрольное число"


@dataclass(frozen=True)
class CheckResult:
    """Результат проверки одного СНИЛС."""

    value: str
    status: Status
    expected_control: Optional[int] = None

    @property
    def is_valid(self) -> bool:
        """True, если СНИЛС полностью корректен."""
        return self.status is Status.VALID