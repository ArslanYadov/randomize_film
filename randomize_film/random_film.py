import sys
import time


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
    print('Спасибо за использование программы.')
    time.sleep(1)
    print('Программа завершается.')
    time.sleep(1)
    sys.exit()


def show_menu():
    """
    1. Создать новый список фильмов.
    2. Выбрать готовый список фильмов.
    0. Выход из программы.
    """
    hello_msg = 'Добро пожаловать в программу по случайному выбору фильма!'
    print(hello_msg)
    
    print('=' * len(hello_msg))
    print('Меню')
    print(
        '1. Для создания нового списка.\n'
        '2. Открыть/редактировать имеющийся список.\n'
        '0. Выход.'
    )
    choose_button: int = int(input('Выберите действие: '))
    return choose_button


def main():
    """Основная логика программы."""
    choice_number = show_menu()
    menu_list = {
        0: exit,
        1: create_movie_list,
        2: choose_movie_list,
    }
    menu_list[choice_number]()
    randomize_movie()


if __name__ == '__main__':
    main()
