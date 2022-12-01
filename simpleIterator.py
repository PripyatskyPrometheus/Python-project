import csv
import re


class SimpleIterator:

    def __init__(self, class_file: str, class_name: str):
        self.class_name = class_name
        self.list = []
        self.class_file = class_file
        self.counter = 0

        with open(self.class_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                self.list.append(row)


    def __iter__(self):
        return self


    def __next__(self) -> str:
        if self.counter < len(self.list):
            abs_way = re.split(';', str(self.list[self.counter]))
            self.counter += 1
            nc = self.class_name + ']'
            if abs_way[2] == nc:
                return abs_way[0][2:]
        else:
            raise StopIteration