from PyQt4 import QtGui, QtCore
from collections import OrderedDict
from core.servers.http_handler.proxyhandler import *


class MitmController(QtGui.QTableWidget):
    mitmhandler = {}
    SetNoMitmMode = QtCore.pyqtSignal(object)
    dockMount = QtCore.pyqtSignal(bool)
    def __init__(self,parent = 0):
        super(MitmController, self).__init__(parent)
        self.parent=parent
        self.FSettings = self.parent.FSettings
        #self.uplinkIF = self.parent.Refactor.get_interfaces()
        #self.downlinkIF = self.parent.selectCard.currentText()
        __manipulator= [prox(parent=self.parent) for prox in MitmMode.MitmMode.__subclasses__()]
        #Keep Proxy in a dictionary
        for k in __manipulator:
            self.mitmhandler[k.Name]=k

        self.m_name = []
        self.m_desc = []
        self.m_settings = []
        for n,p in self.mitmhandler.items():
            self.m_name.append(p.controlui)
            self.m_settings.append(p.btnChangeSettings)
            self.m_desc.append(p.controlui.objectName())
            #self.manipulatorGroup.addButton(p.controlui)
            p.sendSingal_disable.connect(self.DisableMitmMode)
            p.dockwidget.addDock.connect(self.dockUpdate)
            #self.parent.TabListWidget_Menu.addItem(p.tabinterface)
            #self.parent.Stack.addWidget(p)

        self.MitmModeTable = OrderedDict(
            [('proxyhandler', self.m_name),
             ('Settings', self.m_settings),
             ('Description', self.m_desc)
             ])
        self.setColumnCount(3)
        self.setRowCount(len(self.MitmModeTable['proxyhandler']))
        self.resizeRowsToContents()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(23)
        self.setSortingEnabled(True)
        self.setHorizontalHeaderLabels(self.MitmModeTable.keys())
        self.horizontalHeader().resizeSection(0, 158)
        self.horizontalHeader().resizeSection(1, 80)
        self.resizeRowsToContents()

        # add all widgets in Qtable 2 plugin
        Headers = []
        for n, key in enumerate(self.MitmModeTable.keys()):
            Headers.append(key)
            for m, item in enumerate(self.MitmModeTable[key]):
                if type(item) == type(QtGui.QCheckBox()) or type(item) == type(QtGui.QPushButton()):
                    self.setCellWidget(m, n, item)
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.setItem(m, n, item)
        self.setHorizontalHeaderLabels(self.MitmModeTable.keys())
    def DisableMitmMode(self,status):
        self.SetNoMitmMode.emit(status)
    def dockUpdate(self,add=True):
        self.dockMount.emit(add)
    @property
    def ActiveDock(self):
        manobj = []
        for manip in self.mitmhandler.values():
            if manip.controlui.isChecked():
                manobj.append(manip.dockwidget)
        return manobj
    @property
    def Activated(self):
        manobj =[]
        for manip in self.mitmhandler.values():
            if manip.controlui.isChecked():
                manobj.append(manip)
        return manobj
    @property
    def ActiveReactor(self):
        reactor=[]
        for i in self.Activated:
            reactor.append(i.reactor)
        return reactor
    @property
    def get(self):
        return self.mitmhandler
    @classmethod
    def disable(cls, val=True):
        pass
    @property
    def disableproxy(self, name):
        pass
    def Start(self):
        for i in self.Activated:
            i.boot()
    def Stop(self):
        for i in self.Activated:
            i.shutdown()
