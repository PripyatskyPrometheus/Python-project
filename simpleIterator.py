import os
import re
import csv
from typing import Optional


class Simple_Iterator_1:

    '''Класс итератор, для dataset'''
    #конструктор, где инициализириуем класс и файл
    def __init__(self, file_name: str, class_name: str):
        self.path_ = os.path.join(file_name, class_name)
        self.names = os.listdir(self.path_)
        names_ = self.names.copy()
        for i in names_:
            if not ".txt" in i:
                self.names.remove(i)
        self.counter = 0

    #итератор, возвращаеющий самого себя
    def __iter__(self):
       return self

    #получаем следущий элемент
    def __next__(self) -> Optional[str]:
        if self.counter < len(self.names):
            self.counter += 1
            return str(os.path.join(self.path_, self.names[self.counter - 1]))
        else:
            raise StopIteration
        

class Simple_Iterator_2:

    '''Класс итератор, для copy_dataset'''
    #конструктор, где инициализириуем класс и файл
    def __init__(self, file_name: str, class_name: str):
        self.class_name = class_name
        self.list = []
        self.file_name = file_name
        self.counter = 0

        path_ = os.path.join(file_name, class_name)
        self.names = os.listdir(path_)
        for i in self.names:
            if not class_name in i:
                self.names.remove(i)
        self.counter = 0

    #итератор, возвращаеющий самого себя
    def __iter__(self):
        return self
    
    #получаем следущий элемент
    def __next__(self) -> Optional[str]:
        if self.counter < len(self.names):
            self.counter += 1
            return str(self.names[self.counter - 1])
        else: 
            raise StopIteration
        

class Simple_Iterator_3:

    '''Класс итератор, для random_dataset.csv'''
    #конструктор, где инициализириуем класс и файл
    def __init__(self, file_name: str, class_name: str):
        self.class_name = class_name
        self.list = []
        self.file_name = file_name
        self.counter = 0

        with open(self.file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.list.append(row)

    #итератор, возвращаеющий самого себя
    def __iter__(self):
        return self

    #получаем следущий элемент
    def __next__(self) -> Optional[str]:
        if self.counter < len(self.list):
            self.counter += 1
            return str(self.list[self.counter - 1])
        else:
            raise StopIteration
        
def run():
    print(Simple_Iterator_1("dataset", "bad"))

    Simple_Iterator_2("copy_dataset", "good")
    
    Simple_Iterator_3("random_number_dataset.csv", "bad")