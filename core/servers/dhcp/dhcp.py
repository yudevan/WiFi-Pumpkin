from core.config.globalimport import *
from core.widgets.customiseds import *
from core.widgets.default.uimodel import *
from core.servers.components.BaseComponent import BaseComponent


class DHCPServers(BaseComponent):
    def __init__(self):
        super(DHCPServers,self).__init__()
        self.DHCPConf = self.Settings.conf

    @property
    def Settings(self):
        return DHCPSettings.instances[0]




class DHCPSettings(CoreSettings):
    Name = "DHCP"
    ID = "DHCP"
    instances=[]

    def __init__(self,parent=0):
        super(DHCPSettings,self).__init__(parent)
        self.__class__.instances.append(weakref.proxy(self))
        self.setCheckable(False)
        self.setFixedWidth(400)
        self.layoutDHCP = QtGui.QFormLayout()
        self.layoutbuttons = QtGui.QHBoxLayout()
        self.btnDefault = QtGui.QPushButton('Default')
        self.btnSave = QtGui.QPushButton('save settings')
        self.btnSave.setIcon(QtGui.QIcon('icons/export.png'))
        self.btnDefault.setIcon(QtGui.QIcon('icons/settings.png'))
        self.btnDefault.clicked.connect(self.setdefaultSettings)
        self.btnSave.clicked.connect(self.savesettingsDHCP)

        self.dhcpClassIP = QtGui.QComboBox()
        self.EditGateway = QtGui.QLineEdit(self)
        self.EditGateway.setFixedWidth(120)
        self.EditGateway.setHidden(True)  # disable Gateway

        self.classtypes = ['Class-A-Address', 'Class-B-Address', 'Class-C-Address', 'Class-Custom-Address']
        for types in self.classtypes:
            if 'Class-{}-Address'.format(self.FSettings.Settings.get_setting('dhcp', 'classtype')) in types:
                self.classtypes.remove(types), self.classtypes.insert(0, types)
        self.dhcpClassIP.addItems(self.classtypes)
        self.leaseTimeDef = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'leasetimeDef'))
        self.leaseTimeMax = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'leasetimeMax'))
        self.netmask = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'netmask'))
        self.range = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'range'))
        self.router = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'router'))
        self.subnet = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'subnet'))
        self.broadcast = QtGui.QLineEdit(self.FSettings.Settings.get_setting('dhcp', 'broadcast'))
        self.dhcpClassIP.currentIndexChanged.connect(self.dhcpClassIPClicked)

        self.layoutDHCP.addRow('Class Ranges', self.dhcpClassIP)
        self.layoutDHCP.addRow('Default Lease time', self.leaseTimeDef)
        self.layoutDHCP.addRow('Max Lease time', self.leaseTimeMax)
        self.layoutDHCP.addRow('Subnet', self.subnet)
        self.layoutDHCP.addRow('Router', self.router)
        self.layoutDHCP.addRow('Netmask', self.netmask)
        self.layoutDHCP.addRow('Broadcaset Address', self.broadcast)
        self.layoutDHCP.addRow('DHCP IP-Range', self.range)
        self.updateconf()

        # layout add
        self.layoutbuttons.addWidget(self.btnSave)
        self.layoutbuttons.addWidget(self.btnDefault)
        self.layoutDHCP.addRow(self.layoutbuttons)
        self.layout.addLayout(self.layoutDHCP)
    def dhcpClassIPClicked(self,classIP):
        self.selected = str(self.dhcpClassIP.currentText())
        if 'class-Custom-Address' in self.selected: self.selected = 'dhcp'
        self.leaseTimeDef.setText(self.FSettings.Settings.get_setting(self.selected,'leasetimeDef'))
        self.leaseTimeMax.setText(self.FSettings.Settings.get_setting(self.selected,'leasetimeMax'))
        self.netmask.setText(self.FSettings.Settings.get_setting(self.selected,'netmask'))
        self.range.setText(self.FSettings.Settings.get_setting(self.selected,'range'))
        self.router.setText(self.FSettings.Settings.get_setting(self.selected,'router'))
        self.subnet.setText(self.FSettings.Settings.get_setting(self.selected,'subnet'))
        self.broadcast.setText(self.FSettings.Settings.get_setting(self.selected,'broadcast'))
    def setdefaultSettings(self):
        self.dhcpClassIP.setCurrentIndex(self.classtypes.index('Class-A-Address'))
        self.leaseTimeDef.setText(self.FSettings.Settings.get_setting('dhcpdefault','leasetimeDef'))
        self.leaseTimeMax.setText(self.FSettings.Settings.get_setting('dhcpdefault','leasetimeMax'))
        self.netmask.setText(self.FSettings.Settings.get_setting('dhcpdefault','netmask'))
        self.range.setText(self.FSettings.Settings.get_setting('dhcpdefault','range'))
        self.router.setText(self.FSettings.Settings.get_setting('dhcpdefault','router'))
        self.subnet.setText(self.FSettings.Settings.get_setting('dhcpdefault','subnet'))
        self.broadcast.setText(self.FSettings.Settings.get_setting('dhcpdefault','broadcast'))
        self.updateconf()

    def savesettingsDHCP(self):
        self.all_geteway_check = []
        for types in self.classtypes:
            if not 'Class-Custom-Address' in types:
                self.all_geteway_check.append(self.FSettings.Settings.get_by_index_key(5,types))
        self.FSettings.Settings.set_setting('dhcp','classtype',str(self.dhcpClassIP.currentText()).split('-')[1])
        self.FSettings.Settings.set_setting('dhcp','leasetimeDef',str(self.leaseTimeDef.text()))
        self.FSettings.Settings.set_setting('dhcp','leasetimeMax',str(self.leaseTimeMax.text()))
        self.FSettings.Settings.set_setting('dhcp','netmask',str(self.netmask.text()))
        self.FSettings.Settings.set_setting('dhcp','range',str(self.range.text()))
        self.FSettings.Settings.set_setting('dhcp','router',str(self.router.text()))
        self.FSettings.Settings.set_setting('dhcp','subnet',str(self.subnet.text()))
        self.FSettings.Settings.set_setting('dhcp','broadcast',str(self.broadcast.text()))
        if not str(self.route.text()) in self.all_geteway_check:
            self.FSettings.Settings.set_setting('dhcp','classtype','Custom')
        self.btnSave.setEnabled(False)
        self.sendMensage.emit('settings DHCP saved with success...')
        self.btnSave.setEnabled(True)
    def updateconf(self):
        self.conf['leasetimeDef'] = str(self.leaseTimeDef.text())
        self.conf['leasetimeMax'] = str(self.leaseTimeMax.text())
        self.conf['subnet'] = str(self.subnet.text())
        self.conf['router'] = str(self.router.text())
        self.conf['netmask'] = str(self.netmask.text())
        self.conf['broadcast'] = str(self.broadcast.text())
        self.conf['range'] = str(self.range.text())

class DHCPClient(HomeDisplay):
    Name = "DHCP"
    ID = "DHCP"
    def __init__(self,parent):
        super(DHCPClient,self).__init__(parent)
        self.ClientTable = AutoTableWidget()
        self.THeaders = OrderedDict([('Devices', []),
                                     ('IP Address', []),
                                     ('Mac Address', []),
                                     ('Vendors', [])],
                                    )
        self.ClientTable.setRowCount(50)
        self.ClientTable.resizeRowsToContents()
        self.ClientTable.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.ClientTable.horizontalHeader().setStretchLastSection(True)
        self.ClientTable.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.ClientTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ClientTable.verticalHeader().setVisible(False)
        self.ClientTable.setHorizontalHeaderLabels(self.THeaders.keys())
        self.ClientTable.verticalHeader().setDefaultSectionSize(23)
        self.ClientTable.horizontalHeader().resizeSection(3, 158)
        self.ClientTable.horizontalHeader().resizeSection(0, 150)
        self.ClientTable.horizontalHeader().resizeSection(2, 120)
        self.ClientTable.horizontalHeader().resizeSection(1, 120)
        self.ClientTable.setSortingEnabled(True)
        self.ClientTable.setObjectName('table_clients')

        self.layout.addWidget(self.ClientTable)
