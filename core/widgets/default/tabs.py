from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TabsWidget(QWidget):
    Name="Generic"
    Icon = ""
    __subitem = False
    sendMensage = pyqtSignal(str)
    checkDockArea = pyqtSignal(dict)
    def __init__(self,parent=0,FSettings=None):
        super(TabsWidget,self).__init__(parent)
        self.setObjectName(self.Name)
        self.FSettings = FSettings
        self.parent = parent

        self.tabinterface = QListWidgetItem()
        self.tabinterface.setText(self.Name)
        self.tabinterface.setSizeHint(QSize(30, 30))
        self.tabinterface.setIcon(QIcon(self.Icon))
        self.mainlayout = QFormLayout()
        self.scrollwidget = QWidget()
        self.scroll = QScrollArea()
        self.scrollwidget.setLayout(self.mainlayout)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scrollwidget)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

    @property
    def isSubitem(self):
        return self.__subitem
