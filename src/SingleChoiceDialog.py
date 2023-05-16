import sys
import random
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QButtonGroup, QRadioButton, QPushButton

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
        self.submit_button.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for button in self.option_buttons:
            layout.addWidget(button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)
        
        self.get_random_options()

    def get_answer(self):
        if self.button_group.checkedButton():
            answer = self.option_buttons.index(self.button_group.checkedButton())
        else:
            answer = -1
        return answer
    
    def get_random_options(self):
        # 获取所有key组成的列表
        keys = list(self.words.keys())
        # 从key列表中随机选择一个key
        random_key = random.choice(keys)
        self.question_label.setText("请选择{}单词的意思:".format(random_key))
        random_value = self.words[random_key]

        values = list(self.words.values())
        self.answer_pos = random.randint(0, 4)
        for i in range(0, 4):
            if i == self.answer_pos:
                self.option_buttons[i].setText(random_value)
            else:
                value = random.choice(values)
                while value == random_value:
                    value = random.choice(values)
                self.option_buttons[i].setText(value)
    