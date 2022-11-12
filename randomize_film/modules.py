import os

from constants import (
    SELECT_ACTION,
    CONFIRM,
    STEP_BACK,
    PATH_TO_FOLDER
)
from utils import separate, clear, is_empty


def fill_movie_list(path: str, filename: str) -> None:
    """Наполнения списка фильмами."""
    display_filename: str = 'Файл: ' + filename + '.txt'
    clear()
    print(display_filename)
    separate(value=len(display_filename))
    print(f'Введите название фильма. {STEP_BACK}')
    movies_list: list[str] = []
    title: str = ''
    i: int = 1
    while True:
        title = input(f'#{i}: ')
        if is_empty(title):
            break
        movies_list.append(title)
        i += 1
    if not is_empty(movies_list):
        with open(path, 'w') as fout:
            for movie in movies_list:
                fout.write(movie + '\n')
            fout.truncate()
        clear()
        input(f'Список \"{filename}\" создан.\n{STEP_BACK}')


def confirm_to_delete(filename: str) -> bool:
    """Подтверждение на удаление."""
    while True:
        try:
            answer: str = input(
                'Вы уверены, что хотите удалить '
                f'\"{filename}\" из списка? [Да/Нет]: '
            )
            if answer.lower() not in SELECT_ACTION:
                raise KeyError
            break
        except KeyError:
            print('[Error] Да - удалить | Нет - вернуться назад.')
    if answer.lower() not in CONFIRM:
        return False
    return True


def get_all_movie_list() -> list[str]:
    """Получить все имеющиеся списки в каталоге."""
    all_movies_list: dict[str, str] = {}
    if os.path.isdir(PATH_TO_FOLDER):
        for _, _, files in os.walk(PATH_TO_FOLDER):
            all_movies_list = {
                str(id): file for (id, file) in enumerate(files, start=1)
            }
    if not is_empty(all_movies_list):
        return all_movies_list
    print('У вас нет ни одного списка с фильмами.')
    separate(value=len(STEP_BACK))
    input(STEP_BACK)
    return None


def get_menu(filename: str) -> tuple[list[str], list[int]]:
    """Выбор отображаемого меню."""
    MENU_MSG: str = 'Меню'
    menu_buttons: list[int] = [0, 1, 2]

    if filename is not None:
        menu_buttons.extend([3, 4])
        display_filename: str = 'Файл: ' + filename + '.txt'
        print(display_filename)
        separate(value=len(display_filename))
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
    return menu_choices, menu_buttons
