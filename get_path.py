import os
from simpleIterator import Simple_Iterator_1
from typing import Optional


def get_path(file_name: str, class_name: str, index: int) -> Optional[str]:
    """получение путей файлов"""

    i = Simple_Iterator_1(file_name, class_name)
    for val in i:
        if (val != None):
            print(val)
    

def find_review_by_path(path_txt: str) -> str:
    text = ''
    with open('dataset', 'r', encoding='utf-8') as file:
        for item in file:
            text += item
    return text


if __name__ == "__main__":
    file_name = 'dataset'
    class_name = 'good'
    print(get_path(file_name, class_name, 0))
    print(get_path(file_name, class_name, 77))