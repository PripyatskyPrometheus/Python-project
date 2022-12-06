import requests
from bs4 import BeautifulSoup
from time import sleep
import lxml
import random
from base64 import encode
import os

#  Создаём папку dataset и её подпапки bad и good
def create_dir():
    os.mkdir('dataset')
    os.mkdir(os.join('dataset', 'bad')) # os.join()
    os.mkdir(os.join('dataset', 'good'))


def site_read():
    list_films = []
    URL = "https://www.kinopoisk.ru/lists/movies/genre--horror/?b=films&ysclid=l9mbs12lhu196453911"
    html_text = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}).text
    soup = BeautifulSoup(html_text, 'lxml')
    #  Выгружаем 50 фильмов хорроров и добавляем их в наш список  list_films
    films = soup.find_all('a', class_='base-movie-main-info_link__YwtP1')
    for i in films:
        film = i.get('href')
        list_films.append(film)
    #  Создаём и заполняем папку ссылками на страницы с рецензиями
    with open('List_Films_2.txt', 'w') as f:
        for i in list_films:
          f.write('https://www.kinopoisk.ru' + f'{i}' + 'reviews\n')
    
          
def new_file(status):
    #  Читаем файл с фильмами
    status = status.replace('/', '')
    file = open('List_Films_2.txt', 'r')
    line = file.readlines()
    file.close()
    #  Создаём файл со страницами на плохие или хорошие рецензии
    with open('List_Films_' + status + '.txt', 'w') as file_2:
        for i in line:
            i = i.strip()
            i += os.join('ord', 'date', 'status',  status, 'perpage', '200\n')
            file_2.write(i)                  

def printim_lines(status):
    #  Читаем файл с плохими илихорошими рецензиями
    f = open('List_Films_' + status + '.txt', 'r')
    lines = f.readlines()
    f.close()
    j =0
    #  Прходимся по строкам файла с плохими или хорошими отзывами
    while (j != 1000):
        for line in lines:
            line = line.strip()
            #  Выгружаем и выводим в консоль html код, чтобы определить, капча или нет
            response = requests.get(line, headers={'User-Agent':'Mozilla/5.0'})
            print("#" * 100)
            print(response.text)
            print("#" * 100)
            result = response.content
            soup = BeautifulSoup(result, 'lxml')
            sleep(random.randint(60, 66))
            #  Выгружаем текст рецензиями и задаём исключение
            try:
                reviews = soup.find_all(class_='_reachbanner_')
            except AttributeError as e:
                print("Рецензии отсутствуют")
                sleep(30)
                continue
            #  Записываем отзыв в dataset
            for review in reviews:
                if j > 999:
                    break
                #  Определяем количество нулей перед номером
                num = str(j)
                number = num.zfill(4)
                #  создаём подпапку дляотдельного отзыва
                strok = os.join('dataset', status, number + '.txt')
                with open(strok, 'a', encoding='utf-8') as f:
                    name = soup.find(class_='breadcrumbs__link') #Название фильма
                    text = name.text.strip()
                    f.write(text + '\n')
                    #  Заголовок
                    f.write(soup.find(class_='sub_title').text + '\n') 
                    #  Перерабатываем
                    text_reviews = review.text.strip() 
                    f.write(text_reviews)
                    print('...........Downland File №', j, '...........')
                j += 1
                if j == 1000:
                    break
            break
                
def main():
    #create_dir()
    #site_read()
    status = 'bad'
    #new_file(status)
    #printim_lines(status)
    status = 'good'
    #new_file(status)
    #printim_lines(status)


if __name__ == '__main__':
    main()