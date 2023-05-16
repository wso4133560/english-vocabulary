import sys
import random
from read_word import read_word
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QButtonGroup, QRadioButton, QPushButton, QMessageBox

class SingleChoiceDialog(QDialog):
    def __init__(self, words):
        super().__init__()
        self.words = words

        self.question_label = QLabel()
        self.option_buttons = []
        self.button_group = QButtonGroup()

        for i in range(0, 4):
            button = QRadioButton()
            self.option_buttons.append(button)
            self.button_group.addButton(button)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.get_answer)
        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for button in self.option_buttons:
            layout.addWidget(button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.get_random_options()

        self.resize(400, 300)

    def get_answer(self):
        if self.button_group.checkedButton():
            answer = self.option_buttons.index(self.button_group.checkedButton())
            if answer == self.answer_pos:
                reply = QMessageBox.question(self, 'Message', '选择正确', QMessageBox.Yes)
                self.get_random_options()
            else:
                reply = QMessageBox.question(self, 'Message', '选择错误', QMessageBox.Yes)
        else:
            reply = QMessageBox.question(self, 'Message', '请选择一个选项', QMessageBox.Yes)

    def get_random_options(self):
        # 获取所有key组成的列表
        keys = list(self.words.keys())
        # 从key列表中随机选择一个key
        random_key = random.choice(keys)
        self.question_label.setText("请选择{}单词的意思:".format(random_key))
        random_value = self.words[random_key]

        values = list(self.words.values())
        self.answer_pos = random.randint(0, 3)

        false_values = set()
        for i in range(0, 4):
            if i == self.answer_pos:
                self.option_buttons[i].setText(random_value)
            else:
                value = random.choice(values)
                while value == random_value or value in false_values:
                    value = random.choice(values)
                self.option_buttons[i].setText(value)
                false_values.add(value)
        read_word(random_key)
