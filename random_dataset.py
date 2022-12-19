import os
import csv
import shutil
import random
from typing import List


def add_to_csv_and_to_dataset_random_number(path_dataset: str, paths_txt: str) -> None:
    '''Функция создаёт папку для новорй dataset, если её нет, и записывает туда данные без деления на классы со случайными номерами 
    от 0 о 10 000, после того как запишет их в созданную здесь же файл-аннотацию.'''

    name_folder = "random_number_dataset"
    
    #создаём папку
    if not os.path.isdir(name_folder):
        os.mkdir(name_folder)

    path_random_number_dataset = os.path.abspath(name_folder)
    
    #создаём  или открываем файл аннотацию для заполнения
    with open('random_number_dataset.csv', 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(["Absolute path", "Relative path", "Class"])
        #проходимся по нашим файлам и записываем их имена в аннотацию, а данные с ними - папку новую папку
        for i in range (len(paths_txt)):
            class_txt = os.path.join(str(paths_txt[i]))
            class_name = 'bad'
            if class_txt [0 : 4] == ('good'):
                class_name = 'good'
            new_name = str(random.randint(0, 10000)).zfill(5) + '.txt'
            while os.path.isfile(new_name):
                new_name = str(random.randint(0, 10000)).zfill(5) + '.txt'
            writer.writerow([os.path.join(f'{path_dataset}', f'{ new_name }'),
                  os.path.join(f'..', 'random_number_dataset', f'{new_name}'), f'{class_name}'])
            shutil.copyfile(os.path.join(path_dataset, str(paths_txt[i])), os.path.join(path_random_number_dataset, new_name))


def find_path_txt(path_dataset: str) -> List[str]:
    '''Функция формирует и возвращает список из путей к текстовым файлам'''
    
    paths_txt = []
    class_list = ('bad','good')

    # заполняем наш список названиями файлов, выяснив длину списка
    for folder_name in class_list:
        count = len([f for f in os.listdir(os.path.join(path_dataset, folder_name)) if os.path.join(path_dataset, folder_name, f)])
    # заполняем список путей
        for j in range(count):
            path_txt = os.path.join(folder_name, f'{(j): 05}' + '.txt')
            print(f'{folder_name}: {(j): 05}')
            paths_txt.append(path_txt.replace(" ", ""))

    return paths_txt


def copy_dataset_random_add_csv() -> None:
    '''Функция, выполняющая копирование файлов с рандомными номерами в новый dataset и делающая csv-файл к нему'''
    path_dataset = os.path.abspath('dataset')
    paths_txt = find_path_txt(path_dataset)
    add_to_csv_and_to_dataset_random_number(path_dataset, paths_txt)


if __name__ == "__main__":

    path_dataset = os.path.abspath('dataset')
    paths_txt = find_path_txt(path_dataset)
    add_to_csv_and_to_dataset_random_number(path_dataset, paths_txt)