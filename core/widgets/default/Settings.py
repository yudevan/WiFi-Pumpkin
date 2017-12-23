from PyQt4.QtGui import *
from PyQt4.QtCore import *
from core.widgets.default.tabs import *
from core.widgets.default.SettingsItem import SettingsItem


class Settings(TabsWidget):
    ConfigRoot="Settings"
    __subitem = False
    def __init__(self,parent=None,FSettings=None):
        super(Settings,self).__init__(parent,FSettings)
        self.FSettings = FSettings
        self.title = self.__class__.__name__
        _mod_settings = [setitem(self.parent,self.FSettings ) for setitem in SettingsItem.__subclasses__()]


        self.mod_settings = {}
        for mod in _mod_settings:
            self.mod_settings[mod.title]=mod
            self.mainlayout.addWidget(mod)
    @property
    def isSubitem(self):
        return self.__subitem


