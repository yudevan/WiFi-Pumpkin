from collections import OrderedDict
from functools import partial

import core.utility.constants as C
from core.main import  QtGui
from core.servers.http_handler.proxyhandler.MitmMode import MitmMode
from core.utility.collection import SettingsINI
from core.widgets.docks.dockmonitor import (
    dockTCPproxy
)
from plugins.external.scripts import *
from plugins.extension import *
from plugins.analyzers import *


class TCPProxy(MitmMode):
    Name = "TCP Proxy"
    Author = "Wahyudin Aziz"
    Description = "Sniff for isntercept network traffic on UDP,TCP protocol get password,hash,image,etc..."
    Icon = "icons/tcpproxy.png"
    ModSettings = True
    ModType = "proxy"  # proxy or server
    def __init__(self,parent,FSettingsUI=None,main_method=None,  **kwargs):
        super(TCPProxy,self).__init__(parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.config = SettingsINI(C.TCPPROXY_INI)
        self.plugins = []
        self.main_method = main_method
        self.bt_SettingsDict = {}
        self.check_PluginDict = {}
        self.search_all_ProxyPlugins()
        # scroll area
        self.scrollwidget = QtGui.QWidget()
        self.scrollwidget.setLayout(self.mainLayout)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)

        self.tabcontrol = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.page_1 = QtGui.QVBoxLayout(self.tab1)
        self.page_2 = QtGui.QVBoxLayout(self.tab2)
        self.tableLogging = dockTCPproxy()

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
        self.THeaders = OrderedDict([('Plugins', []), ('Author', []), ('Description', [])])
        self.TabPlugins.setHorizontalHeaderLabels(self.THeaders.keys())
        self.TabPlugins.horizontalHeader().resizeSection(0, 158)
        self.TabPlugins.horizontalHeader().resizeSection(1, 120)

        self.page_1.addWidget(self.TabPlugins)
        self.page_2.addWidget(self.tableLogging)
        # get all plugins and add into TabWidget
        Headers = []
        for plugin in self.plugins:
            self.bt_SettingsDict[plugin.Name] = QtGui.QPushButton(plugin.Author)
            self.check_PluginDict[plugin.Name] = QtGui.QCheckBox(plugin.Name)
            self.check_PluginDict[plugin.Name].setObjectName(plugin.Name)
            self.check_PluginDict[plugin.Name].clicked.connect(partial(self.setPluginOption, plugin.Name))
            self.THeaders['Plugins'].append(self.check_PluginDict[plugin.Name])
            self.THeaders['Author'].append({'name': plugin.Name})
            self.THeaders['Description'].append(plugin.Description)
        for n, key in enumerate(self.THeaders.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeaders[key]):
                if type(item) == type(QtGui.QCheckBox()):
                    self.TabPlugins.setCellWidget(m, n, item)
                elif type(item) == type(dict()):
                    self.TabPlugins.setCellWidget(m, n, self.bt_SettingsDict[item['name']])
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.TabPlugins.setItem(m, n, item)
        self.TabPlugins.setHorizontalHeaderLabels(self.THeaders.keys())

        # check status all checkbox plugins
        for box in self.check_PluginDict.keys():
            self.check_PluginDict[box].setChecked(self.config.get_setting('plugins', box, format=bool))

        self.mainLayout.addWidget(self.tabcontrol)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    def setPluginOption(self, name, status):
        ''' get each plugins status'''
        # enable realtime disable and enable plugin
        if self.main_method.FSettings.Settings.get_setting('accesspoint', 'statusAP', format=bool):
            self.main_method.Thread_TCPproxy.disablePlugin(name, status)
        self.config.set_setting('plugins', name, status)

    def search_all_ProxyPlugins(self):
        ''' load all plugins function '''
        plugin_classes = default.PSniffer.__subclasses__()
        for p in plugin_classes:
            if p().Name != 'httpCap':
                self.plugins.append(p())
    def CheckOptions(self):
        self.FSettings.Settings.set_setting('mitmhandler', self.Name, self.plugin_radio.isChecked())
        if self.plugin_radio.isChecked() == True:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
        self.Initialize()
