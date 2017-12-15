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
from core.Manipulator.Manipulator import Manipulator


class NetCreds(Manipulator):
    ASName = "Net Credentials"
    ASAuthor = "Wahyudin Aziz"
    ASDescription = "Sniff passwords and hashes from an interface or pcap file coded by: Dan McInerney"
    ASIcon = "icons/tcpproxy.png"
    ASSettings = True
    ASType = "proxy"  # proxy or server
    def __init__(self,parent,FSettingsUI=None,main_method=None,  **kwargs):
        super(NetCreds, self).__init__(parent)

