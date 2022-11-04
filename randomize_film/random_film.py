# TO DO:
# написать функцию select_movie_list для открытия и редактирования имеющегося файла
# написать функцию random_movie для рандомного флильма из выбранного списка
# использую import logging написать логгирование ошибок
import os
import sys
import time

from typing import List, Any


MENU_BUTTONS: List[int] = [0, 1, 2]
EXIT_COMMANDS: List[str] = ['quit', 'q', '']
PATH_TO_FOLDER: str = os.path.expanduser(r'~/Dev/randomize_film/randomize_film/Movie List')


def clear() -> None:
    """Очистака консоли."""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def is_empty(variable: Any) -> bool:
    """Проверка для пустого ввода."""
    return len(variable) == 0


def create_movie_list() -> None:
    """Создать в каталоге список фильмов."""
    if not os.path.isdir(PATH_TO_FOLDER):
        os.mkdir(PATH_TO_FOLDER)

    file_name: str = input('\nВведите название файла: ')
    if is_empty(file_name):
        file_name += 'NoName'
    while True:
        file_name += '.txt'
        file_name = os.path.join(PATH_TO_FOLDER, file_name)
        if not os.path.exists(file_name):
            print(
                'Введите название фильма.\n'
                'Для разделения фильмов используйте <Enter>.\n'
                'Чтобы выйти введите <q or quit> или оставьте пустое поле:'
            )
            movie_list: List[str] = []
            title: str = ''
            i: int = 1
            while True:
                title = input(f'#{i}: ')
                if title.lower() in EXIT_COMMANDS:
                    break
                movie_list.append(title)
                i += 1
            if not is_empty(movie_list):
                with open(file_name, 'w') as fout:
                    fout.writelines('\n'.join(movie_list))
            return
        print('Файл с таким именем уже существует! Попробуйте снова.')
        file_name = input('Введите другое название файла: ')


def get_all_movie_list() -> list:
    """Получить все имеющиеся списки."""
    all_movie_list: List[str] = []
    if os.path.isdir(PATH_TO_FOLDER):
        for _, _, files in os.walk(PATH_TO_FOLDER):
            for filename in files:
                all_movie_list.append(filename)
        return all_movie_list
    print('У вас нет ни одного списка с фильмами.')
    return None


def select_movie_list():
    """Выбрать список из имеющихся."""
    all_movie_list: List[str] = get_all_movie_list()
    if all_movie_list is not None:
        print(*all_movie_list)
        edit_file: str = input('Выберите файл из списка <пустая строка для возврата назад>: ')
        if not is_empty(edit_file):
            return
        return
    return


def random_movie():
    """Выбрать рандомный фильм из списка."""
    ...


def exit() -> None:
    """Закрытие программы."""
    print('Выход.')
    time.sleep(0.7)
    print('Спасибо за использование программы.')
    time.sleep(0.7)
    print('Программа завершается.')
    time.sleep(0.7)
    clear()
    sys.exit()


def say_hello() -> None:
    """Приветствие."""
    clear()
    hello_msg = 'Добро пожаловать в программу по случайному выбору фильма!'
    print(hello_msg)
    print('=' * len(hello_msg))
    time.sleep(1)


def show_menu() -> int:
    """Вывод меню приложения."""
    clear()
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
    clear()
    return choose_button


def main() -> None:
    """Основная логика программы."""
    say_hello()
    while True:
        choice_number: int = show_menu()
        menu_list = {
            0: exit,
            1: create_movie_list,
            2: select_movie_list,
        }
        menu_list[choice_number]()


if __name__ == '__main__':
    main()
