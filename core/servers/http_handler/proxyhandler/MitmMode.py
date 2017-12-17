from os import path
from core.main import  QtGui,QtCore
from datetime import datetime
from core.utils import Refactor
from collections import OrderedDict
from core.utility.threads import ThreadPopen
from core.widgets.docks.dockmonitor import (
    dockAreaAPI,dockUrlMonitor,dockCredsMonitor,dockPumpkinProxy,dockTCPproxy
)
from core.utility.threads import  (
    ProcessHostapd,Thread_sergioProxy,
    ThRunDhcp,Thread_sslstrip,ProcessThread,
    ThreadReactor,ThreadPopen,ThreadPumpkinProxy
)
from core.widgets.pluginssettings import PumpkinProxySettings
from core.utility.collection import SettingsINI
from plugins.external.scripts import *
from plugins.extension import *
from functools import partial
from plugins.analyzers import *
import core.utility.constants as C
from core.widgets.customiseds import AutoGridLayout
class Widget(QtGui.QFrame):
    def __init__(self,parent):
        QtGui.QWidget.__init__(self,parent)
class VBox(QtGui.QVBoxLayout):
    def __init__(self):
        QtGui.QVBoxLayout.__init__(self)

class MitmMode(Widget):
    Name = "Generic"
    Author = "Wahyudin Aziz"
    Description = "Generic Placeholder for Attack Scenario"
    Icon = "icons/plugins-new.png"
    ModSettings = False
    ModType = "proxy" # proxy or server
    Hidden = True
    _cmd_array = []
    plugins = []
    sendError = QtCore.pyqtSignal(str)
    sendSingal_disable = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
        super(MitmMode, self).__init__(parent)
        self.parent = parent
        self.FSettings = parent.FSettings
        self.reactor = None
        self.server = None
        self.popup = QtGui.QWidget()
        self.tabinterface = QtGui.QListWidgetItem()
        self.tabinterface.setText(self.Name)
        self.tabinterface.setSizeHint(QtCore.QSize(30, 30))
        self.tabinterface.setIcon(QtGui.QIcon(self.Icon))
        self.ConfigWindow = QtGui.QDialog()

        self.plugin_radio = QtGui.QCheckBox(self.Name)
        self.plugin_radio.setObjectName(QtCore.QString(self.Description))
        self.plugin_radio.setChecked(self.FSettings.Settings.get_setting('mitmhandler', self.Name, format=bool))
        self.plugin_radio.clicked.connect(self.CheckOptions)

        self.setEnabled(self.FSettings.Settings.get_setting('mitmhandler', self.Name, format=bool))
        self.btnChangeSettings = QtGui.QPushButton("None")
        self.btnChangeSettings.setEnabled(False)

        if self.ModSettings:
            self.btnChangeSettings.setEnabled(True)
            self.btnChangeSettings.setText("Change")
            self.btnChangeSettings.setIcon(QtGui.QIcon('icons/config.png'))
            self.btnChangeSettings.clicked.connect(self.Configure)


        self.mainLayout = QtGui.QFormLayout()
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
    @property
    def CMD_ARRAY(self):
        return self._cmd_array

    @property
    def hasSettings(self):
        return self.ModSettings
    def CheckOptions(self):
        self.FSettings.Settings.set_setting('mitmhandler', self.Name, self.plugin_radio.isChecked())
        if self.plugin_radio.isChecked() == True:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
        self.Initialize()
    def Initialize(self):
        self.SetRules()
    def SetRules(self):
        pass
    def ClearRules(self):
        pass
    def Configure(self):
        self.ConfigWindow.show()
    def boot(self):
        if self.CMD_ARRAY:
            self.reactor= ProcessThread({'python': self.CMD_ARRAY})
            self.reactor._ProcssOutput.connect(self.LogOutput)
            self.reactor.setObjectName(self.Name)
            print "Scheduling {}".format(self.Name)
    def shutdown(self):
        pass
    def LogOutput(self,data):
        pass



