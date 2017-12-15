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
import core.utility.constants as C
from core.widgets.customiseds import AutoGridLayout
class Widget(QtGui.QFrame):
    def __init__(self,parent):
        QtGui.QWidget.__init__(self,parent)
class VBox(QtGui.QVBoxLayout):
    def __init__(self):
        QtGui.QVBoxLayout.__init__(self)

class Manipulator(Widget):
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
        super(Manipulator, self).__init__(parent)
        self.parent = parent
        self.FSettings = parent.FSettings
        self.reactor = None
        self.popup = QtGui.QWidget()
        self.tabinterface = QtGui.QListWidgetItem()
        self.tabinterface.setText(self.ASName)
        self.tabinterface.setSizeHint(QtCore.QSize(30, 30))
        self.tabinterface.setIcon(QtGui.QIcon(self.ASIcon))
        self.ConfigWindow = QtGui.QDialog()

        self.plugin_radio = QtGui.QCheckBox(self.ASName)
        self.plugin_radio.setObjectName(QtCore.QString(self.ASDescription))
        self.plugin_radio.setChecked(self.FSettings.Settings.get_setting('manipulator', self.ASName, format=bool))
        self.plugin_radio.clicked.connect(self.CheckOptions)

        self.setEnabled(self.FSettings.Settings.get_setting('manipulator', self.ASName, format=bool))
        self.btnChangeSettings = QtGui.QPushButton("None")
        self.btnChangeSettings.setEnabled(False)

        if self.ASSettings:
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
    def hasSettings(self):
        return self.ASSettings
    def CheckOptions(self):
        self.FSettings.Settings.set_setting('manipulator', self.ASName, self.plugin_radio.isChecked())
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
        pass
    def shutdown(self):
        pass



