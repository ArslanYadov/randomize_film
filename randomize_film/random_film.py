# TO DO:
# написать функцию choose_movie_list для открытия и редактирования имеющегося файла
# написать функцию random_movie для рандомного флильма из выбранного списка
# использую import logging написать логгирование ошибок
import os
import sys
import time


MENU_BUTTONS: list = [0, 1, 2]
EXIT_COMMANDS: list = ['quit', 'q', '']


def create_movie_list() -> None:
    """Создать в каталоге список фильмов."""
    path_to_folder = os.path.expanduser(r'~/Dev/randomize_film/randomize_film/Movie List')
    if not os.path.isdir(path_to_folder):
        os.mkdir(path_to_folder)

    file_name: str = input('\nВведите название файла: ')
    while True:
        file_name += '.txt'
        file_name = os.path.join(path_to_folder, file_name)
        if not os.path.exists(file_name):
            print(
                'Введите название фильма.\n'
                'Для разделения фильмов используйте <Enter>.\n'
                'Чтобы выйти введите <q or quit> или оставьте пустое поле:'
            )
            movie_list: list = []
            title: str = ''
            i: int = 1
            while True:
                title = input(f'#{i}: ')
                if title.lower() in EXIT_COMMANDS:
                    break
                movie_list.append(title)
                i += 1
            if len(movie_list) != 0:
                with open(file_name, 'w') as fout:
                    fout.writelines('\n'.join(movie_list))

            return
        print('Файл с таким именем уже существует! Попробуйте снова.')
        file_name = input('Введите другое название файла: ')


def choose_movie_list():
    """Выбрать список из имеющихся."""
    ...


def random_movie():
    """Выбрать рандомный фильм из списка."""
    ...


def exit() -> None:
    """Закрытие программы."""
    print('Выход.')
    time.sleep(0.5)
    print('Спасибо за использование программы.')
    time.sleep(0.5)
    print('Программа завершается.')
    time.sleep(0.5)
    sys.exit()


def say_hello() -> None:
    """Приветствие."""
    hello_msg = 'Добро пожаловать в программу по случайному выбору фильма!'
    print(hello_msg)
    print('=' * len(hello_msg))


def show_menu() -> int:
    """Вывод меню приложения."""
    print('Меню')
    menu_choices: str = (
        '1. Для создания нового списка.\n'
        '2. Открыть/редактировать имеющийся список.\n'
        '0. Выход.'
    )
    print(menu_choices)
    while True:
        try:
            choose_button: int = int(input('Выберите действие: '))
            if choose_button not in MENU_BUTTONS:
                raise Exception
            break
        except ValueError:
            print('[Error] Неверный формат. Необходимо ввести число.')
        except Exception:
            print('[Error] Выберите доступные действия из меню')
            print(menu_choices)
    return choose_button


def main() -> None:
    """Основная логика программы."""
    say_hello()
    while True:
        choice_number: int = show_menu()
        menu_list = {
            0: exit,
            1: create_movie_list,
            2: choose_movie_list,
        }
        menu_list[choice_number]()


if __name__ == '__main__':
    main()
