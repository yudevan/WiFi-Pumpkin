from core.config.globalimport import *
from os import (
    system,path,getcwd,
    popen,listdir,mkdir,chown
)
from core.widgets.default.SessionConfig import *
from core.servers.dhcp.dhcp import DHCPClient

class Mode(QtGui.QWidget):
    ConfigRoot = "Generic"
    SubConfig = "Generic"
    ID = "GenericWirelessMode"
    Name = "Wireless Mode Generic"
    service = None
    reactor = None
    def __init__(self,parent=None,FSettings = None):
        super(Mode,self).__init__(parent)
        self.parent = parent
        self.FSettings = SuperSettings.getInstance()
        self.controlui = QtGui.QCheckBox(self.Name)
        self.controlui.clicked.connect(partial(self.controlcheck,self.controlui))
        self.SettingsAP = {}
        self.hostapd_path = os.path.abspath(
            str(self.FSettings.Settings.get_setting(self.ConfigRoot, '{}_hostapd_path'.format(self.ConfigRoot))))
        self.currentSessionID = self.parent.currentSessionID
        self.SettingsAP = self.parent.SettingsAP
        self.SessionsAP = self.parent.SessionsAP
        self.SessionConfig = SessionConfig.instances[0]
        self.interfacesLink = Refactor.get_interfaces()
    def get_soft_dependencies(self):
        ''' check if Hostapd, isc-dhcp-server is installed '''
        if not path.isfile(self.hostapd_path):
            return QtGui.QMessageBox.information(self,'Error Hostapd','hostapd is not installed')
        if self.FSettings.Settings.get_setting('accesspoint','dhcpd_server',format=bool):
            if not self.SettingsEnable['ProgCheck'][3]:
                return QtGui.QMessageBox.warning(self,'Error dhcpd','isc-dhcp-server (dhcpd) is not installed')
        return True
    def configure_network_AP(self):
        self.parent.configure_network_AP()
    def controlcheck(self,object):
        pass

    @property
    def WirelessSettings(self):
        return self.SessionConfig.Wireless
    @property
    def Settings(self):
        pass
    def Initialize(self):
        pass
    def boot(self):
        pass
    def Shutdown(self):
        pass
    def Start(self):
        self.Initialize()
        self.boot()
        self.PostStart()
    def PostStart(self):
        self.parent.set_status_label_AP(True)
        # TODO remove the code below as it has been replaced with proxy disables
        # self.ProxyPluginsTAB.GroupSettings.setEnabled(False)
        print('-------------------------------')
        print('AP::[{}] Running...'.format(self.WirelessSettings.EditSSID.text()))
        print('AP::BSSID::[{}] CH {}'.format(Refactor.get_interface_mac(
            self.WirelessSettings.WLANCard.currentText()),
            self.WirelessSettings.EditChannel.value()))
        self.FSettings.Settings.set_setting('accesspoint', 'statusAP', True)
        self.FSettings.Settings.set_setting('accesspoint', 'interfaceAP',
                                            str(self.WirelessSettings.WLANCard.currentText()))
        # check if Advanced mode is enable
    def Stop(self):
        self.Shutdown()
    @property
    def DHCPClient(self):
        return DHCPClient.instances[0]
    def get_error_hostapdServices(self,data):
        '''check error hostapd on mount AP '''
        self.Shutdown()
        return QtGui.QMessageBox.warning(self,'[ERROR] Hostpad',
        'Failed to initiate Access Point, '
        'check output process hostapd.\n\nOutput::\n{}'.format(data))
    def LogOutput(self,data):
        ''' get inactivity client from hostapd response'''

        if self.DHCPClient.ClientTable.APclients != {}:
            if data in self.DHCPClient.ClientTable.APclients.keys():
                self.parent.StationMonitor.addRequests(data,self.DHCPClient.ClientTable.APclients[data],False)
            self.DHCPClient.ClientTable.delete_item(data)
            self.parent.connectedCount.setText(str(len(self.DHCPClient.ClientTable.APclients.keys())))
