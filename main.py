import requests
from bs4 import BeautifulSoup
from time import sleep
import lxml
import random
from base64 import encode
import os


def create_dir():
    os.mkdir('dataset/')
    os.mkdir('dataset/bad')
    os.mkdir('dataset/good')


def site_read():
    list_films = []
    URL = "https://www.kinopoisk.ru/lists/movies/genre--horror/?b=films&ysclid=l9mbs12lhu196453911"
    html_text = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}).text
    soup = BeautifulSoup(html_text, 'lxml')

    films = soup.find_all('a', class_='base-movie-main-info_link__YwtP1')
    for i in films:
        film = i.get('href')
        list_films.append(film)

    with open('List_Films_2.txt', 'w') as file:
        for i in list_films:
          file.write('https://www.kinopoisk.ru' + f'{i}' + 'reviews\n')
    
          
def new_file(status):
    status = status.replace('/', '')
    file = open('List_Films_2.txt', 'r')
    line = file.readlines()
    file.close()
    with open('List_Films_' + status + '.txt', 'w') as file_2:
        for i in line:
            i = i.strip()
            i += '/ord/date/status/' + status + '/perpage/200\n'
            file_2.write(i)                  

def printim_lines(status):
    file = open('List_Films_' + status + '.txt', 'r')
    lines = file.readlines()
    file.close()
    j = 0

    while (j != 1000):
        for line in lines:
            line = line.strip()

            response = requests.get(line, headers={'User-Agent':'Mozilla/5.0'})
            print("#" * 100)
            print(response.text)
            print("#" * 100)
            result = response.content
            soup = BeautifulSoup(result, 'lxml')
            sleep(random.randint(60, 66))

            try:
                reviews = soup.find_all(class_='_reachbanner_')
            except AttributeError as e:
                print("Рецензия отсутствует")
                sleep(30)
                continue
            for review in reviews:
               num = '/000'
               if j >= 10 and j < 100:
                    num = '/00'
               if j >= 100 and j < 1001:
                num = '/0'
               with open('dataset/' + status +  num + str(j) + '.txt', 'a', encoding='utf-8') as file:
                        name = soup.find(class_='breadcrumbs__link')
                        text = name.text.strip()
                        file.write(text + '\n')
                        file.write(soup.find(class_='sub_title').text)
                        text_reviews = review.text.strip()
                        file.write(text_reviews)
                        print('...........Downland File №', j, '...........')
               j += 1
               
                
def main():
    #create_dir()
    #site_read()
    status = 'bad'
    #new_file(status)
    printim_lines(status)
    #status = 'good'
    #new_file(status)
   # printim_lines(status)


if __name__ == '__main__':
    main()