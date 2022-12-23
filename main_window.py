import os
import sys
import codecs
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, QObject
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QFileDialog, QMessageBox, QDesktopWidget, QTextEdit, QHBoxLayout, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

import work
import copy_dataset
import random_dataset
import get_path
from simpleIterator import Simple_Iterator_1
import typing


class CreateDataset(QThread):
    def __init__(self, parent: typing.Optional[QObject]) -> None:
        super().__init__(parent)

    def run(self):
        copy_dataset.copy_dataset_add_csv()


class CreateDatasetRandom(QThread):
    def __init__(self, parent: typing.Optional[QObject]) -> None:
        super().__init__(parent)

    def run(self):
        random_dataset.copy_dataset_random_add_csv()

class CreateSCV(QThread):
    def __init__(self, parent: typing.Optional[QObject]) -> None:
        super().__init__(parent)

    def run(self):
        work.create_csv()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.create_csv = CreateSCV(self)
        self.create_new_dataset = CreateDataset(self)
        self.create_random_number_dataset = CreateDatasetRandom(self)
        self.iterator_good = Simple_Iterator_1(os.path.abspath('dataset'), "good")
        self.iterator_bad = Simple_Iterator_1(os.path.abspath('dataset'), "bad")
        self.path_dataset = ""
        self.label = QLabel(self)
        self.initUI()

    def Set_Label(self, x: int, y: int, text: str) -> None:
        '''Устанавливаем "этикетки" по заданным коардинатам'''

        reviews = QLabel(text, self)
        reviews.resize(reviews.sizeHint())
        reviews.move(x, y)

    def Set_LineEdit(self, x: int, y: int) -> QTextEdit:
        '''Устанвливаем "текстовый редактор" по заданным коардинатам'''

        reviews_edit = QTextEdit(' ', self)
        reviews_edit.resize(400, 500)
        reviews_edit.setReadOnly(True)
        reviews_edit.move(x, y)
        return reviews_edit

    def Set_Button(self, x: int, y: int, text: str, function) -> None:
        '''Устанвливаем "конпку" на форму по заданным координатам'''

        btn = QPushButton(text, self)
        btn.resize(btn.sizeHint())
        btn.move(x, y)
        btn.clicked.connect(function)
        return btn

    def Set_Widgets(self) -> None:
        '''Показываем кнопки и передаём им функции лицом'''

        self.Set_Label(150, 50, 'Хороший отзыв')
        self.Set_Label(700, 50, 'Плохой отзыв')

        self.Line_Edit_Good = self.Set_LineEdit(50, 90)
        self.Line_Edit_Bad = self.Set_LineEdit(500, 90)

        self.Set_Button(100, 610, 'Посмотреть следующий хороший отзыв', self.On_Next_Good)

        self.Set_Button(610, 610, 'Посмотреть следующий плохой отзыв', self.On_Next_Bad)

        self.Set_Button(1000, 90, 'Создать аннотацию для dataset', self.On_Create_Csv_Dataset_Button)
        self.Set_Button(1000, 140, 'Создать new_dataset и аннотацию', self.On_Create_Copy_Dataset_Button)
        self.Set_Button(1000, 190, 'Создать random_number_dataset и аннотацию ', self.On_Create_Dataset_Random_Button)

    def On_Next_Good(self) -> None:
        '''Берём следующий хороший отзыв'''
        if self.path_dataset != '':
            
            new =  self.iterator_good.__next__()
            print(new)
            with open(new, 'r', 'utf-8') as f:
                self.review = f.read()
                self.label.setText(self.review)

    def On_Next_Bad(self) -> None:
        '''Берём следующий плохой отзыв'''
        if self.path_dataset != '':
            new = self.iterator_bad.__next__()
            print(new)
            with open(new, 'r', 'utf-8') as f:
                self.review = f.read()
                self.label.setText(self.review)

    def On_Create_Csv_Dataset_Button(self) -> None:
        '''Создаём csv-файла dataset'''
        while self.path_dataset == "":
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку исходного dataset')
            self.path_dataset = 'dataset'
            self.create_csv.start()

    def On_Create_Copy_Dataset_Button(self) -> None:
        '''Метод для создания сopy_dataset и его csv-файла'''
        if self.path_dataset != "":
            self.create_new_dataset.start()

    def On_Create_Dataset_Random_Button(self) -> None:
        '''Метод для создания random_number_dataset и его csv-файла'''
        if self.path_dataset != "":
            self.create_random_number_dataset.start()

    def initUI(self) -> None:

        self.resize(1400, 700)
        self.center()
        self.Set_Widgets()
        self.msg = QMessageBox()

        self.setWindowIcon(QIcon('.text'))

    def center(self) -> None:

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    '''Создаём оконного приложения'''
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())