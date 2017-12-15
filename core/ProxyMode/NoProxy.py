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
from core.ProxyMode.ProxyMode import ProxyMode


class NoProxy(ProxyMode):
    ASName="No Proxy"
    ASAuthor = "Wahyudin Aziz"

    def __init__(self, parent, FsettingsUI=None, main_method=None, **kwargs):
        super(NoProxy, self).__init__(parent)
        self.controlui.setChecked(self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool))
        self.controlui.toggled.connect(self.CheckOptions)
        self.setEnabled(self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool))
        #parent.PopUpPlugins.GroupPluginsProxy.setChecked(not self.FSettings.Settings.get_setting('plugins', self.ASName, format=bool))