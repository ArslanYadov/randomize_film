from load import loading_imitation


def empty_input(count: int) -> None:
    """Множественные попытки пустого ввода."""
    if count < 10:
        print('Имя файла не может быть пустым.')
    elif count == 10:
        loading_imitation('Проверяю', 10, .4)
        print('Нет, все же имя файла не может быть пустым.')
    return
