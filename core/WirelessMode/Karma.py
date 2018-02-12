from core.config.globalimport import  *
import weakref
from core.utility.threads import ProcessHostapd,ThRunDhcp,ProcessThread
from core.widgets.default.uimodel import *
from core.WirelessMode.WirelessMode import Mode


class Karma(Mode):
    ConfigRoot = "Karma"
    SubConfig = "Karma"
    Name = "Karma AP Mode"
    ID = "Karma"
    def __init__(self,parent=0):
        super(Karma,self).__init__(parent)


    def Initialize(self):

        self.configure_network_AP()
        self.get_soft_dependencies()
        ignore = ('interface=', 'ssid=', 'channel=', 'essid=')
        with open(C.HOSTAPDCONF_PATH, 'w') as apconf:
            for i in self.parent.SettingsAP['hostapd']: apconf.write(i)
            for config in str(self.FSettings.ListHostapd.toPlainText()).split('\n'):
                if not config.startswith('#') and len(config) > 0:
                    if not config.startswith(ignore):
                        apconf.write(config + '\n')
            if self.Settings.EnableMana.isChecked():
                apconf.write('enable_karma=1'+'\n')
                if self.Settings.ManaLoud.isChecked():
                    apconf.write('karma_black_white=1' + '\n')
                else:
                    apconf.write('karma_black_white=0' + '\n')
            apconf.close()

    def boot(self):
        # create thread for hostapd and connect get_Hostapd_Response function
        self.reactor = ProcessHostapd({self.hostapd_path: [C.HOSTAPDCONF_PATH]}, self.parent.currentSessionID)
        self.reactor.setObjectName('KarmaHostapd')
        self.reactor.statusAP_connected.connect(self.LogOutput)
        self.reactor.statusAPError.connect(self.Shutdown)
    @property
    def Settings(self):
        return KarmaSettings.instances[0]

class KarmaSettings(CoreSettings):
    ConfigRoot = "Karma"
    Name = "Karma"
    ID = "Karma"
    instances = []
    def __init__(self,parent):
        super(KarmaSettings,self).__init__(parent)
        self.__class__.instances.append(weakref.proxy(self))
        self.FSettings = SuperSettings.instances[0]
        self.setCheckable(False)
        self.WLayout = QtGui.QGroupBox()
        self.WLayout.setTitle("Karma AP Settings")
        self.WLGrid = QtGui.QGridLayout()
        self.WLayout.setLayout(self.WLGrid)


        self.HostapdKarmaPath = QtGui.QLineEdit()
        self.HostapdKarmaPath.setText(self.FSettings.Settings.get_setting(self.ConfigRoot ,'{}_hostapd_path'.format(self.ConfigRoot)))
        self.HostapdConf = QtGui.QComboBox()
        os.path.walk('core/config/hostapd',self.osWalkCallback,None)

        self.EditSSID = QtGui.QLineEdit()
        self.BtnRandomSSID = QtGui.QPushButton()
        self.BtnRandomSSID.setIcon(QtGui.QIcon('icons/refresh.png'))
        self.BtnRandomSSID.clicked.connect(self.setAP_essid_random)

        self.EditBSSID = QtGui.QLineEdit()
        self.EditChannel = QtGui.QSpinBox()
        self.EditChannel.setMaximum(11)
        self.EditChannel.setFixedWidth(10)
        self.EditChannel.setMinimum(0)

        self.EnableMana = QtGui.QGroupBox("Enable Karma")
        self.EnableMana.setCheckable(True)
        self.EnableMana.setObjectName("enable_karma")
        self.EnableMana.setChecked(self.FSettings.Settings.get_setting(self.ConfigRoot, 'enable_karma',format=bool))
        self.ManaLoud = QtGui.QCheckBox("Karma Black")
        self.ManaLoud.setObjectName("karma_black_white")
        self.ManaLoud.setChecked(self.FSettings.Settings.get_setting(self.ConfigRoot, 'karma_black_white',format=bool))
        self.KLayout = QtGui.QFormLayout()
        self.KLayout.addRow(self.ManaLoud)
        self.EnableMana.setLayout(self.KLayout)

        self.EditSSID.setText(self.FSettings.Settings.get_setting('accesspoint', 'ssid'))
        self.EditBSSID.setText(self.FSettings.Settings.get_setting('accesspoint', 'bssid'))
        self.EditChannel.setValue(self.FSettings.Settings.get_setting('accesspoint', 'channel', format=int))

        self.WLGrid.addWidget(QtGui.QLabel("Initial SSID:"), 0, 0)
        self.WLGrid.addWidget(self.EditSSID, 0, 1)
        self.WLGrid.addWidget(QtGui.QLabel("BSSID:"), 2, 0)
        self.WLGrid.addWidget(self.EditBSSID, 2, 1)
        self.WLGrid.addWidget(self.BtnRandomSSID, 2, 2)
        self.WLGrid.addWidget(QtGui.QLabel("Channel:"), 3, 0)
        self.WLGrid.addWidget(self.EditChannel, 3, 1)
        self.APLayout = QtGui.QFormLayout()
        self.APLayout.addRow(QtGui.QLabel("Hostapd with Mana"),self.HostapdKarmaPath)
        self.APLayout.addRow(QtGui.QLabel("Mana Conf"), self.HostapdConf)
        self.APLayout.addRow(self.WLayout,self.EnableMana)
        self.layout.addLayout(self.APLayout)
    def osWalkCallback(self,arg,directory,files):
        for file in files:
            self.HostapdConf.addItem(os.path.join(directory,file))
    def setAP_essid_random(self):
        ''' set random mac 3 last digits  '''
        prefix = []
        for item in [x for x in str(self.EditBSSID.text()).split(':')]:
            prefix.append(int(item,16))
        self.EditBSSID.setText(Refactor.randomMacAddress([prefix[0],prefix[1],prefix[2]]).upper())
