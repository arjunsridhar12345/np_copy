from PyQt5 import QtCore, QtGui, QtWidgets

import pyqtgraph as pg
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
#from pyqtgraph.Qt import QtWidgets
import sys
import pathlib
import shutil
import os

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None, label=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.resize(1000, 500)
        self.title = "file transfer gui with docked modules"
        self.initUI()
    
    def initUI(self):
        self.hBoxLayout = QtWidgets.QHBoxLayout() # main layout - A and B
        self.aBoxLayout = QtWidgets.QVBoxLayout() # layout for A
        self.bBoxLayout = QtWidgets.QVBoxLayout() # layout for B

        self.dirTextBoxA = QtWidgets.QLineEdit(self) # directory A
        self.dirTextBoxA.returnPressed.connect(self.setTreeViewA)
        self.dirTextBoxB = QtWidgets.QLineEdit(self) # directory B
        self.dirTextBoxB.returnPressed.connect(self.setTreeViewB)

        self.textLayoutA = QtWidgets.QFormLayout()
        self.textLayoutA.addRow('Enter directory A path', self.dirTextBoxA)

        self.textLayoutB = QtWidgets.QFormLayout()
        self.textLayoutB.addRow('Enter directory B path', self.dirTextBoxB)

        self.aBoxLayout.addLayout(self.textLayoutA)
        self.bBoxLayout.addLayout(self.textLayoutB)

        self.moveAtoB = QtWidgets.QPushButton('Move from A to B')
        self.moveAtoB.clicked.connect(self.moveFromAtoB)

        self.copyAtoB = QtWidgets.QPushButton('Copy from A to B')
        self.copyAtoB.clicked.connect(self.copyFromAtoB)

        self.moveBtoA = QtWidgets.QPushButton('Move from B to A')
        self.moveBtoA.clicked.connect(self.moveFromBtoA)

        self.copyBtoA = QtWidgets.QPushButton('Copy from B to A')

        self.aButtonsLayout = QtWidgets.QHBoxLayout()
        self.aButtonsLayout.addWidget(self.moveAtoB)
        self.aButtonsLayout.addWidget(self.copyAtoB)

        self.bButtonsLayout = QtWidgets.QHBoxLayout()
        self.bButtonsLayout.addWidget(self.moveBtoA)
        self.bButtonsLayout.addWidget(self.copyBtoA)

        self.aBoxLayout.addLayout(self.aButtonsLayout)
        self.bBoxLayout.addLayout(self.bButtonsLayout)

        self.treeViewA= QtWidgets.QTreeView()
        self.aBoxLayout.addWidget(self.treeViewA)
        self.treeViewB = QtWidgets.QTreeView()
        self.bBoxLayout.addWidget(self.treeViewB)

        self.hBoxLayout.addLayout(self.aBoxLayout)
        self.seperator = QtWidgets.QFrame()
        self.seperator.setFrameShape(QtWidgets.QFrame.VLine)
        self.seperator.setLineWidth(3)
        self.hBoxLayout.addWidget(self.seperator)
        self.hBoxLayout.addLayout(self.bBoxLayout)

        self.setLayout(self.hBoxLayout)
    
    def copyFromAtoB(self):
        directory = self.folder_modelA.itemData(self.treeViewA.selectedIndexes()[0])[0]
        print(directory)
        source = str(pathlib.Path.joinpath(pathlib.Path(self.dirTextBoxA.text()), directory))
        dest = str(pathlib.Path(self.dirTextBoxB.text()))

        if source != '' and dest != '':
            if os.path.exists(source) and os.path.isdir(dest):
                shutil.copytree(source, dest, dirs_exist_ok=True)

    def copyFromBtoA(self):
        directory = self.folder_modelB.itemData(self.treeViewA.selectedIndexes()[0])[0]
        print(directory)
        source = str(pathlib.Path.joinpath(pathlib.Path(self.dirTextBoxB.text()), directory))
        dest = str(pathlib.Path(self.dirTextBoxA.text()))

        if source != '' and dest != '':
            if os.path.exists(source) and os.path.isdir(dest):
                shutil.copytree(source, dest, dirs_exist_ok=True)

    def moveFromAtoB(self):
        directory = self.folder_modelA.itemData(self.treeViewA.selectedIndexes()[0])[0]
        print(directory)
        source = str(pathlib.Path.joinpath(pathlib.Path(self.dirTextBoxA.text()), directory))
        dest = str(pathlib.Path(self.dirTextBoxB.text()))

        if source != '' and dest != '':
            if os.path.exists(source) and os.path.isdir(dest):
                shutil.move(source, dest)
    
    def moveFromBtoA(self):
        directory = self.folder_modelB.itemData(self.treeViewA.selectedIndexes()[0])[0]
        print(directory)
        source = str(pathlib.Path.joinpath(pathlib.Path(self.dirTextBoxB.text()), directory))
        dest = str(pathlib.Path(self.dirTextBoxA.text()))

        if source != '' and dest != '':
            if os.path.exists(source) and os.path.isdir(dest):
                shutil.move(source, dest)

    def setTreeViewA(self):
        path = self.dirTextBoxA.text()
        print(path)
        dirPath = str(pathlib.Path(path))

        self.folder_modelA = QtWidgets.QFileSystemModel()
        self.folder_modelA.setRootPath(dirPath)
        self.folder_modelA.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

        if path != '':
            self.treeViewA.setModel(self.folder_modelA)
            self.treeViewA.setRootIndex(self.folder_modelA.index(dirPath))

    def setTreeViewB(self):
        path = self.dirTextBoxA.text()
        print(path)
        dirPath = str(pathlib.Path(path))

        self.folder_modelB = QtWidgets.QFileSystemModel()
        self.folder_modelB.setRootPath(dirPath)
        self.folder_modelB.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

        if path != '':
            self.treeViewB.setModel(self.folder_modelB)
            self.treeViewB.setRootIndex(self.folder_modelB.index(dirPath))

if __name__ == '__main__':
    app = pg.mkQApp("docked widget GUI")
    win = MainWindow()
    #swin.add_docked_widgets([]) # FolderTreeView()

    # app.exec()
    win.show()
    sys.exit(pg.exec())