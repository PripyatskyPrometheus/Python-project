from simpleIterator import SimpleIterator
from typing import Optional


def get_path(file_name, class_name) :
    # получаем и перебираем элементы класса
    i = SimpleIterator(file_name, class_name)
    for val in i:
        if (val != None):
            print(val)


if __name__ == "__main__":
    file_name = 'dataset.csv'
    class_name = 'good'
    get_path(file_name, class_name)
    class_name = 'bad'
    get_path(file_name, class_name)
    