from core.config.globalimport import *
from core.servers.dhcp.dhcp import DHCPServers

class PyDHCP(DHCPServers):
    Name = "Python DHCP Server"
    ID = "PyDHCP"
    def __init__(self):
        super(PyDHCP,self).__init__()