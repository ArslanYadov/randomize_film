import os
import sys
import time
import random

from utils import (
    clear,
    loading_imitation,
    is_empty,
    separate,
    path_to_file,
    confirm_to_delete
)
from constant import (
    PATH_TO_FOLDER,
    SELECT_ACTION,
    STEP_BACK
)


def create_movie_list() -> None:
    """Создать в каталоге список фильмов."""
    if not os.path.isdir(PATH_TO_FOLDER):
        os.mkdir(PATH_TO_FOLDER)

    file_name: str = input(f'\nВведите название списка. {STEP_BACK}')
    while True:
        if is_empty(file_name):
            return
        filename: str = file_name
        file_name += '.txt'
        file_name_show: str = 'Файл: ' + file_name
        file_name = path_to_file(file_name)
        if not os.path.exists(file_name):
            clear()
            print(file_name_show)
            separate(value=len(file_name_show))
            print(f'Введите название фильма. {STEP_BACK}')
            movie_list: list[str] = []
            title: str = ''
            i: int = 1
            while True:
                title = input(f'#{i}: ')
                if is_empty(title):
                    break
                movie_list.append(title)
                i += 1
            if not is_empty(movie_list):
                with open(file_name, 'w') as fout:
                    for movie in movie_list:
                        fout.write(movie + '\n')
                    fout.truncate()
                clear()
                input(f'Список \"{filename}\" создан.\n{STEP_BACK}')
            return
        print('Файл с таким именем уже существует! Попробуйте снова.')
        file_name = input('Введите другое название файла: ')


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
                edit_file += '.txt'
                read_add_file(edit_file, show_menu(edit_file))
                break
            elif edit_file in all_movie_list:
                all_movie_list[edit_file] += '.txt'
                read_add_file(
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


def read_add_file(filename: str, choice_number: int) -> None:
    """
    Показать список.
    Добавить в список.
    Выбрать случайный фильм из списка.
    """
    if choice_number not in [1, 2, 3, 4]:
        return
    menu: dict = {
        1: read_file,
        2: add_file,
        3: random_movie,
        4: delete_list
    }
    menu[choice_number](filename)
    read_add_file(filename, show_menu(filename))


def get_all_movie_list() -> list[str]:
    """Получить все имеющиеся списки."""
    all_movie_list: dict[str, str] = {}
    if os.path.isdir(PATH_TO_FOLDER):
        for _, _, files in os.walk(PATH_TO_FOLDER):
            all_movie_list = {
                str(id): file[:-4] for (id, file) in enumerate(files, start=1)
            }
    if not is_empty(all_movie_list):
        return all_movie_list
    print('У вас нет ни одного списка с фильмами.')
    separate(value=len(STEP_BACK))
    input(STEP_BACK)
    return None


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

    new_movie_list: list[str] = []
    movie: str = input(INPUT_MSG)
    while True:
        if is_empty(movie):
            break
        new_movie_list.append(movie)
        clear()
        print(*new_movie_list, sep='\n')
        separate(value=len(INPUT_MSG))
        movie: str = input(INPUT_MSG)
    if not is_empty(new_movie_list):
        with open(path_to_file(filename), 'a') as fstream:
            for movie in new_movie_list:
                fstream.write(movie + '\n')
            fstream.truncate()
    return


def random_movie(filename: str) -> None:
    """Выбрать рандомный фильм из списка."""
    file_path = path_to_file(filename)
    with open(file_path, 'r') as fin:
        movie_list_for_random: list[str] = [movie.rstrip() for movie in fin]
    if is_empty(movie_list_for_random):
        input(
            'Нельзя выбрать фильм из пустого списка. '
            'Наполните его фильмами.\n'
            f'{STEP_BACK} для возврата назад: ')
        return
    rand_film: str = random.choice(movie_list_for_random)
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


def show_menu(filename=None) -> int:
    """Вывод меню приложения."""
    MENU_MSG: str = 'Меню'
    menu_buttons: list[int] = [0, 1, 2]

    clear()
    if filename is not None:
        menu_buttons.extend([3, 4])
        file_name_msg: str = 'Файл: ' + filename
        print(file_name_msg)
        separate(value=len(file_name_msg))
        menu_choices: str = (
            '1. Показать список.\n'
            '2. Добавить фильм в список.\n'
            '3. Выбрать случайный фильм из списка.\n'
            '4. Удалить список.\n'
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
            clear()
            error: str = '[Error] Неверный формат. Необходимо ввести число.'
            print(error)
            separate(value=len(error))
            print(menu_choices)
        except Exception:
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
        menu_list = {
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
