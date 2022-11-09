import os

from dotenv import load_dotenv, find_dotenv

from typing import List


load_dotenv(find_dotenv())

PATH_TO_FOLDER: str = os.path.expanduser(os.getenv('PATH_TO_FOLDER'), r'~/Movie List')

SELECT_ACTION: List[str] = [
    'yes', 'y',
    'no', 'n',
    'да', 'д',
    'нет', 'н',
]

STEP_BACK: str = '<Enter> для возврата назад: '
