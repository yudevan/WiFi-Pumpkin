from core.servers.http_handler.proxyhandler.MitmMode import MitmMode


class NetCreds(MitmMode):
    Name = "Net Credentials"
    Author = "P0cL4bs"
    Description = "Sniff passwords and hashes from an interface or pcap file coded by: Dan McInerney"
    Icon = "icons/tcpproxy.png"
    ModSettings = True
    ModType = "proxy"  # proxy or server
    def __init__(self,parent,FSettingsUI=None,main_method=None,  **kwargs):
        super(NetCreds, self).__init__(parent)

