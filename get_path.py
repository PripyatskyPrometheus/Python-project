from simpleIterator import Simple_Iterator_1
from typing import Optional


def get_path(file_name: str, class_name: str) -> Optional[str] :
    '''получаем объекты класса и выводим их, если они не равны None'''
    # получаем и перебираем элементы класса
    i = Simple_Iterator_1(file_name, class_name)
    for val in i:
        if (val != None):
            print(val)


if __name__ == "__main__":
    file_name = 'dataset'
    class_name = 'good'
    get_path(file_name, class_name)
    class_name = 'bad'
    get_path(file_name, class_name)
    