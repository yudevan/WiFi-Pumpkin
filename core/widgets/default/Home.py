from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *
from core.widgets.default.tabs import TabsWidget



class Home(TabsWidget):
    Name = "Home"
    __subitem = False
    def __init__(self,parent= None,FSettings=None):
        super(Home,self).__init__(parent,FSettings)