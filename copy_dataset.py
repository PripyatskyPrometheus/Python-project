import os
import csv
import shutil


def add_csv (path_dataset, paths_txt):
    
    with open('dataset_new.csv','w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(["Absolute path", "Relative path", "Class"])

        for i in range (1, len(paths_txt)):
            class_txt = str(paths_txt[i]).split('\\')
            class_txt = str(class_txt[1]).split('_')
            writer.writerow([f'{ (path_dataset + str(paths_txt[i])).replace(" ","")}', f'..\\dataset{(str(paths_txt[i])).replace(" ","")}', f'{class_txt[0]}'])

            
def copy_dataset_new_dataset(path_dataset, path_txt_old, path_txt_new):

    name_folder = "dataset_new"

    if not os.path.isdir(name_folder):
        os.mkdir(name_folder)
    
    for i in range(1, len(path_txt_old)):
        shutil.copyfile(path_dataset + str(path_txt_old[i]), name_folder + str(path_txt_new[i]))
    

def find_path_txt (path_dataset, delimiter):
    paths_txt = list()
    class_list = ('\\good', '\\bad')

    for folder_name in class_list:
        count = len([f for f in os.listdir(path_dataset + folder_name) if os.path.join(path_dataset + folder_name, f)])

        for j in range (0, count):
            path_txt = folder_name + delimiter +  f'{(j): 05}' + '.txt'
            print(f'{folder_name}: {(j): 05}')
            paths_txt.append(path_txt.replace(" ",""))
    
    return paths_txt


if __name__ == "__main__":
 
    path_laba_2 = os.getcwd()
    path_dataset = os.path.abspath('dataset')
    path_txt_old = find_path_txt (path_dataset, '\\')
    path_txt_new = find_path_txt (path_dataset, '_')
    copy_dataset_new_dataset(path_dataset, path_txt_old, path_txt_new)
    add_csv (path_dataset, path_txt_new)

    print("Задача выполнена")