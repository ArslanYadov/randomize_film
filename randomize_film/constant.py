import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

if os.name == 'nt':
    PATH_TO_FOLDER: str = os.path.expanduser(r'~/Desktop/Movie List')
else:
    PATH_TO_FOLDER: str = os.path.expanduser(
        os.getenv('PATH_TO_FOLDER', r'~/Movie List')
    )

CONFIRM: list[str] = ['yes', 'y', 'да', 'д']

DECLINE: list[str] = ['no', 'n', 'нет', 'н']

SELECT_ACTION: list[str] = CONFIRM + DECLINE

STEP_BACK: str = '<Enter> для возврата назад: '
