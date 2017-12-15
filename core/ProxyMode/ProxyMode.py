from os import path
from core.main import  QtGui,QtCore
from datetime import datetime
from core.utils import Refactor
from collections import OrderedDict
from core.utility.threads import ThreadPopen
from core.widgets.docks.dockmonitor import (
    dockAreaAPI,dockUrlMonitor,dockCredsMonitor,dockPumpkinProxy,dockTCPproxy
)
from core.widgets.pluginssettings import PumpkinProxySettings
from core.utility.collection import SettingsINI
from plugins.external.scripts import *
from plugins.extension import *
from functools import partial
from plugins.analyzers import *
from configobj import ConfigObj,Section
import modules as GUI
from core.loaders.models.PackagesUI import *
import core.utility.constants as C
from core.widgets.customiseds import AutoGridLayout
from core.utility.threads import  (
    ProcessHostapd,Thread_sergioProxy,
    ThRunDhcp,Thread_sslstrip,ProcessThread,
    ThreadReactor,ThreadPopen,ThreadPumpkinProxy
)
class Widget(QtGui.QFrame):
    def __init__(self):
        QtGui.QWidget.__init__(self)
class VBox(QtGui.QVBoxLayout):
    def __init__(self):
        QtGui.QVBoxLayout.__init__(self)

class ProxyMode(Widget):
    ASName = "Generic"
    ASAuthor = "Wahyudin Aziz"
    ASDescription = "Generic Placeholder for Attack Scenario"
    ASIcon = "icons/plugins-new.png"
    ASSettings = False
    ASType = "proxy" # proxy or server
    Hidden = True
    plugins = []
    sendError = QtCore.pyqtSignal(str)
    sendSingal_disable = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
        super(ProxyMode, self).__init__()
        self.parent = parent
        self.FSettings = parent.FSettings
        self.reactor = ThreadReactor()
        self.popup = QtGui.QWidget()
        self.tabinterface = QtGui.QListWidgetItem()
        self.tabinterface.setText(self.ASName)
        self.tabinterface.setSizeHint(QtCore.QSize(30, 30))
        self.tabinterface.setIcon(QtGui.QIcon(self.ASIcon))
        self.ConfigWindow = QtGui.QDialog()

        self.controlui = QtGui.QRadioButton(self.ASName)
        self.controlui.setObjectName(QtCore.QString(self.ASDescription))
        self.controlui.setChecked(self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool))
        self.controlui.toggled.connect(self.CheckOptions)
        self.setEnabled(self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool))

        self.btnChangeSettings = QtGui.QPushButton("None")
        self.btnChangeSettings.setEnabled(False)

        if self.ASSettings:
            self.btnChangeSettings.setEnabled(True)
            self.btnChangeSettings.setText("Change")
            self.btnChangeSettings.setIcon(QtGui.QIcon('icons/config.png'))
            self.btnChangeSettings.clicked.connect(self.Configure)
        #TODO Update parent Proxy Status When Loading

        self.mainLayout = QtGui.QFormLayout()
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
    def get_disable_status(self):
        if self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool) == True:
            if self.ASName == "No Proxy":
                self.ClearRules()
                self.parent.set_proxy_statusbar('', disabled=True)
                self.sendSingal_disable.emit(self.controlui.isChecked())
                return

            self.parent.set_proxy_statusbar(self.ASName)
    @property
    def hasSettings(self):
        return self.ASSettings
    def CheckOptions(self):
        self.FSettings.Settings.set_setting('plugins', self.ASName, self.controlui.isChecked())
        self.get_disable_status()
        #self.parent.get_disable_proxy()
        self.ClearRules()
        if self.controlui.isChecked() == True:
            self.setEnabled(True)
            self.SetRules()
        else:
            self.setEnabled(False)
            self.ClearRules()
        self.Initialize()
    def boot(self):
        self.reactor = ProcessThread('echo Starting')
        #self.reactor= ProcessThread({'python': [C.BDFPROXY_EXEC, '-k', self.currentSessionID]})
        self.reactor._ProcssOutput.connect(self.LogOutput)
        self.reactor.setObjectName(self.ASName)
        #self.Apthreads['RougeAP'].append(self.reactor)
    def shutdown(self):
        pass
    @property
    def isEnabled(self):
        pass
    def optionsRules(self):
        return "No Rules"
    def Initialize(self):
        self.SetRules()
    def defaultRules(self,type):
        ''' add rules iptable by type plugins'''
        search = {
        'dns2proxy':str('iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port 53'),
        }
        return search[type]
    def SetRules(self):
        items = []
        for index in xrange(self.FSettings.ListRules.count()):
            items.append(str(self.FSettings.ListRules.item(index).text()))
        if self.optionsRules() in items:
            return
        item = QtGui.QListWidgetItem()
        item.setText(self.optionsRules())
        item.setSizeHint(QtCore.QSize(30, 30))
        self.FSettings.ListRules.addItem(item)
    def ClearRules(self):
        pass
    def LogOutput(self,data):
        pass
    def Configure(self):
        self.ConfigWindow.show()

    def unset_Rules(self,type):
        ''' remove rules from Listwidget in settings widget'''
        items = []
        for index in xrange(self.FSettings.ListRules.count()):
            items.append(str(self.FSettings.ListRules.item(index).text()))
        for position,line in enumerate(items):
            if self.optionsRules(type) == line:
                self.FSettings.ListRules.takeItem(position)
    def SaveLog(self):
        pass



