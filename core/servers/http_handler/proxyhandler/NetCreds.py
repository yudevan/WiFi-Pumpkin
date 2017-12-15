from core.servers.http_handler.proxyhandler.MitmMode import Manipulator


class NetCreds(Manipulator):
    ASName = "Net Credentials"
    ASAuthor = "Wahyudin Aziz"
    ASDescription = "Sniff passwords and hashes from an interface or pcap file coded by: Dan McInerney"
    ASIcon = "icons/tcpproxy.png"
    ASSettings = True
    ASType = "proxy"  # proxy or server
    def __init__(self,parent,FSettingsUI=None,main_method=None,  **kwargs):
        super(NetCreds, self).__init__(parent)

