def create_movie_list():
    """Создать список фильмов и сохранить в файл."""
    ...


def choose_movie_list():
    """Выбрать список из имеющихся."""
    ...


def randomize_movie():
    """Выбрать рандомный фильм из списка."""
    ...


def exit():
    """Закрытие программы."""
    ...


def show_menu():
    """
    1. Создать новый список фильмов.
    2. Выбрать готовый список фильмов.
    0. Выход из программы.
    """
    print('Приветствие')
    print('Выбор')
    choose_button: int = int(input('Введите нмоер: '))
    return choose_button


def main():
    """Основная логика программы."""
    show_menu()
    create_movie_list()
    choose_movie_list()
    randomize_movie()
    exit()


if __name__ == '__main__':
    main()
