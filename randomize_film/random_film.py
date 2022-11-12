import os
import sys
import time
import random

from utils import (
    clear,
    loading_imitation,
    is_empty,
    separate,
    path_to_file
)
from constants import (
    PATH_TO_FOLDER,
    SELECT_ACTION,
    CONFIRM,
    DECLINE,
    STEP_BACK
)
from modules import (
    confirm_to_delete,
    fill_movie_list,
    get_all_movie_list,
    get_menu
)


def create_movie_list() -> None:
    """Создать в каталоге список фильмов."""
    if not os.path.isdir(PATH_TO_FOLDER):
        os.mkdir(PATH_TO_FOLDER)

    input_name_for_file: str = input(f'Введите название списка. {STEP_BACK}')
    while True:
        if is_empty(input_name_for_file):
            return
        file_path: str = path_to_file(input_name_for_file)
        if not os.path.exists(file_path):
            fill_movie_list(file_path, input_name_for_file)
            return
        clear()
        print('[Error] Файл с таким именем уже существует! Попробуйте снова.')
        input_name_for_file = input(
            f'Введите другое название файла. {STEP_BACK}'
        )


def select_movie_list() -> None:
    """Выбрать список из имеющихся."""
    SELECT_FILE_MSG: str = (
        'Выберите файл из списка. '
        f'{STEP_BACK}'
    )
    FILE_NOT_EXIST: str = 'Такого файла не существует! Попробуйте снова.'

    all_movie_list: dict[str, str] = get_all_movie_list()
    if all_movie_list is not None:
        for id, filename in all_movie_list.items():
            print(f'{id}: {filename}')
        separate(value=len(SELECT_FILE_MSG))
        edit_file: str = input(SELECT_FILE_MSG)
        while True:
            if is_empty(edit_file):
                return
            if edit_file in all_movie_list.values():
                process_file(edit_file, show_menu(edit_file))
                break
            elif edit_file in all_movie_list:
                process_file(
                    all_movie_list[edit_file],
                    show_menu(all_movie_list[edit_file])
                )
                break
            else:
                clear()
                for id, filename in all_movie_list.items():
                    print(f'{id}: {filename}')
                separate(value=len(SELECT_FILE_MSG))
                print(FILE_NOT_EXIST)
                edit_file = input(SELECT_FILE_MSG)


def process_file(filename: str, choice_number: int) -> None:
    """
    Показать список.
    Добавить в список.
    Выбрать случайный фильм из списка.
    Удалить список.
    """
    if choice_number not in [1, 2, 3, 4]:
        return
    menu_buttons: dict = {
        1: read_file,
        2: add_file,
        3: random_movie,
        4: delete_list
    }
    menu_buttons[choice_number](filename)
    process_file(filename, show_menu(filename))


def read_file(filename: str) -> None:
    """Показать список."""
    if os.path.getsize(path_to_file(filename)) == 0:
        input(f'Тут ещё ничего нет. {STEP_BACK}')
        return
    with open(path_to_file(filename), 'r') as fin:
        for num, movie in enumerate(fin, start=1):
            print(f'{num}: {movie}', end='')
        separate(value=len(STEP_BACK))
        if input(STEP_BACK):
            return


def add_file(filename: str) -> None:
    """Добавить фильм в конец списка."""
    INPUT_MSG: str = (
        'Введите название фильма. '
        f'{STEP_BACK}'
    )

    movies_list: list[str] = []
    movie: str = input(INPUT_MSG)
    while True:
        if is_empty(movie):
            break
        movies_list.append(movie)
        clear()
        print(*movies_list, sep='\n')
        separate(value=len(INPUT_MSG))
        movie: str = input(INPUT_MSG)
    if not is_empty(movies_list):
        with open(path_to_file(filename), 'a') as fstream:
            for movie in movies_list:
                fstream.write(movie + '\n')
            fstream.truncate()
    return


def random_movie(filename: str) -> None:
    """Выбрать рандомный фильм из списка."""
    file_path = path_to_file(filename)
    with open(file_path, 'r') as fin:
        movies_list: list[str] = [movie.rstrip() for movie in fin]
    if is_empty(movies_list):
        input(
            'Нельзя выбрать фильм из пустого списка. '
            'Наполните его фильмами.\n'
            f'{STEP_BACK} для возврата назад: ')
        return
    rand_film: str = random.choice(movies_list)
    selected_movie: str = 'Ваш фильм на сегодня: ' + rand_film
    print(selected_movie)
    separate(value=len(selected_movie))
    process_movie(filename, rand_film)


def process_movie(filename: str, moviename: str) -> None:
    """Доступные действия со случайным фильмом."""
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
            if answer.lower() in CONFIRM:
                delete_selected_movie(filename, moviename)
                return
            if answer.lower() in DECLINE:
                clear()
                loading_imitation('Попробуем ещё раз', 2, 0.2)
                random_movie(filename)
            break
        except KeyError:
            print('[Error] Выберите доступные действия из меню')
            print(MENU_MSG)


def delete_selected_movie(filename: str, moviename: str) -> None:
    """Удаляет выбранный фильм."""
    clear()
    file_path = path_to_file(filename)
    if not confirm_to_delete(moviename):
        return
    with open(file_path, 'r+') as fstream:
        movies: list[str] = fstream.readlines()
        fstream.seek(0)
        for movie in movies:
            if movie.lower() != moviename + '\n':
                fstream.write(movie)
            fstream.truncate()
    clear()
    input(f'Фильм \"{moviename}\" удален из списка {filename}.\n{STEP_BACK}')
    return


def delete_list(filename: str) -> None:
    """Удаление выбранного списка из каталога."""
    if not confirm_to_delete(filename):
        return
    os.remove(path_to_file(filename))
    clear()
    input(f'Список \"{filename}\" удален из каталога.\n{STEP_BACK}')
    menu()


def exit() -> None:
    """Закрытие программы."""
    print('Спасибо за использование программы.')
    time.sleep(1)
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


def show_menu(filename: str = None) -> int:
    """Вывод меню приложения."""
    clear()
    menu_choices, menu_buttons = get_menu(filename)
    while True:
        try:
            choose_button: int = int(input('Выберите действие: '))
            if choose_button not in menu_buttons:
                raise Exception
            break
        except ValueError:
            clear()
            error: str = '[Error] Неверный формат. Необходимо ввести число.'
            print(error)
            separate(value=len(error))
            print(menu_choices)
        except KeyError:
            clear()
            error: str = '[Error] Выберите доступные действия из меню'
            print(error)
            separate(value=len(error))
            print(menu_choices)
    clear()
    return choose_button


def menu() -> None:
    """Меню приложения."""
    while True:
        choice_number: int = show_menu()
        menu_list: dict[int, ] = {
            0: exit,
            1: create_movie_list,
            2: select_movie_list,
        }
        menu_list[choice_number]()


def main() -> None:
    """Основная логика программы."""
    say_hello()
    menu()


if __name__ == '__main__':
    main()
