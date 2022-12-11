import os
import csv
import shutil
import random


def add_to_csv_and_to_dataset_random_number(path_dataset, paths_txt):

    name_folder = "random_number_dataset"

    if not os.path.isdir(name_folder):
        os.mkdir(name_folder)

    path_random_number_dataset = os.path.abspath(name_folder)

    with open('random_number_dataset.csv', 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(["Absolute path", "Relative path", "Class"])

        for i in range (len(paths_txt)):
            class_txt = str(paths_txt[i]).split('\\')
            new_name = str(random.randint(0, 10000)).zfill(5) + '.txt'
            while os.path.isfile(new_name):
                new_name = str(random.randint(0, 10000)).zfill(5) + '.txt'
            writer.writerow([f'{path_dataset}\{ new_name }',
                  f'..\\random_number_dataset\{new_name}', f'{class_txt[1]}'])
            shutil.copyfile(path_dataset + str(paths_txt[i]), path_random_number_dataset + '\\' + new_name)


def find_path_txt(path_dataset):
    paths_txt = list()
    class_list = ('\\bad','\good')

    for folder_name in class_list:
        count = len([f for f in os.listdir(path_dataset + folder_name)
                    if os.path.join(path_dataset + folder_name, f)])

        for j in range(0, count):
            path_txt = folder_name + f'\\{(j): 05}' + '.txt'
            print(f'{folder_name}: {(j): 05}')
            paths_txt.append(path_txt.replace(" ", ""))

    return paths_txt


if __name__ == "__main__":

    path_dataset = os.path.abspath('dataset')
    paths_txt = find_path_txt(path_dataset)
    add_to_csv_and_to_dataset_random_number(path_dataset, paths_txt)