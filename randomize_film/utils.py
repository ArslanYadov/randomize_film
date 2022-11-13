import os
import time
import colorama

from typing import Any

from constants import PATH_TO_FOLDER


def clear() -> None:
    """Очистака консоли."""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def loading_imitation(
    message: str,
    cycle: int = 0,
    seconds: float = 0
) -> None:
    """Имитация загрузки."""
    amount_of_dots: int = 3
    for _ in range(cycle):
        print(message, end='\r')
        dot: str = '.'
        for i in range(amount_of_dots):
            print(f'\r{message}{dot * (i + 1)}', end='\r')
            time.sleep(seconds)
        clear()


def is_empty(variable: Any) -> bool:
    """Проверка для пустого ввода."""
    return len(variable) == 0


def separate(symbol: str = '-', value: int = 20) -> None:
    """Отделяет название от меню."""
    print(symbol * value)


def path_to_file(filename) -> str:
    """Возвращает путь к выбранному файлу."""
    return os.path.join(PATH_TO_FOLDER, filename)


def display_title(filename: str, extension: str = None) -> None:
    """Отобразить название и расширение."""
    display_filename: str = None
    if extension is not None:
        display_filename = f'Файл: {filename}.{extension}'
    else:
        display_filename = f'Ваш фильм на сегодня: {filename}'
    print(display_filename)
    separate(value=len(display_filename))


def progress_bar(progress: int, total: int, color=colorama.Fore.RED) -> None:
    """Прогресс бар."""
    bar: str = '=' * int(progress)
    print(color + f'\r{bar}', end='\r')
    if progress == total:
        print(colorama.Fore.GREEN + f'\r{bar}', end='\r')
