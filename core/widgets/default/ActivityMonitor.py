from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *
from core.widgets.default.uimodel import *



class ActivityMonitor(TabsWidget):
    Name = "Monitor Activity"
    ID = "ActivityMonitor"
    Icon = "icons/activity-monitor.png"
    __subitem = False
    def __init__(self,parent= None,FSettings=None):
        super(ActivityMonitor,self).__init__(parent,FSettings)
        self.Dock = QtGui.QMainWindow()
        del self.scrollwidget
        del self.scroll
        del self.mainlayout
        self.layout.addWidget(self.Dock,True)
