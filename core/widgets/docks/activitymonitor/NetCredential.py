from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

from core.widgets.docks.activitymonitor.activitymonitor import ActivityMonitorControl

class URLMonitor(ActivityMonitorControl):
    id = "URLMonitor"
    title = "URLMonitor"
    def __init__(self,parent=None):
        super(URLMonitor,self).__init__(parent,title="URLMonitor")
        self.maindockwidget = QTreeView()
        self.maindockwidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['URL', 'HTTP-Headers'])
        self.maindockwidget.setModel(self.model)
        self.maindockwidget.setUniformRowHeights(True)
        self.maindockwidget.setColumnWidth(0, 130)
        self.setWidget(self.maindockwidget)
        self.setObjectName(self.title)

    def writeModeData(self, data):
        ''' get data output and add on QtableWidgets '''
        ParentMaster = QStandardItem('[ {0[src]} > {0[dst]} ] {1[Method]} {1[Host]}{1[Path]}'.format(
            data['urlsCap']['IP'], data['urlsCap']['Headers']))
        ParentMaster.setIcon(QIcon('icons/accept.png'))
        ParentMaster.setSizeHint(QSize(30, 30))
        for item in data['urlsCap']['Headers']:
            ParentMaster.appendRow([QStandardItem('{}'.format(item)),
                                    QStandardItem(data['urlsCap']['Headers'][item])])
        self.maindockwidget.model.appendRow(ParentMaster)
        self.maindockwidget.setFirstColumnSpanned(ParentMaster.row(),
                                   self.rootIndex(), True)
        self.maindockwidget.scrollToBottom()

    def clear(self):
        self.maindockwidget.model.clear()

    def stopProcess(self):
        self.maindockwidget.clearSelection()