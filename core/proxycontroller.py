from core.config.globalimport import *
from collections import OrderedDict
from core.widgets.default.uimodel import *
from core.servers.proxy.package import *
from core.utility.component import ControllerBlueprint



class ProxyModeController(PluginsUI,ControllerBlueprint):
    Name = "Proxy"
    Caption = "Enable Proxy Server"
    proxies = {}
    SetNoProxy = QtCore.pyqtSignal(object)
    dockMount = QtCore.pyqtSignal(bool)

    def __init__(self,parent, FSettings=None, main_method=None, **kwargs):
        super(ProxyModeController, self).__init__(parent)
        self.parent=parent
        self.FSettings = SuperSettings.instances[0]
        self.setCheckable(True)
        self.setChecked(self.FSettings.Settings.get_setting('plugins', 'disableproxy', format=bool))
        self.clicked.connect(self.get_disable_proxy)
        self.proxyGroup = QtGui.QButtonGroup()
        __proxlist= [prox(parent=self.parent) for prox in ProxyMode.ProxyMode.__subclasses__()]
        #Keep Proxy in a dictionary
        for k in __proxlist:
            self.proxies[k.Name]=k

        self.p_name = []
        self.p_desc = []
        self.p_settings = []
        for n,p in self.proxies.items():
            self.p_name.append(p.controlui)
            self.p_settings.append(p.btnChangeSettings)
            self.p_desc.append(p.controlui.objectName())
            self.proxyGroup.addButton(p.controlui)
            p.sendSingal_disable.connect(self.DisableProxy)
            p.dockwidget.addDock.connect(self.dockUpdate)

        self.THeadersPluginsProxy = OrderedDict(
            [('Proxies', self.p_name),
             ('Settings', self.p_settings),
             ('Description', self.p_desc)
             ])
        self.table.setColumnCount(3)
        self.table.setRowCount(len(self.proxies))
        self.table.resizeRowsToContents()
        self.table.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(23)
        self.table.setSortingEnabled(True)
        self.table.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())
        self.table.horizontalHeader().resizeSection(0, 158)
        self.table.horizontalHeader().resizeSection(1, 80)
        self.table.resizeRowsToContents()
        # add all widgets in Qtable 1 plgins
        Headers = []
        for n, key in enumerate(self.THeadersPluginsProxy.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeadersPluginsProxy[key]):
                if type(item) == type(QtGui.QRadioButton()) or type(item) == type(QtGui.QPushButton()):
                    self.table.setCellWidget(m, n, item)
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.table.setItem(m, n, item)
        self.table.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())
    def get_disable_proxy(self):


        if self.isChecked():
            self.parent.set_proxy_statusbar(self.Activated.Name, disabled=False)
            self.FSettings.Settings.set_setting('plugins', 'disableproxy',
                                                self.isChecked())

        else:
            self.SetNoProxy.emit(self.isChecked())
            self.FSettings.Settings.set_setting('plugins', 'disableproxy',
                                                self.isChecked())
            self.parent.set_proxy_statusbar('', disabled=True)

    def dockUpdate(self,add=True):
        self.dockMount.emit(add)

    def DisableProxy(self,status):
        self.SetNoProxy.emit(status)
    @property
    def ActiveDocks(self):
        return self.Activated.dockwidget

    @property
    def ActiveReactor(self):
        reactor = []
        for act in self.proxies.values():
            if act.controlui.isChecked():
                if act.Name =="No Proxy":
                    return None
                else:
                    reactor.append(act.reactor)
                    if act.subreactor:
                        reactor.append(act.subreactor)
        return reactor
    @property
    def Activated(self):
        for act in self.proxies.values():
            if act.controlui.isChecked():
                if act.Name =="No Proxy":
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
        self.Activated.Initialize()
        self.Activated.Serve()
        self.Activated.boot()

    def Stop(self):
        self.setEnabled(True)
        self.Activated.Serve(False)
        self.Activated.shutdown()
    def SaveLog(self):

        self.Activated.SaveLog()