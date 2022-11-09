import os

from typing import List


PATH_TO_FOLDER: str = os.path.expanduser(r'~/Movie List')

SELECT_ACTION: List[str] = [
    'yes', 'y',
    'no', 'n',
    'да', 'д',
    'нет', 'н',
]

STEP_BACK: str = '<Enter> для возврата назад: '
