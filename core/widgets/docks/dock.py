from PyQt4 import QtGui,QtCore,Qt
from functools import  partial

class Docking(QtGui.QDockWidget):
    title = 'Default'
    id = 'default'
    def __init__(self,parent=0,title='Default',info={}):
        super(Docking,self).__init__(parent)
        self.parent = parent
        self.title = title
        self.logger = info
        self.startThread = False
        self.processThrear = None
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)

        self.controlui = QtGui.QCheckBox(self.title)
        self.controlui.toggled.connect(partial(self.controlui_toggled))
    def runThread(self):
        self.startThread=True
    def controlui_toggled(self):
        pass
    def writeModeData(self,data):
        item = QListWidgetItem()
        item.setText(data)
        item.setSizeHint(QSize(27, 27))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        self.insertItem(self.count() + 1, item)
        self.scrollToBottom()
    def clear(self):
        pass
    def stopProcess(self):
        if self.processThread != None:
            self.processThread.stop()