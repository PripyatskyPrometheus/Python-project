import csv
import re


class SimpleIterator:

    def __init__(self, file_name: str, class_name: str):
        self.class_name = class_name
        self.list = []
        self.file_name = file_name
        self.counter = 0

        with open(self.file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                self.list.append(row)


    def __iter__(self):
        return self


    def __next__(self) -> str:
        if self.counter < len(self.list):
            self.counter += 1
            return str(self.list[self.counter - 1])
        else:
            raise StopIteration