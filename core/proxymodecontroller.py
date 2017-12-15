import os, sys
from collections import OrderedDict
from core.ProxyMode import  *
from PyQt4 import QtGui, QtCore



class ProxyModeController(QtGui.QTableWidget):
    proxies = {}
    SetNoProxy = QtCore.pyqtSignal(object)
    def __init__(self,parent = 0):
        super(ProxyModeController, self).__init__(parent)
        self.parent=parent
        self.FSettings = self.parent.FSettings
        self.proxyGroup = QtGui.QButtonGroup()
        __proxlist= [prox(parent=self.parent) for prox in ProxyMode.ProxyMode.__subclasses__()]
        #Keep Proxy in a dictionary
        for k in __proxlist:
            self.proxies[k.ASName]=k

        self.p_name = []
        self.p_desc = []
        self.p_settings = []
        for n,p in self.proxies.items():
            self.p_name.append(p.controlui)
            self.p_settings.append(p.btnChangeSettings)
            self.p_desc.append(p.controlui.objectName())
            self.proxyGroup.addButton(p.controlui)
            p.sendSingal_disable.connect(self.DisableProxy)
            #self.parent.TabListWidget_Menu.addItem(p.tabinterface)
            #self.parent.Stack.addWidget(p)

        self.THeadersPluginsProxy = OrderedDict(
            [('Proxies', self.p_name),
             ('Settings', self.p_settings),
             ('Description', self.p_desc)
             ])
        self.setColumnCount(3)
        self.setRowCount(len(self.proxies))
        self.resizeRowsToContents()
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(23)
        self.setSortingEnabled(True)
        self.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())
        self.horizontalHeader().resizeSection(0, 158)
        self.horizontalHeader().resizeSection(1, 80)
        self.resizeRowsToContents()
        # add all widgets in Qtable 1 plgins
        Headers = []
        for n, key in enumerate(self.THeadersPluginsProxy.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeadersPluginsProxy[key]):
                if type(item) == type(QtGui.QRadioButton()) or type(item) == type(QtGui.QPushButton()):
                    self.setCellWidget(m, n, item)
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.setItem(m, n, item)
        self.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())
    def DisableProxy(self,status):
        self.SetNoProxy.emit(status)
    @property
    def Activated(self):
        for act in self.proxies.values():
            if act.controlui.isChecked():
                if act.ASName =="No Proxy":
                    return None
                else:
                    return act
    @property
    def get(self):
        return self.proxies
    @classmethod
    def disable(cls, val=True):
        pass
    @property
    def disableproxy(self, name):
        pass
    def Start(self):
        self.setEnabled(False)
        self.Activated.boot()
    def Stop(self):
        self.setEnabled(True)
        self.Activated.shutdown()
    def SaveLog(self):
        self.Activated.SaveLog()