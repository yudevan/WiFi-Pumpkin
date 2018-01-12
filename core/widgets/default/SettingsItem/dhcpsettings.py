from core.config.globalimport import *
from core.widgets.default.tabs import *


class DHCPSettings(CoreSettings):
    Name = "DHCP"
    def __init__(self,parent=0):
        super(DHCPSettings,self).__init__(parent)
        self.setCheckable(False)