import os


def clear() -> None:
    """Очистака консоли."""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
