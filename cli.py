"""Консольный интерфейс."""
from exceptions.app_error import AppError
from exceptions.input_error import InputError
from models.check_result import CheckResult, Status
from services.finder import check_all
from services.validator import check
from sources.file_source import FileSource
from sources.web_source import WebSource

MENU = """
1 - Проверить СНИЛС (ввод)
2 - Найти СНИЛС в файле
3 - Найти СНИЛС на веб-странице
0 - Выход"""


def read_input(prompt: str) -> str:
    """Читает непустую строку от пользователя."""
    value = input(prompt).strip()
    if not value:
        raise InputError("Пустой ввод.")
    return value


def describe(result: CheckResult) -> str:
    """Текстовое описание результата проверки одного СНИЛС."""
    if result.status is Status.BAD_FORMAT:
        return "Неверный формат (нужно XXX-XXX-XXX YY)."
    if result.status is Status.BAD_CONTROL:
        return ("Формат верный, но контрольное число неверно "
                f"(должно быть {result.expected_control:02d}).")
    return "СНИЛС корректен."


def format_results(results: list) -> str:
    """Формирует отчёт по найденным СНИЛС."""
    if not results:
        return "СНИЛС не найдены."
    lines = [f"Найдено СНИЛС: {len(results)}"]
    for result in results:
        if result.is_valid:
            lines.append(f"  [OK]      {result.value}")
        else:
            lines.append(f"  [ОШИБКА]  {result.value} "
                         f"(должно быть {result.expected_control:02d})")
    return "\n".join(lines)


def handle_choice(choice: str) -> bool:
    """Выполняет пункт меню. Возвращает False, если нужно выйти."""
    try:
        if choice == "1":
            print(describe(check(read_input("Введите СНИЛС: "))))
        elif choice == "2":
            text = FileSource(read_input("Путь к файлу: ")).read()
            print(format_results(check_all(text)))
        elif choice == "3":
            text = WebSource(read_input("URL: ")).read()
            print(format_results(check_all(text)))
        elif choice == "0":
            return False
        else:
            print("Неизвестная команда.")
    except AppError as err:
        print(f"Ошибка: {err}")
    return True


def main() -> None:
    """Главный цикл меню."""
    running = True
    while running:
        print(MENU)
        running = handle_choice(input("Выбор: ").strip())