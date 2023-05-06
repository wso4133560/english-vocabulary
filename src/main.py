import sys
import requests
import os
import csv
from bs4 import BeautifulSoup
from playsound import playsound
from gtts import gTTS

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QStandardItemModel, QStandardItem
    from PyQt5.QtWidgets import QTableView, QApplication, QAction, QMainWindow, QMenuBar, QMenu
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QStandardItemModel, QStandardItem
    from PySide2.QtWidgets import QTableView, QApplication, QAction

def on_button_click(word):
    word = word.lower()
    # check ../mp3/下是否有此单词的mp3文件
    filePath = f"../mp3/{word}.mp3"
    if os.path.isfile(filePath):
        playsound(filePath)
        return

    language = 'en'

    speech = gTTS(text=word, lang=language, slow=True)
    speech.save(filePath)
    playsound(filePath)

class TableView(QTableView):

    def __init__(self, filePath, parent=None):
        super(TableView, self).__init__(parent)
        self.resize(800, 600)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # 右键菜单
        self.setEditTriggers(self.NoEditTriggers)  # 禁止编辑
        self.doubleClicked.connect(self.onDoubleClick)
        self.addAction(QAction("复制", self, triggered=self.copyData))
        self.myModel = QStandardItemModel()  # model
        self.initHeader()  # 初始化表头
        self.setModel(self.myModel)
        self.initData(filePath)  # 初始化模拟数据

    def onDoubleClick(self, index):
        if 0 == index.column():
            on_button_click(index.data())

    def keyPressEvent(self, event):
        super(TableView, self).keyPressEvent(event)
        # Ctrl + C
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.copyData()

    def copyData(self):
        count = len(self.selectedIndexes())
        if count == 0:
            return
        if count == 1:  # 只复制了一个
            QApplication.clipboard().setText(
                self.selectedIndexes()[0].data())  # 复制到剪贴板中
            return
        rows = set()
        cols = set()
        for index in self.selectedIndexes():  # 得到所有选择的
            rows.add(index.row())
            cols.add(index.column())
            # print(index.row(),index.column(),index.data())
        if len(rows) == 1:  # 一行
            QApplication.clipboard().setText("\t".join(
                [index.data() for index in self.selectedIndexes()]))  # 复制
            return
        if len(cols) == 1:  # 一列
            QApplication.clipboard().setText("\r\n".join(
                [index.data() for index in self.selectedIndexes()]))  # 复制
            return
        mirow, marow = min(rows), max(rows)  # 最(少/多)行
        micol, macol = min(cols), max(cols)  # 最(少/多)列
        print(mirow, marow, micol, macol)
        arrays = [
            [
                "" for _ in range(macol - micol + 1)
            ] for _ in range(marow - mirow + 1)
        ]  # 创建二维数组(并排除前面的空行和空列)
        print(arrays)
        # 填充数据
        for index in self.selectedIndexes():  # 遍历所有选择的
            arrays[index.row() - mirow][index.column() - micol] = index.data()
        print(arrays)
        data = ""  # 最后的结果
        for row in arrays:
            data += "\t".join(row) + "\r\n"
        print(data)
        QApplication.clipboard().setText(data)  # 复制到剪贴板中

    def initHeader(self):
        self.myModel.setHorizontalHeaderItem(0, QStandardItem("单词"))
        self.myModel.setHorizontalHeaderItem(1, QStandardItem("词意"))

    def initData(self, filePath):
        csvfile = open(filePath, newline='', encoding='utf-8')
        reader = csv.reader(csvfile)
        row = 0
        for word in reader:
            pos = word[1].find("vi.")
            self.myModel.setItem(row, 0, QStandardItem(word[0]))
            self.myModel.setItem(row, 1, QStandardItem(word[1]))
            row = row + 1

        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 500)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建菜单栏
        menu_bar = QMenuBar()

        # 添加TableView的菜单
        english_classes = QMenu("English classes", menu_bar)
        menu_bar.addMenu(english_classes)

        # 添加annimal的子菜单
        annimal_action = QAction("annimal", self)
        annimal_action.triggered.connect(self.on_annimal)
        english_classes.addAction(annimal_action)

        # 添加medical的子菜单
        medical_action = QAction("medical", self)
        medical_action.triggered.connect(self.on_medical)
        english_classes.addAction(medical_action)        

        # 添加adj的子菜单
        adj_action = QAction("adj", self)
        adj_action.triggered.connect(self.on_adj)
        english_classes.addAction(adj_action)

        # 添加adv的子菜单
        adv_action = QAction("adv", self)
        adv_action.triggered.connect(self.on_adv)
        english_classes.addAction(adv_action) 

        # 添加vi的子菜单
        vi_action = QAction("vi", self)
        vi_action.triggered.connect(self.on_vi)
        english_classes.addAction(vi_action) 

        # 添加vt的子菜单
        vt_action = QAction("vt", self)
        vt_action.triggered.connect(self.on_vt)
        english_classes.addAction(vt_action) 

        # 将菜单栏添加到主窗口上
        self.setMenuBar(menu_bar)

    def on_annimal(self):
        table_view = TableView("../resource/annimal.csv")
        window.setCentralWidget(table_view)
        table_view.show()

    def on_medical(self):
        table_view = TableView("../resource/medical.csv")
        window.setCentralWidget(table_view)
        table_view.show()

    def on_adj(self):
        table_view = TableView("../resource/adj.csv")
        window.setCentralWidget(table_view)
        table_view.show()

    def on_adv(self):
        table_view = TableView("../resource/adv.csv")
        window.setCentralWidget(table_view)
        table_view.show()

    def on_vi(self):
        table_view = TableView("../resource/vi.csv")
        window.setCentralWidget(table_view)
        table_view.show()

    def on_vt(self):
        table_view = TableView("../resource/vt.csv")
        window.setCentralWidget(table_view)
        table_view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("english")

    window = MainWindow()
    window.resize(800, 600)

    window.show()
    sys.exit(app.exec_())
