from core.servers.http_handler.proxyhandler.MitmMode import Manipulator


class NetCreds(Manipulator):
    Name = "Net Credentials"
    Author = "Wahyudin Aziz"
    Description = "Sniff passwords and hashes from an interface or pcap file coded by: Dan McInerney"
    Icon = "icons/tcpproxy.png"
    ModSettings = True
    ModType = "proxy"  # proxy or server
    def __init__(self,parent,FSettingsUI=None,main_method=None,  **kwargs):
        super(NetCreds, self).__init__(parent)

