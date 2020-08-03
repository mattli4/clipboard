from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import PySide2
from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import (QAction, QApplication, QGridLayout,
                               QMainWindow, QWidget, QLabel, QInputDialog, QFileDialog, QMenu)

from ctrl import ControlCV


class MainWindow(QMainWindow):
    def __init__(self):
        self.ctrlcv = ControlCV()
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
        self.clip_panel = [QLabel('') for i in range(9)]
        for i in range(9):
            self.clip_panel[i].setText('')
            self.clip_panel[i].setStyleSheet("border:0.51px solid grey;")
            layout.addWidget(self.clip_panel[i], int(i/3), i % 3, 1, 1)
        self.setCentralWidget(main_widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    def get_item_from_input(self):
        value, ok = QInputDialog.getMultiLineText(self, "please input text", "", "")
        if ok and value not in self.ctrlcv.CLIPBOARD:
            self.combo_box.addItem(value)
            self.ctrlcv.CLIPBOARD.append(value)

    def load_from_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "load file", self.ctrlcv.cwd, "Text Files (*.txt)")
        self.ctrlcv.load_from_file_by_line(filename)
        self.combo_box.clear()
        for item in self.ctrlcv.CLIPBOARD:
            self.combo_box.addItem(item)

    def mouseReleaseEvent(self, event:PySide2.QtGui.QMouseEvent):
        if event.button() == Qt.LeftButton:
            p = event.pos()
            clip_panel = self.childAt(p)
            clipboard = QApplication.clipboard()
            if hasattr(clip_panel, 'text'):
                text = clip_panel.text()
                clipboard.setText(text)

    def contextMenuEvent(self, event):
        clip_panel_menu = QMenu(self)
        clear_action = clip_panel_menu.addAction("Clear")
        edit_action = clip_panel_menu.addAction("Edit")
        action = clip_panel_menu.exec_(self.mapToGlobal(event.pos()))
        p = event.pos()
        clip_panel = self.childAt(p)
        if action == clear_action:
            clip_panel.setText('')
        elif action == edit_action:
            if hasattr(clip_panel, 'text'):
                cur_value = clip_panel.text()
                value, ok = QInputDialog.getMultiLineText(self, "please input text", "", cur_value)
                if ok:
                    clip_panel.setText(value)

if __name__ == "__main__":
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    window = MainWindow()
    window.resize(200, 200)
    window.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
