# TO DO:
# при удалении выбранного фильма с конца, вместо него записывается пустое место
# добавить возможность удалить список целиком
# использую import logging написать логгирование ошибок
import os
import sys
import time
import random
import re

from typing import List, Pattern

from utils import (
    clear,
    loading_imitation,
    is_empty,
    empty_input,
    separate,
    path_to_file,
    PATH_TO_FOLDER
)


def create_movie_list() -> None:
    """Создать в каталоге список фильмов."""
    EXIT_COMMANDS: List[str] = ['quit', 'q', '']

    if not os.path.isdir(PATH_TO_FOLDER):
        os.mkdir(PATH_TO_FOLDER)

    file_name: str = input('\nВведите название списка: ')
    count: int = 1
    while True:
        if not is_empty(file_name):
            filename: str = file_name
            file_name += '.txt'
            file_name_show: str = 'Файл: ' + file_name
            clear()
            print(file_name_show)
            separate(value=len(file_name_show))
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
                    clear()
                    input(f'Список \"{filename}\" создан.\n<Enter>')
                return
            print('Файл с таким именем уже существует! Попробуйте снова.')
            file_name = input('Введите другое название файла: ')
        clear()
        empty_input(count)
        if count > 10:
            return
        count += 1
        file_name = input('Введите другое название файла: ')


def get_all_movie_list() -> List[str]:
    """Получить все имеющиеся списки."""
    all_movie_list: List[str] = []
    if os.path.isdir(PATH_TO_FOLDER):
        for _, _, files in os.walk(PATH_TO_FOLDER):
            for filename in files:
                all_movie_list.append(filename)
    if not is_empty(all_movie_list):
        all_movie_list.sort()
        return all_movie_list
    print('У вас нет ни одного списка с фильмами.')
    input('<Enter>')
    return None


def length_for_separate(movie_list: List[str]) -> int:
    """Высчитывает количество символов для разделителя."""
    total: int = 0
    for i in range(len(movie_list)):
        if i == len(movie_list) - 1:
            total += len(movie_list[i])
            break
        total += len(movie_list[i]) + 3
    return total


def select_movie_list() -> None:
    """Выбрать список из имеющихся."""
    SELECT_FILE_MSG: str = (
        'Выберите файл из списка '
        '<пустая строка для возврата назад>: '
    )
    FILE_NOT_EXIST: str = 'Такого файла не существует! Попробуйте снова.'

    all_movie_list: List[str] = get_all_movie_list()
    if all_movie_list is not None:
        print(*all_movie_list, sep=' | ')
        sep_len: int = length_for_separate(all_movie_list)
        separate(value=(sep_len))
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


def random_movie(filename: str) -> None:
    """Выбрать рандомный фильм из списка."""
    file_path = path_to_file(filename)
    with open(file_path, 'r') as fin:
        movie_list_for_random: List[str] = [movie.rstrip() for movie in fin]
    rand_film: str = random.choice(movie_list_for_random)
    selected_movie: str = 'Ваш фильм на сегодня: ' + rand_film
    print(selected_movie)
    separate(value=len(selected_movie))
    process_movie(filename, rand_film)


def delete_selected_movie(filename: str, moviename: str) -> None:
    """Удаляет выбранный фильм."""
    file_path = path_to_file(filename)
    pattern: Pattern[str] = re.compile(re.escape(moviename))
    with open(file_path, 'r+') as fstream:
        movies: List[str] = fstream.readlines()
        fstream.seek(0)
        for movie in movies:
            result = pattern.search(movie)
            if result is None:
                fstream.write(movie)
            fstream.truncate()
    clear()
    print(f'Фильм \"{moviename}\" удален из списка {filename}')
    input('<Enter>')
    return


def process_movie(filename: str, moviename: str) -> None:
    """Доступные действия со случайным фильмом."""
    SELECT_ACTION: List[str] = [
        'yes', 'y',
        'no', 'n',
        'да', 'д',
        'нет', 'н',
    ]
    MENU_MSG: str = (
        'Выбрать и удалить из списка: <да> | '
        'Ещё попытка: <нет> | '
        'Назад: <Enter>'
    )

    print(MENU_MSG)
    while True:
        try:
            answer: str = input('Ваш выбор: ')
            if is_empty(answer):
                return
            if answer.lower() not in SELECT_ACTION:
                raise Exception
            if answer.lower() in ['yes', 'y', 'да', 'д']:
                delete_selected_movie(filename, moviename)
                return
            if answer.lower() in ['no', 'n', 'нет', 'н']:
                clear()
                loading_imitation('Попробуем ещё раз', 2, 0.2)
                random_movie(filename)
            break
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
    INPUT_MSG: str = (
        'Введите название фильма '
        '<пустая строка для возврата назад>: '
    )

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
    print('Спасибо за использование программы.')
    time.sleep(0.7)
    clear()
    loading_imitation('Программа завершается', 2, 0.7)
    sys.exit()


def say_hello() -> None:
    """Приветствие."""
    clear()
    HELLO_MSG: str = (
        'Добро пожаловать в программу '
        'по выбору случайного фильма!'
    )

    print(HELLO_MSG)
    separate('=', len(HELLO_MSG))
    time.sleep(2)
    clear()
    loading_imitation('Загрузка', 2, 0.3)


def show_menu(filename=None) -> int:
    """Вывод меню приложения."""
    MENU_MSG: str = 'Меню'
    menu_buttons: List[int] = [0, 1, 2]

    clear()
    if filename is not None:
        menu_buttons.append(3)
        file_name_msg: str = 'Файл: ' + filename
        print(file_name_msg)
        separate(value=len(file_name_msg))
        menu_choices: str = (
            '1. Показать список.\n'
            '2. Добавить фильм в список.\n'
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
