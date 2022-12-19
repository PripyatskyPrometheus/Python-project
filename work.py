import csv
import os
from typing import List


def add_in_csv (path_dataset: str, paths_txt: List[str]) -> None:
    
    '''Создаёт и записывает файл аннотацию dataseta'''
    #создаём  или открываем файл аннотацию для заполнения
    with open('dataset.csv', 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["Absolute path", "Relative path", "Class"])
        
        #проходимся по нашим именам и записываем их в аннотацию
        for i in range (len(paths_txt)):
            class_txt = os.path.join(str(paths_txt[i]))
            class_name = 'bad'
            if class_txt [0 : 4] == ('good'):
                class_name = 'good'
            writer.writerow([(f'{os.path.join(path_dataset, str(paths_txt[i])).replace(" ","")}'), 
                os.path.join('..', 'dataset', f'{(str(paths_txt[i])).replace(" ","")}'), f'{class_name}'])

        
def find_path_txt (path_dataset: str) -> List[str]:
    '''Функция формирует и возвращает список из путей к текстовым файлам'''
    
    paths_txt = []
    class_list = ('bad', 'good')

    for folder_name in class_list:
        count = len([f for f in os.listdir(os.path.join(path_dataset, folder_name)) if os.path.join(path_dataset, folder_name, f)])

        for j in range(count):
            path_txt = os.path.join(folder_name, f'{(j): 05}' + '.txt')
            print(f'{folder_name}: {(j): 05}')
            paths_txt.append(path_txt)
    
    return paths_txt

def Create_csv(path_dataset: str) -> None:
    '''Вызов функций для поиска путей файлов и создания csv-файла'''
    paths_txt = find_path_txt(path_dataset)
    add_in_csv(path_dataset, paths_txt)

if __name__ == "__main__":
    
    path_dataset = os.path.abspath('dataset')
    paths_txt = find_path_txt(path_dataset)
    add_in_csv (path_dataset, paths_txt)