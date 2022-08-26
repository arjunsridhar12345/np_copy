import datetime
import json
import os
import pathlib
import sys
import time

import numpy as np
import requests

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ModuleNotFoundError:
    from PyQt5 import QtCore, QtGui, QtWidgets

import pyqtgraph as pg
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets


class RigComputerModel(QtGui.QStandardItemModel):

    def __init__(self, parent=None, label=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.label = "rig details"
        self.addRigs()

    def launch_rdc(self, index):
        item = self.itemFromIndex(index)
        if 'stim' in item.comp.lower():
            s = input("stim pc connection requested - may be displaying\ncontinue?\n>>")
            if s.lower() != 'y':
                print('cancelled')
                return
        os.system(f"mstsc /v:{item.hostname}")

    def addRigs(self):
        for comp, hostname in self.get_np_computers().items():
            display_name = f"{comp}    |    {hostname}"
            textual_item = QtGui.QStandardItem(display_name)
            textual_item.hostname = hostname
            textual_item.comp = comp
            textual_item.setEditable = False
            # Add the item to the model
            self.appendRow(textual_item)

    def get_np_computers(self, rigs=None, comp=None):
        if rigs is None:
            rigs = [0, 1, 2]

        if not isinstance(rigs, list):
            rigs = [int(rigs)]

        if comp is None:
            comp = ['sync', 'acq', 'mon', 'stim']

        if not isinstance(comp, list):
            comp = [str(comp)]

        comp = [c.lower() for c in comp]

        np_idx = ["NP." + str(idx) for idx in rigs]

        all_pc = requests.get("http://mpe-computers/v2.0").json()
        a = {}
        for k, v in all_pc['comp_ids'].items():
            if any([sub in k for sub in np_idx]) and any([s in k.lower() for s in comp]):
                a[k] = v['hostname'].upper()
        return a


class RigComputerView(QtWidgets.QTreeView):

    def __init__(self, parent=None, label=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.label = "rig computer list display"
        self.setMinimumSize(200, 200)
        self.model = RigComputerModel()
        # Apply the model to the list view
        self.setModel(self.model) # todo move to controller

        # this enables the view to do some optimizations:
        # self.setUniformItemSizes(True)
        self.expandAll()
        self.doubleClicked.connect(self.model.launch_rdc)

        # # todo move some of this to controller
        # self.proxy = FileFilterProxyModel()
        # self.setModel(self.proxy)
        # self.source = self.proxy.sourceModel()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None, label=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.title = "RDC launcher"
        self.setCentralWidget(RigComputerView())


if __name__ == "__main__":
    app = pg.mkQApp("docked widget GUI")
    win = MainWindow()
    # win.add_docked_widgets([]) # FolderTreeView()

    # app.exec()
    win.show()
    sys.exit(pg.exec())
