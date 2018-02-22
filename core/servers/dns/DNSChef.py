from core.config.globalimport import *
from core.utility.threads import ProcessThread
from core.servers.dns.DNSBase import DNSBase
from core.servers.dhcp.dhcpserver import  DNSServer

class PyDNSServer(DNSBase):
    ID = "PyDNS"
    Name = "PyDNS Server"
    ExecutableFile = "plugins/external/dns2proxy/dns2proxy.py"
    def __init__(self,parent):
        super(PyDNSServer,self).__init__(parent)
    @property
    def commandline(self):
        cmd=[]
        cmd.insert(0,self.ExecutableFile)
        cmd.extend(['-i',str(self.parent.SessionConfig.Wireless.WLANCard.currentText()),'-k', self.parent.currentSessionID])
    def boot(self):
        self.reactor = DNSServer(str(self.parent.SessionConfig.Wireless.WLANCard.currentText()),
                                             self.DHCPConf['router'])
        self.reactor._ProcssOutput.connect(self.parent.get_dns2proxy_output)
        self.reactor.setObjectName(self.Name)  # use dns2proxy as DNS server
