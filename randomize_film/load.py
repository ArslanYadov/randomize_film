import time

from clear import clear


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
