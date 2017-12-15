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


class PumpkinMitmproxy(ProxyMode):
    ''' settings  Transparent Proxy '''
    ASName = "Pumpkin Proxy"
    ASAuthor = "Wahyudin Aziz"
    ASDescription = "Generic Placeholder for Attack Scenario"
    ASIcon = "icons/pumpkinproxy.png"
    ASSettings = True
    Hidden = False
    ASType = "proxy"  # proxy or server
    sendError = QtCore.pyqtSignal(str)

    def __init__(self, parent, FsettingsUI=None, main_method=None, **kwargs):
        super(PumpkinMitmproxy,self).__init__(parent)
        self.mainLayout     = QtGui.QVBoxLayout()
        self.config         = SettingsINI(C.PUMPPROXY_INI)
        self.plugins        = []
        self.main_method    = parent
        self.bt_SettingsDict    = {}
        self.check_PluginDict   = {}
        self.search_all_ProxyPlugins()
        #scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)

        # create for add dock logging
        self.tabcontrol = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.page_1 = QtGui.QVBoxLayout(self.tab1)
        self.page_2 = QtGui.QVBoxLayout(self.tab2)
        self.tableLogging  = dockPumpkinProxy()

        self.tabcontrol.addTab(self.tab1, 'Plugins')
        self.tabcontrol.addTab(self.tab2, 'Logging')

        self.TabPlugins = QtGui.QTableWidget()
        self.TabPlugins.setColumnCount(3)
        self.TabPlugins.setRowCount(len(self.plugins))
        self.TabPlugins.resizeRowsToContents()
        self.TabPlugins.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.TabPlugins.horizontalHeader().setStretchLastSection(True)
        self.TabPlugins.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.TabPlugins.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TabPlugins.verticalHeader().setVisible(False)
        self.TabPlugins.verticalHeader().setDefaultSectionSize(27)
        self.TabPlugins.setSortingEnabled(True)
        self.THeaders  = OrderedDict([ ('Plugins',[]),('Settings',[]),('Description',[])])
        self.TabPlugins.setHorizontalHeaderLabels(self.THeaders.keys())
        self.TabPlugins.horizontalHeader().resizeSection(0,158)
        self.TabPlugins.horizontalHeader().resizeSection(1,80)

        # add on tab
        self.page_1.addWidget(self.TabPlugins)
        self.page_2.addWidget(self.tableLogging)

        # get all plugins and add into TabWidget
        Headers = []
        for plugin in self.plugins:
            if plugin.ConfigParser:
                self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton('Settings')
                self.bt_SettingsDict[plugin.Name].clicked.connect(partial(self.setSettingsPlgins,plugin.Name))
            else:
                self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton('None')
            self.check_PluginDict[plugin.Name] = QtGui.QCheckBox(plugin.Name)
            self.check_PluginDict[plugin.Name].setObjectName(plugin.Name)
            self.check_PluginDict[plugin.Name].clicked.connect(partial(self.setPluginOption,plugin.Name))
            self.THeaders['Plugins'].append(self.check_PluginDict[plugin.Name])
            self.THeaders['Settings'].append({'name': plugin.Name})
            self.THeaders['Description'].append(plugin.Description)
        for n, key in enumerate(self.THeaders.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeaders[key]):
                if type(item) == type(QtGui.QCheckBox()):
                    self.TabPlugins.setCellWidget(m,n,item)
                elif type(item) == type(dict()):
                    self.TabPlugins.setCellWidget(m,n,self.bt_SettingsDict[item['name']])
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.TabPlugins.setItem(m, n, item)
        self.TabPlugins.setHorizontalHeaderLabels(self.THeaders.keys())

        # check status all checkbox plugins
        for box in self.check_PluginDict.keys():
            self.check_PluginDict[box].setChecked(self.config.get_setting('plugins',box,format=bool))

        self.mainLayout.addWidget(self.tabcontrol)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    def setPluginOption(self, name,status):
        ''' get each plugins status'''
        # enable realtime disable and enable plugin
        if self.main_method.PopUpPlugins.check_pumpkinProxy.isChecked() and \
            self.main_method.FSettings.Settings.get_setting('accesspoint','statusAP',format=bool):
                self.main_method.Thread_PumpkinProxy.m.disablePlugin(name, status)
        self.config.set_setting('plugins',name,status)

    def setSettingsPlgins(self,plugin):
        ''' open settings options for each plugins'''
        key = 'set_{}'.format(plugin)
        self.widget = PumpkinProxySettings(key,self.config.get_all_childname(key))
        self.widget.show()

    def search_all_ProxyPlugins(self):
        ''' load all plugins function '''
        plugin_classes = plugin.PluginTemplate.__subclasses__()
        for p in plugin_classes:
            self.plugins.append(p())
    def boot(self):
        self.tableLogging.clearContents()
        plugin_classes = plugin.PluginTemplate.__subclasses__()
        for p in plugin_classes:
            self.plugins.append(p())
    def optionsRules(self):
        return str('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080')
