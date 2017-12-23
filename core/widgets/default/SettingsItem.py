from PyQt4.QtGui import *
from PyQt4.QtCore import *
from core.widgets.default.tabs import *


class SettingsItem(TabsWidget):
    __subitem = True
    def __init__(self,parent=None,FSettings=None):
        super(SettingsItem,self).__init__(parent,FSettings)
        self.title = self.__class__.__name__
        self.parent = parent
        self.FSettings = FSettings


