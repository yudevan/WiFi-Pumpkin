from PyQt4 import QtGui, QtCore
from collections import OrderedDict
from core.servers.http_handler.proxyhandler.MitmMode import *


class MitmController(QtGui.QTableWidget):
    manipulator = {}
    SetNoManipulator = QtCore.pyqtSignal(object)
    def __init__(self,parent = 0):
        super(MitmController, self).__init__(parent)
        self.parent=parent
        self.FSettings = self.parent.FSettings
        #self.uplinkIF = self.parent.Refactor.get_interfaces()
        #self.downlinkIF = self.parent.selectCard.currentText()
        __manipulator= [prox(parent=self.parent) for prox in MitmMode.__subclasses__()]
        #Keep Proxy in a dictionary
        for k in __manipulator:
            self.manipulator[k.Name]=k

        self.m_name = []
        self.m_desc = []
        self.m_settings = []
        for n,p in self.manipulator.items():
            self.m_name.append(p.plugin_radio)
            self.m_settings.append(p.btnChangeSettings)
            self.m_desc.append(p.plugin_radio.objectName())
            #self.manipulatorGroup.addButton(p.controlui)
            p.sendSingal_disable.connect(self.DisableManipulator)
            #self.parent.TabListWidget_Menu.addItem(p.tabinterface)
            #self.parent.Stack.addWidget(p)

        self.ManipulatorTable = OrderedDict(
            [('proxyhandler', self.m_name),
             ('Settings', self.m_settings),
             ('Description', self.m_desc)
             ])
        self.setColumnCount(3)
        self.setRowCount(len(self.ManipulatorTable['proxyhandler']))
        self.resizeRowsToContents()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(23)
        self.setSortingEnabled(True)
        self.setHorizontalHeaderLabels(self.ManipulatorTable.keys())
        self.horizontalHeader().resizeSection(0, 158)
        self.horizontalHeader().resizeSection(1, 80)
        self.resizeRowsToContents()

        # add all widgets in Qtable 2 plugin
        Headers = []
        for n, key in enumerate(self.ManipulatorTable.keys()):
            Headers.append(key)
            for m, item in enumerate(self.ManipulatorTable[key]):
                if type(item) == type(QtGui.QCheckBox()) or type(item) == type(QtGui.QPushButton()):
                    self.setCellWidget(m, n, item)
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.setItem(m, n, item)
        self.setHorizontalHeaderLabels(self.ManipulatorTable.keys())
    def DisableManipulator(self,status):
        self.SetNoManipulator.emit(status)
    @property
    def Activated(self):
        manobj =[]
        for manip in self.manipulator.values():
            if manip.plugin_radio.isChecked():
                manobj.append(manip)
        return manobj
    @property
    def get(self):
        return self.manipulator
    @classmethod
    def disable(cls, val=True):
        pass
    @property
    def disableproxy(self, name):
        pass
    def Start(self):
        for i in self.Activated:
            print "Starting {}".format(i.Name)
            i.boot()
    def Stop(self):
        for i in self.Activated:
            print "Stopping {}".format(i.Name)
            i.shutdown()
