import sys
import requests
import os
import csv
import threading
import random

from read_word import read_word
from bs4 import BeautifulSoup

from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QApplication, QAction, QMainWindow, QMenuBar, QMenu, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAbstractItemView, QDialog, QLabel, QButtonGroup, QRadioButton, QMessageBox

from read_word import read_word

class SingleChoiceDialog(QDialog):
    def __init__(self, csv_path):
        super().__init__()
        self.words_meanings = []
        self.words_list = self.load_words(csv_path)

        # 显示剩余的单词量
        self.list_label = QLabel()

        self.option_buttons = []
        self.button_group = QButtonGroup()

        for i in range(0, 4):
            button = QRadioButton()
            self.option_buttons.append(button)
            self.button_group.addButton(button)

        self.submit_button = QPushButton('提交')
        self.submit_button.clicked.connect(self.get_answer)

        self.read_button = QPushButton('朗读')
        self.read_button.clicked.connect(self.read_word)

        layout = QVBoxLayout()
        layout.addWidget(self.list_label)

        for button in self.option_buttons:
            layout.addWidget(button)

        layout.addWidget(self.submit_button)
        layout.addWidget(self.read_button)
        self.setLayout(layout)

        self.get_random_options()

        self.resize(400, 300)

    def load_words(self, csv_path):
        csvfile = open(csv_path, newline='', encoding='utf-8')
        reader = csv.reader(csvfile)
        words_list = dict()
        for word in reader:
            words_list[word[0]] = word[1]
            self.words_meanings.append(word[1])
        return words_list

    def get_answer(self):
        if self.button_group.checkedButton():
            answer = self.option_buttons.index(self.button_group.checkedButton())
            if answer == self.answer_pos:
                reply = QMessageBox.question(self, 'Message', self.selected_word, QMessageBox.Yes)
                self.get_random_options()
            else:
                reply = QMessageBox.question(self, 'Message', self.selected_word, QMessageBox.Yes)
        else:
            reply = QMessageBox.question(self, 'Message', '请选择一个选项', QMessageBox.Yes)

    def get_random_options(self):
        keys = list(self.words_list.keys())
        if None == keys:
            return
        random_key = random.choice(keys)

        self.selected_word = random_key
        self.selected_meaning = self.words_list[random_key]

        del self.words_list[random_key]

        len_words = len(self.words_list)

        self.list_label.setText("还剩余{}单词:".format(len_words))
        self.answer_pos = random.randint(0, 3)

        repeat = dict()

        for i in range(0, 4):
            if i == self.answer_pos:
                self.option_buttons[i].setText(self.selected_meaning)
            else:
                while True:
                    random_item = random.choice(self.words_meanings)

                    if repeat.get(random_item):
                        continue

                    if random_item != self.selected_meaning:
                        self.option_buttons[i].setText(random_item)
                        repeat[random_item] = 0
                        break
    
    def read_word(self):
        read_word(self.selected_word)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建菜单栏
        menu_bar = QMenuBar()
        english_classes = QMenu("English classes", menu_bar)
        menu_bar.addMenu(english_classes)

        # 添加fruit的子菜单
        fruit_action = QAction("fruit", self)
        fruit_action.triggered.connect(self.on_fruit)
        english_classes.addAction(fruit_action)

        # 将菜单栏添加到主窗口上
        self.setMenuBar(menu_bar)

    def on_fruit(self):
        dialog_view = SingleChoiceDialog("../resource/fruit.csv")
        #self.layout(dialog_view)
        dialog_view.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("listen english")

    window = MainWindow()
    window.resize(800, 600)

    window.show()
    sys.exit(app.exec_())