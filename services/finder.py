"""Поиск СНИЛС в тексте."""
from services.patterns import SNILS_SEARCH
from services.validator import check, is_valid


def find_all(text: str, only_valid: bool = False) -> list:
    """Ищет все СНИЛС в тексте (по формату)."""
    found = SNILS_SEARCH.findall(text)
    if only_valid:
        found = [s for s in found if is_valid(s)]
    return found


def check_all(text: str) -> list:
    """Ищет все СНИЛС в тексте и проверяет каждый."""
    return [check(s) for s in find_all(text)]