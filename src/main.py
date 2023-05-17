import sys
import requests
import os
import csv
import threading

from read_word import read_word
from bs4 import BeautifulSoup

from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QApplication, QAction, QMainWindow, QMenuBar, QMenu, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QAbstractItemView

from SingleChoiceDialog import SingleChoiceDialog

class ReadCycleThread(QThread):
    def __init__(self, table_view):
        super().__init__()
        self.table_view = table_view
        self.finished_signal = pyqtSignal()

    def run(self):
        words = self.table_view.get_words()
        row = 0
        for word in words:
            self.table_view.select_and_scroll_to_row(row)
            row = row + 1
            read_word(word)

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
        self.words = []
        self.words_list = dict()
        self.row = 0
        self.initData(filePath)  # 初始化模拟数据

    def onDoubleClick(self, index):
        if 0 == index.column():
            read_word(index.data())

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
        self.row = 0
        for word in reader:
            self.words.append(word[0])
            self.words_list[word[0]] = word[1]
            pos = word[1].find("vi.")
            self.myModel.setItem(self.row, 0, QStandardItem(word[0]))
            self.myModel.setItem(self.row, 1, QStandardItem(word[1]))
            self.row = self.row + 1

        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 500)

    def get_words(self):
        return self.words

    def get_words_list(self):
        return self.words_list

    def get_lines(self):
        return self.row

    def select_and_scroll_to_row(self, row_index):
        # 获取当前选中行的模型
        selection_model: QItemSelectionModel = self.selectionModel()
        # 将选中行设置为row_index
        index = self.model().index(row_index, 0, QModelIndex())
        selection_model.select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        # 将选中行滚动到可见区域
        self.scrollTo(index, QAbstractItemView.PositionAtTop)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建菜单栏
        menu_bar = QMenuBar()

        # 添加TableView的菜单
        english_classes = QMenu("English classes", menu_bar)
        menu_bar.addMenu(english_classes)

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

        # 添加TableView的菜单
        n_classes = QMenu("名词", menu_bar)
        menu_bar.addMenu(n_classes)

        # 添加annimal的子菜单
        annimal_action = QAction("annimal", self)
        annimal_action.triggered.connect(self.on_annimal)
        n_classes.addAction(annimal_action)

        # 添加vegetable的子菜单
        vegetable_atction = QAction("vegetable", self)
        vegetable_atction.triggered.connect(self.on_vegetable)
        n_classes.addAction(vegetable_atction)

        # 添加fruit的子菜单
        fruit_atction = QAction("fruit", self)
        fruit_atction.triggered.connect(self.on_fruit)
        n_classes.addAction(fruit_atction)

        # 添加metal的子菜单
        metal_atction = QAction("metal", self)
        metal_atction.triggered.connect(self.on_metal)
        n_classes.addAction(metal_atction)

        # 词汇
        root_prefix_suffix = QMenu("root-prefix-suffix", menu_bar)
        menu_bar.addMenu(root_prefix_suffix)

        # 添加root的子菜单
        root_action = QAction("root", self)
        root_action.triggered.connect(self.on_root)
        root_prefix_suffix.addAction(root_action)

        # 添加prefix的子菜单
        prefix_action = QAction("prefix", self)
        prefix_action.triggered.connect(self.on_prefix)
        root_prefix_suffix.addAction(prefix_action)

        # 将菜单栏添加到主窗口上
        self.setMenuBar(menu_bar)

    def closeEvent(self, event):
        # 停止所有的线程
        self.thread.requestInterruption()
        self.thread.finished_signal.disconnect(self.on_thread_finished)
        self.thread.wait()
        event.accept()

    def on_thread_finished(self):
        self.button.setEnabled(True)

    def read_words_by_cycle(self, table_view):
        self.thread = ReadCycleThread(table_view)
        self.thread.start()

    def question_dialog(self, table_view):
        dialog = SingleChoiceDialog(table_view.get_words_list())
        dialog.exec_()

    def layout(self, table_view):
        # 创建一个QPushButton
        button = QPushButton("循环朗诵")
        question_button = QPushButton("单项选择对话框")

        button.clicked.connect(lambda: self.read_words_by_cycle(table_view))
        question_button.clicked.connect(lambda: self.question_dialog(table_view))

        # 创建一个水平布局并将按钮添加到该布局中
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addWidget(question_button)
        button_layout.addStretch()

        # 创建一个垂直布局并将table_view和button_layout添加到该布局中
        main_layout = QVBoxLayout()
        main_layout.addWidget(table_view)
        main_layout.addLayout(button_layout)

        # 创建一个QWidget并将垂直布局设置为其布局
        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def on_medical(self):
        table_view = TableView("../resource/medical.csv")
        self.layout(table_view)

    def on_adj(self):
        table_view = TableView("../resource/adj.csv")
        self.layout(table_view)

    def on_adv(self):
        table_view = TableView("../resource/adv.csv")
        self.layout(table_view)

    def on_vi(self):
        table_view = TableView("../resource/vi.csv")
        self.layout(table_view)

    def on_vt(self):
        table_view = TableView("../resource/vt.csv")
        self.layout(table_view)

    def on_annimal(self):
        table_view = TableView("../resource/annimal.csv")
        self.layout(table_view)

    def on_vegetable(self):
        table_view = TableView("../resource/vegetable.csv")
        self.layout(table_view)

    def on_fruit(self):
        table_view = TableView("../resource/fruit.csv")
        self.layout(table_view)

    def on_metal(self):
        table_view = TableView("../resource/metal.csv")
        self.layout(table_view)

    def on_root(self):
        table_view = TableView("../resource/root.csv")
        self.layout(table_view)

    def on_prefix(self):
        table_view = TableView("../resource/prefix.csv")
        self.layout(table_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("english")

    window = MainWindow()
    window.resize(800, 600)

    window.show()
    sys.exit(app.exec_())
