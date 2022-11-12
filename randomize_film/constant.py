import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

if os.name == 'nt':
        PATH_TO_FOLDER: str = os.path.expanduser(r'~/Desktop/Movie List')
else:
        PATH_TO_FOLDER: str = os.path.expanduser(os.getenv('PATH_TO_FOLDER', r'~/Movie List'))

SELECT_ACTION: list[str] = [
    'yes', 'y',
    'no', 'n',
    'да', 'д',
    'нет', 'н',
]

STEP_BACK: str = '<Enter> для возврата назад: '
