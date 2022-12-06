import scv
import os.path


def add_in_csv (path_dataset, paths_txt):

    with open('dataset.csv','w+', encoding='utf-8', newline='') as f:
        writer = scv.writer(f, delimiter=' ')
        writer.writerow(['Absolute path', 'Relative path', 'Class'])

        for i in range (1, len(paths_txt)):
            class_txt = str(paths_txt[i]).split('\\')
            print(class_txt[1])
            writer.writerow([f'{ (path_dataset + str(paths_txt[i])).replace(" ","")}', f'..\\dataset{(str(paths_txt[i])).replace(" ","")}', f'{class_txt[0]}'])
            print(i)

        
def find_path_txt (path_dataset):
    paths_txt = list()
    class_list = ('\\good', '\\bad')

    for folder_name in class_list:
        count = len([f for f in os.listdir(path_dataset + folder_name) if os.path.join(path_dataset + folder_name, f)])

        for j in range (0, count):
            path_txt = folder_name + f'\\{(j): 05}' + '.txt'
            print(f'{folder_name}: {(j): 05}')
            paths_txt.append(path_txt.replace(" ",""))
    
    return paths_txt


if __name__ == "__main__":
    
    path_dataset = os.path.abspath('dataset')
    paths_txt = find_path_txt(path_dataset)
    add_in_csv (path_dataset, paths_txt)
    
    print("Задача выполнена")