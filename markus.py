from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
import os
import numpy as np
import os.path
import pymorphy2
import regex as re
from nltk.corpus import stopwords
from pymystem3 import Mystem
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import string


def pos(word, morth=pymorphy2.MorphAnalyzer()):
    '''возвращает часть речи'''
    return morth.parse(word)[0].tag.POS


def strip_words(words: str) -> str:
    
    words_upd = []

    for word in words:
        word = re.sub(r'[^\pL\p{Space}]', '', word).lower()
        if word != '':
            words_upd.append(word)
    return words_upd


def lemmatize_for_class_mark(reviews_df: pd.DataFrame, class_mark: str) -> list:
    '''Обрабатываем слова из dataframe по метке класса'''
    reviews_class_mark_df = filtered_dataframe_class(reviews_df, 'class_mark', class_mark)
    return lemmatize(reviews_class_mark_df, 'text_review')


def lemmatize(reviews_df: pd.DataFrame, column_name: str) -> list:
    '''возвращает список лемматизированных слов'''
    text_nomalized = str()

    for i in range(len(reviews_df.index)):

        text = reviews_df.iloc[i]
        text = text[column_name]
        words = text.split()
        words = strip_words(words)

        for i in range(len(words)):
            text_nomalized += words[i]
            text_nomalized += ' '

    m = Mystem()
    lemmas = m.lemmatize(text_nomalized)

    lemmas_res = strip_words(lemmas)
    return lemmas_res


def lemmatizer_list(reviews_df: pd.DataFrame, column_name: str, class_name: str) -> list:
    '''лемматизация слов по метке класса'''
    output_lemma = []
    stopwords_ru = stopwords.words("russian")
    lemma = pymorphy2.MorphAnalyzer()

    functors_pos = {'CONJ', 'PREP', 'NPRO', 'PRCL'}
    for i in range(len(reviews_df)):
        if reviews_df['class_mark'][i] == class_name:

            for word in reviews_df[column_name][i].split():

                word = re.sub(r'[^\pL\p{Space}]', '', word).lower()
                part_speech = pymorphy2.MorphAnalyzer().parse(word)[0].tag.POS
                if part_speech not in functors_pos and word and word not in stopwords_ru:
                    output_lemma.append(lemma.parse(word)[0].normal_form)
    return output_lemma


def add_to_list(txt_name: list, text_reviews: list, name_class: list) -> list:
    '''возвращает два списка: один с отзывами, другой с меткой класса'''
    for i in range(2000):

        with open(txt_name[i], 'r', encoding='utf-8') as f:
            data = f.read()
            text_reviews.append(data)
            class_name = str(txt_name[i]).split('\\')[1]
            name_class.append(class_name)

    return text_reviews, name_class


def add_to_dataframe() -> pd.DataFrame:
    '''записывает в dataframe текст отзыва и метку класса в два столбца'''
    filename = "dataset.csv"
    text_reviews = []
    name_class = []
    txt_name = []
    data_dict = {}

    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if row[1] != 'Relative path':
                txt_name.append(str(row[1])[3:])

    text_reviews, name_class = add_to_list(txt_name, text_reviews, name_class)

    column_name = ['class_mark', 'text_review', 'count_words']
    data_dict[column_name[0]] = name_class
    data_dict[column_name[1]] = text_reviews
    reviews_df = pd.DataFrame(data_dict)
    return reviews_df


def list_words(reviews_df: pd.DataFrame,  class_name: str, column_name: str) -> list:
    '''возвращаем список слов'''
    words = []

    for i in range(len(reviews_df.index)):
        if reviews_df['class_mark'][i] == class_name:
            text = reviews_df.iloc[i]
            text = text[column_name]
            text = text.replace("\n", ' ')
            text = text.replace(",", "").replace('.', '.').replace("?", '').replace("!", "")
            text = text.lower()
            for word in text.split():
                words.append(word)

            words.sort()

    return words


def statistical_information(reviews_df: pd.DataFrame, column_name: str) -> pd.Series:
    '''возвращаем статистическую информацию 0 столбце'''
    return reviews_df[column_name].describe()


def filtered_dataframe_class(reviews_df: pd.DataFrame, column_name: str, class_name: str) -> pd.DataFrame:
    '''возвращаем обработанный по метке класса dataframe'''
    result = pd.DataFrame(reviews_df[reviews_df[column_name] == class_name])
    return result


def filtered_dataframe_word(reviews_df: pd.DataFrame, column_name: str, count: int) -> pd.DataFrame:
    '''возвращает обработанный по количествам слов dataframe'''
    result = pd.DataFrame(reviews_df[reviews_df[column_name] <= count])
    return result


def count_words_in_text(reviews_df: pd.DataFrame, column_name: str) -> list:
    '''возвращаем список c количеством слов в каждом отзыве'''
    count_words = []
    for i in range(len(reviews_df.index)):
        text = reviews_df.iloc[i]
        text = text[column_name]
        text = text.replace("\n", " ")
        text = text.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace("'", "")
        text = text.lower()
        words = text.split()
        words.sort()
        count_words.append(len(words))
    return count_words


def check_nan(reviews_df: pd.DataFrame, column_name:str) -> bool:
    '''Проверяем на пустоту в dataframe'''
    return reviews_df[column_name].isnull().values.any()



def main():

    column_name = ['class_mark', 'text_review', 'count_words']
    reviews_df = add_to_dataframe()
    count_word = count_words_in_text(reviews_df, column_name[1])
    reviews_df[column_name[2]] = pd.Series(count_word)
    print(reviews_df)
    stat = statistical_information(reviews_df, column_name[2])
    print(stat)
    filtered_reviews_df = filtered_dataframe_word(
        reviews_df, column_name[2], 100)
    print(filtered_reviews_df)
    reviews_df.to_csv('dataframe.csv')
    reviews_good_df = filtered_dataframe_class(reviews_df, column_name[0], 'good')
    reviews_bad_df = filtered_dataframe_class( reviews_df, column_name[0], 'bad')
    print(reviews_bad_df)
    print(reviews_good_df)

    stat_good = statistical_information(reviews_good_df, column_name[2])
    print('Для положительных отзывов:\n')
    print('Минимальное кол-во слов:', stat_good['min'])
    print('Максимальное кол-во слов:', stat_good['max'])
    print('Среднее кол-во слов:', stat_good['mean'])

    stat_bad = statistical_information(reviews_bad_df, column_name[2])
    print('Для отрицательных отзывов:\n')
    print('Минимальное кол-во слов:', stat_bad['min'])
    print('Максимальное кол-во слов:', stat_bad['max'])
    print('Среднее кол-во слов:', stat_bad['mean'])
        

def lemmatize(text) -> list:
    morph = pymorphy2.MorphAnalyzer()
    new_list = []
    table = str.maketrans(dict.fromkeys(string.punctuation))
    elem = text.translate(table)
    if elem is not None:
        list_words = elem.split()
    for word in list_words:
        p = morph.parse(word)[0]
        new_list.append(p.normal_form)
    return new_list

def create_histogram(reviews_df: pd.DataFrame, label: str) -> plt.Figure:

    dict = {}
    list = []
    reviews_df = reviews_df[reviews_df['class_mark'] == label][['text_review']]
    for text in reviews_df['text_review']:
        list_new = lemmatize(text)
    for word in list_new:
        if word not in dict.keys():
            dict[word] = list_new.count(word)
            list.append(list_new.count(word))
    return list, dict


if __name__ == "__main__":
    main()
   
    column_name = ['class_mark', 'text_review', 'count_words']
    reviews_df = add_to_dataframe()

    list, dict = create_histogram(reviews_df, 'good')

    plt.figure(figsize=(30, 10))
    plt.ylabel('Количество слов')
    plt.title('Гистограмма')

    new = []
    for elem in dict:
        print(elem)
        new.append(elem)
    plt.hist(list[:20], bins=len(list), color='blue', edgecolor='black')
    plt.xticks(np.arange(len(list[:20])), new[:20], rotation=90, horizontalalignment='left')

    plt.show()