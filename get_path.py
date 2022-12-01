from simpleIterator import Iterator


def get_path(file_name, class_name):

    i = Iterator(file_name, class_name)
    for val in i:
        if (val != None):
            print(val)

    print('Задача выполнена')


if __name__ == "__main__":
    file_name = 'dataset.csv'
    class_name = 'good'
    get_path(file_name, class_name)