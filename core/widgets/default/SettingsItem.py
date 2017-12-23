from PyQt4.QtGui import *
from PyQt4.QtCore import *
from core.widgets.default.tabs import *


class Settings(Tabs):
    def __init__(self,parent=None,FSettings=None):
        super(Settings,self).__init__(parent,FSettings)
        self.title = self.__class__.__name__

