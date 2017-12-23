from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Mode(QWidget):
    ConfigRoot = "Wireless"
    Name ="Wireless Mode Generic"
    def __init__(self,parent=None,FSettings = None):
        super(Mode,self).__init__(parent,FSettings)