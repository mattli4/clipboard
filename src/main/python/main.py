from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import PySide2
from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import (QAction, QApplication, QGridLayout,
                               QMainWindow, QPushButton, QWidget, QComboBox, QInputDialog, QFileDialog)

from ctrl import ControlCV
import pyHook

class MainWindow(QMainWindow):
    def __init__(self):
        self.ctrlcv = ControlCV()
        self.hm = pyHook.HookManager()
        QMainWindow.__init__(self)
        self.setWindowTitle("ClipBoard")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_from_file)
        self.file_menu.addAction(load_action)
        main_widget = QWidget()
        layout = QGridLayout()
        main_widget.setLayout(layout)
        self.combo_box = QComboBox()
        self.combo_box.activated.connect(self.ctrl_c)
        layout.addWidget(self.combo_box, 1, 1, 1, 4)
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.get_item_from_input)
        layout.addWidget(add_button, 1, 5, 1, 1)
        del_button = QPushButton("Delete")
        del_button.clicked.connect(self.remove_item_from_list)
        layout.addWidget(del_button, 1, 6, 1, 1)
        mod_button = QPushButton("Modify")
        mod_button.clicked.connect(self.modify_selected_item)
        layout.addWidget(mod_button, 1, 7, 1, 1)
        self.setCentralWidget(main_widget)
        self.hm.KeyUp = self.onKeyboardEvent
        self.hm.HookKeyboard()


    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    def get_item_from_input(self):
        value, ok = QInputDialog.getMultiLineText(self, "please input text", "", "")
        if ok and value not in self.ctrlcv.CLIPBOARD:
            self.combo_box.addItem(value)
            self.ctrlcv.CLIPBOARD.append(value)

    def remove_item_from_list(self):
        cur_value = self.combo_box.currentText()
        if cur_value is not '':
            item_index = self.ctrlcv.CLIPBOARD.index(cur_value)
            self.ctrlcv.CLIPBOARD.remove(cur_value)
            self.combo_box.removeItem(item_index)

    def modify_selected_item(self):
        cur_value = self.combo_box.currentText()
        value, ok = QInputDialog.getMultiLineText(self, "please input text", "", cur_value)
        if ok and value not in self.ctrlcv.CLIPBOARD:
            self.combo_box.addItem(value)
            self.ctrlcv.CLIPBOARD.append(value)
            self.remove_item_from_list()

    def load_from_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "load file", self.ctrlcv.cwd, "Text Files (*.txt)")
        self.ctrlcv.load_from_file_by_line(filename)
        self.combo_box.clear()
        for item in self.ctrlcv.CLIPBOARD:
            self.combo_box.addItem(item)

    def onKeyboardEvent(self, event):
        print(str(event.Ascii))
        if event.Ascii == 3:
            print('c up')
        return True

    def ctrl_c(self):
        clipboard = QApplication.clipboard()
        text = self.combo_box.currentText()
        clipboard.setText(text)

if __name__ == "__main__":
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    window = MainWindow()
    window.resize(600, 30)
    window.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
