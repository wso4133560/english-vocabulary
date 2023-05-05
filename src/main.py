import sys
import requests
import os
from bs4 import BeautifulSoup
from playsound import playsound
from FileManager import FileManager

try:
    from PyQt5.QtCore import QSize
    from PyQt5.QtGui import QStandardItemModel, QStandardItem
    from PyQt5.QtWidgets import QListView, QWidget, QHBoxLayout, QLineEdit, \
        QPushButton, QApplication
except ImportError:
    from PySide2.QtCore import QSize
    from PySide2.QtGui import QStandardItemModel, QStandardItem
    from PySide2.QtWidgets import QListView, QWidget, QHBoxLayout, QLineEdit, \
        QPushButton, QApplication

def on_button_click(word):
    word = word.lower()
    # check ../mp3/下是否有此单词的mp3文件
    filePath = f"../mp3/{word}.mp3"
    if os.path.isfile(filePath):
        playsound(filePath)
        return
    # 没有就下载
    # 构造 URL
    url = f"https://www.macmillandictionary.com/dictionary/british/{word}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    }

    # 发送请求获取 HTML 页面
    response = requests.get(url, headers=headers)

    # 解析 HTML 页面
    soup = BeautifulSoup(response.content, "html.parser")

    audio = soup.find('span', {'class': 'sound audio_play_button dflex middle-xs'})
    audio_url = audio['data-src-mp3']

    # 下载 MP3 文件
    response = requests.get(audio_url, headers=headers)

    with open(filePath, "wb") as f:
        f.write(response.content)
    playsound(filePath)
    

class CustomWidget(QWidget):

    def __init__(self, text, note, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLineEdit(text, self))
        layout.addWidget(QLineEdit(note, self))
        button = QPushButton("发音")
        button.clicked.connect(lambda: on_button_click(text))
        layout.addWidget(button)

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)


class ListView(QListView):

    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        # 模型
        self._model = QStandardItemModel(self)
        self.setModel(self._model)

        fileManager = FileManager()
        words_list = fileManager.get_words_list()
        # 循环生成10个自定义控件
        for word in words_list:
            item = QStandardItem()
            self._model.appendRow(item)  # 添加item

            # 得到索引
            index = self._model.indexFromItem(item)
            widget = CustomWidget(word[0], word[1])
            item.setSizeHint(widget.sizeHint())  # 主要是调整item的高度
            # 设置自定义的widget
            self.setIndexWidget(index, widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ListView()
    w.resize(800, 500)

    w.show()
    sys.exit(app.exec_())