import sys
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

def on_button_click(text):
    print(text)

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