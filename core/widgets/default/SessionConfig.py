from core.config.globalimport import *
from core.widgets.default.tabs import *
from core.widgets.default.SettingsItem import *


class SessionConfig(TabsWidget):
    ConfigRoot="Settings"
    Name = "Session Config"
    Icon = "icons/settings-AP.png"
    __subitem = False
    def __init__(self,parent=None,FSettings=None):
        super(SessionConfig,self).__init__(parent,FSettings)
        self.FSettings = SuperSettings()
        self.title = self.__class__.__name__
        _mod_settings = [setitem(self.parent ) for setitem in CoreSettings.__subclasses__()]
        self.mod_settings = {}
        for mod in _mod_settings:
            self.mod_settings[mod.title]=mod
            self.mainlayout.addWidget(mod)
    @property
    def isSubitem(self):
        return self.__subitem


