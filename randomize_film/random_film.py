# TO DO:
# разобраться с пунктами в меню (общий и для конкретного файла)
# сделать возможность удалить выбранный в рандоме фильм
# использую import logging написать логгирование ошибок
import os
import sys
import time
import random
import itertools

from typing import List, Any


EXIT_COMMANDS: List[str] = ['quit', 'q', '']
PATH_TO_FOLDER: str = os.path.expanduser(r'~/Dev/randomize_film/randomize_film/Movie List')


def separate(symbol: str = '-', value: int = 20) -> None:
    """Отделяет название от меню."""
    print(symbol * value)


def path_to_file(filename) -> str:
    """Возвращает путь к выбранному файлу."""
    return os.path.join(PATH_TO_FOLDER, filename)


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
        file_name = path_to_file(file_name)
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


def get_all_movie_list() -> List[str]:
    """Получить все имеющиеся списки."""
    all_movie_list: List[str] = []
    if os.path.isdir(PATH_TO_FOLDER):
        for _, _, files in os.walk(PATH_TO_FOLDER):
            for filename in files:
                all_movie_list.append(filename)
        return all_movie_list
    print('У вас нет ни одного списка с фильмами.')
    return None


def length_for_separate(movie_list: List[str]) -> int:
    """Высчитывает количество символов для разделителя."""
    total: int = 0
    for i in range(len(movie_list)):
        total += len(movie_list[i])
    return total


def calculate_tail(length_movie_lists: int) -> int:
    """Рассчитывает последний символ для разделителя."""
    tail: int
    if length_movie_lists % 2 == 0:
        tail = 1
        return tail
    tail = 2
    return tail


def select_movie_list() -> None:
    """Выбрать список из имеющихся."""
    SELECT_FILE_MSG: str = 'Выберите файл из списка <пустая строка для возврата назад>: '
    FILE_NOT_EXIST: str = 'Такого файла не существует! Попробуйте снова.'

    all_movie_list: List[str] = get_all_movie_list()
    if all_movie_list is not None:
        print(*all_movie_list, sep=' | ')
        sep_len: int = length_for_separate(all_movie_list)
        tail: int = calculate_tail(len(all_movie_list))
        separate(value=(sep_len + 2*len(all_movie_list) + tail))
        edit_file: str = input(SELECT_FILE_MSG)
        while True:
            if is_empty(edit_file):
                return
            edit_file += '.txt'
            if edit_file in all_movie_list:
                read_add_file(edit_file, show_menu(edit_file))
                break
            else:
                print(FILE_NOT_EXIST)
                edit_file = input(SELECT_FILE_MSG)
    return


def random_movie(filename: str) -> None:
    """Выбрать рандомный фильм из списка."""
    filename = path_to_file(filename)
    movie_list_for_random: List[str] = []
    with open(filename, 'r') as fin:
        for movie in fin:
            movie_list_for_random.append(movie)
    print('Ваш фильм на сегодня:', random.choice(movie_list_for_random))
    separate()
    process_movie(filename)


def process_movie(filename) -> None:
    """Доступные действия со случайным фильмом."""
    SELECT_ACTION: List[str] = [
        '',
        'yes', 'y',
        'no', 'n',
        'да', 'д',
        'нет', 'н',
    ]
    MENU_MSG: str = 'Выбрать и удалить из списка: <да> | Ещё попытка: <нет> | Назад: <Enter>'

    print(MENU_MSG)
    while True:
        try:
            answer: str = input('Ваш выбор: ')
            if answer.lower() not in SELECT_ACTION:
                raise Exception
            if answer.lower() in ['yes', 'y', 'да', 'д']:
                ...
            if answer.lower() in ['no', 'n', 'нет', 'н']:
                clear()
                random_movie(filename)
            if answer == '':
                return
        except Exception:
            print('[Error] Выберите доступные действия из меню')
            print(MENU_MSG)


def read_add_file(filename: str, choice_number: int) -> None:
    """
    Показать список.
    Добавить в список.
    Выбрать случайный фильм из списка.
    """
    if choice_number not in [1, 2, 3]:
        return
    menu: dict = {
        1: read_file,
        2: add_file,
        3: random_movie,
    }
    menu[choice_number](filename)
    read_add_file(filename, show_menu(filename))


def read_file(filename) -> None:
    """Показать список."""
    with open(path_to_file(filename), 'r') as fin:
        for num, movie in enumerate(fin, start=1):
            print(f'{num}: {movie}', end='')
        print()
        if input('<Enter>'):
            return


def add_file(filename) -> None:
    """Добавить фильм в конец списка."""
    INPUT_MSG: str = 'Введите название фильма <пустая строка для возврата назад>: '

    new_movie_list: List[str] = []
    movie: str = input(INPUT_MSG)
    while True:
        if is_empty(movie):
            break
        new_movie_list.append(movie)
        clear()
        print(*new_movie_list, sep='\n')
        separate()
        movie: str = input(INPUT_MSG)
    if not is_empty(new_movie_list):
        with open(path_to_file(filename), 'a') as fstream:
            fstream.write('\n')
            fstream.writelines('\n'.join(new_movie_list))
    return


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
    time.sleep(2)


def show_menu(filename=None) -> int:
    """Вывод меню приложения."""
    MENU_MSG: str = 'Меню'
    menu_buttons: List[int] = [0, 1, 2]

    clear()
    if filename is not None:
        menu_buttons.append(3)

        print('Файл:', filename)
        separate()
        menu_choices: str = (
            '1. Показать список.\n'
            '2. Добавить в список.\n'
            '3. Выбрать случайный фильм из списка.\n'
            '0. Назад.'
        )
        print(menu_choices)
    else:
        print(f'{MENU_MSG:*^10}')
        menu_choices: str = (
            '1. Для создания нового списка.\n'
            '2. Открыть/редактировать имеющийся список.\n'
            '0. Выход.'
        )
        print(menu_choices)
    while True:
        try:
            choose_button: int = int(input('Выберите действие: '))
            if choose_button not in menu_buttons:
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
