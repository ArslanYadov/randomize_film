import os
import time

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
    for _ in range(cycle):
        print(message + '.')
        time.sleep(seconds)
        clear()
        print(message + '..')
        time.sleep(seconds)
        clear()
        print(message + '...')
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
