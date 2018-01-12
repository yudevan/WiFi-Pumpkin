from core.config.globalimport import  *
from core.WirelessMode.WirelessMode import Mode


class Static(Mode):
    SubConfig = "Static"
    Name = "Static SSID Mode"
    def __init__(self,parent=0):
        super(Static,self).__init__(parent)
        
