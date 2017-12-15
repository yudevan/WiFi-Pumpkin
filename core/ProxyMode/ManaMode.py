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


class ManaMode(ProxyMode):
    ASName = "Mana Mode"
    ASAuthor = "Wahyudin Aziz"
    ASDescription = "Refactor from mana-toolkit by digininja"
    Hidden = False


    def __init__(self, parent, FsettingsUI=None, main_method=None, **kwargs):
        super(ManaMode,self).__init__(parent)
