import os
import sys
import time


def create_movie_list():
    """Создать список фильмов и сохранить в файл."""
    folder_for_movie_list: str = 'Movie List'
    if not os.path.isdir(folder_for_movie_list):
        os.mkdir(folder_for_movie_list)
    os.chdir(folder_for_movie_list)

    file_name: str = input('\nВведите название файла: ')
    file_name +='.txt'
    if not os.path.exists(file_name):
        print(
            'Введите название фильма\n'
            'Для разделения используйте enter\n'
            'Чтобы выйти введите <q or quit>:\n'
        )
        movie_list = []
        title: str = ''
        i = 1
        while True:
            title = input(f'#{i}: ')
            if title == 'q' or title == 'quit':
                break
            movie_list.append(title)
            i += 1

        with open(file_name, 'w') as fout:
            fout.writelines('\n'.join(movie_list))
        return
    return


def choose_movie_list():
    """Выбрать список из имеющихся."""
    ...


def randomize_movie():
    """Выбрать рандомный фильм из списка."""
    ...


def exit() -> None:
    """Закрытие программы."""
    print('Спасибо за использование программы.')
    time.sleep(1)
    print('Программа завершается.')
    time.sleep(1)
    sys.exit()


def say_hello() -> None:
    """Приветствие."""
    hello_msg = 'Добро пожаловать в программу по случайному выбору фильма!'
    print(hello_msg)
    print('=' * len(hello_msg))


def show_menu() -> int:
    """
    1. Создать новый список фильмов.
    2. Выбрать готовый список фильмов.
    0. Выход из программы.
    """
    print('Меню')
    print(
        '1. Для создания нового списка.\n'
        '2. Открыть/редактировать имеющийся список.\n'
        '0. Выход.'
    )
    choose_button: int = int(input('Выберите действие: '))
    return choose_button


def main() -> None:
    """Основная логика программы."""
    say_hello()
    choice_number = show_menu()
    menu_list = {
        0: exit,
        1: create_movie_list,
        2: choose_movie_list,
    }
    menu_list[choice_number]()
    #randomize_movie()
    exit()


if __name__ == '__main__':
    main()
