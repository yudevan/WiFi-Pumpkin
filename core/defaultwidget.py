from PyQt4.QtGui import *
from PyQt4.QtCore import *
from core.widgets.default.tabs import *


class DefaultWidget(QWidget):
    def __init__(self,parent=None,FSettings = None):
        super(DefaultWidget,self).__init__(parent)
        self.parent = parent
        self.FSettings = FSettings
        self.defaultui = []
        self.allui =[]
        __defaultui = [ui(parent,self.FSettings) for ui in TabsWidget.__subclasses__()]
        for ui in __defaultui:
            if not  ui.isSubitem:
                self.defaultui.append(ui)
            self.allui.append(ui)

    @property
    def CoreTabs(self):
        return self.defaultui

