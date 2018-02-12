from core.config.globalimport import *
from core.servers.dhcp.dhcpserver import DHCPServer, DNSServer
from core.utility.threads import ProcessThread
from core.servers.dhcp.dhcp import DHCPServers

class PyDHCP(DHCPServers):
    Name = "Python DHCP Server"
    ID = "PyDHCP"
    def __init__(self,parent=0):
        super(PyDHCP,self).__init__(parent)
    def Initialize(self):
        if self.FSettings.Settings.get_setting('accesspoint', 'pydns_server', format=bool):
            self.service = DNSServer(str(self.parent.SessionConfig.Wireless.WLANCard.currentText()),
                                             self.DHCPConf['router'])
            self.service.setObjectName('PyDNS')  # use DNS python implements

        elif self.FSettings.Settings.get_setting('accesspoint', 'dnsproxy_server', format=bool):
            self.service = ProcessThread({'python': ['plugins/external/dns2proxy/dns2proxy.py', '-i',
                                                             str(self.parent.SessionConfig.Wireless.WLANCard.currentText()),
                                                             '-k', self.parent.currentSessionID]})
            self.service._ProcssOutput.connect(self.parent.get_dns2proxy_output)
            self.service.setObjectName('DNS2Proxy')  # use dns2proxy as DNS server


    def boot(self):
        self.reactor = DHCPServer(str(self.parent.SessionConfig.Wireless.WLANCard.currentText()), self.DHCPConf)
        self.reactor.sendConnetedClient.connect(self.get_DHCP_Discover_clients)
        self.reactor.setObjectName('Py_DHCP')
