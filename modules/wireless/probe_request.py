from re import search
from core.utils import set_monitor_mode
from core.packets.wireless import ThreadProbeScan
from core.loaders.models.PackagesUI import *

"""
Description:
    This program is a module for wifi-pumpkin.py file which includes functionality
    for monitor probe request AP.

Copyright:
    Copyright (C) 2015-2016 Marcos Nesster P0cl4bs Team
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class frm_PMonitor(PumpkinModule):
    def __init__(self, parent=None):
        super(frm_PMonitor, self).__init__(parent)
        self.Main       = QtGui.QVBoxLayout()
        self.Requests   = []
        self.data       = {'Devices':[],'MacAddress': [], 'SSIDs':[]}
        self.setWindowTitle("Probe Request wifi Monitor")
        self.setWindowIcon(QtGui.QIcon('icons/icon.ico'))
        self.setGeometry(QtCore.QRect(100, 100, 420, 450))
        self.setupGUI()

    def setupGUI(self):
        # base widget responsible
        self.widget         = QtGui.QWidget()
        self.layout         = QtGui.QVBoxLayout(self.widget)
        self.StatusBar      = QtGui.QStatusBar()
        self.StatusProbe    = QtGui.QLabel('')
        self.StatusBar.addWidget(QtGui.QLabel('Scannner::'))

        self.StartedProbe(False)
        self.StatusBar.setFixedHeight(15)
        # create table widget
        self.tables = QtGui.QTableWidget(5,3)
        self.tables.setRowCount(50)
        self.tables.setMinimumHeight(180)
        self.tables.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.tables.horizontalHeader().setStretchLastSection(True)
        self.tables.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tables.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tables.resizeColumnsToContents()
        self.tables.resizeRowsToContents()
        self.tables.horizontalHeader().resizeSection(0,120)
        self.tables.horizontalHeader().resizeSection(1,110)
        self.tables.horizontalHeader().resizeSection(2,130)
        self.tables.verticalHeader().setVisible(False)
        self.tables.setSortingEnabled(True)
        Headers = []
        for key in reversed(self.data.keys()):
            Headers.append(key)
        self.tables.setHorizontalHeaderLabels(Headers)
        self.tables.verticalHeader().setDefaultSectionSize(23)

        # create all buttons
        self.btn_scan = QtGui.QPushButton('Start')
        self.btn_stop = QtGui.QPushButton('Stop')
        self.btn_refrash = QtGui.QPushButton('Refresh')
        self.btn_refrash.clicked.connect(self.loadCard)
        self.btn_stop.clicked.connect(self.StopProbeResquest)
        self.btn_scan.clicked.connect(self.StartProbeResquest)
        self.btn_scan.setIcon(QtGui.QIcon('icons/network.png'))
        self.btn_stop.setIcon(QtGui.QIcon('icons/network_off.png'))
        self.btn_refrash.setIcon(QtGui.QIcon('icons/refresh.png'))
        self.get_placa = QtGui.QComboBox(self)
        self.btn_stop.setEnabled(False)
        self.loadCard()

        # group Network card select
        self.GroupBoxNetwork = QtGui.QGroupBox()
        self.layoutGroupNW = QtGui.QHBoxLayout()
        self.GroupBoxNetwork.setLayout(self.layoutGroupNW)
        self.GroupBoxNetwork.setTitle('Network Adapter:')
        self.layoutGroupNW.addWidget(self.get_placa)
        self.layoutGroupNW.addWidget(self.btn_refrash)

        # add table and GroupNetwork
        self.form0  = QtGui.QVBoxLayout()
        self.form0.addWidget(self.tables)
        self.form0.addWidget(self.GroupBoxNetwork)

        # form buttons and statusbar
        self.mForm = QtGui.QFormLayout()
        self.mForm.addRow(self.btn_scan, self.btn_stop)
        self.mForm.addRow(self.StatusBar)

        # add form in widget Main base
        self.layout.addLayout(self.form0)
        self.layout.addLayout(self.mForm)
        self.Main.addWidget(self.widget)
        self.setLayout(self.Main)

    def loadCard(self):
        # add all card wireless in ComboBox
        self.get_placa.clear()
        n = Refactor.get_interfaces()['all']
        for item,card in enumerate(n):
            if search("wl", card):
                self.get_placa.addItem(n[item])

    def StartedProbe(self,bool):
        if bool:
            self.StatusProbe.setText("[ON]")
            self.StatusProbe.setStyleSheet("QLabel {  color : green; }")
        else:
            self.StatusProbe.setText("[OFF]")
            self.StatusProbe.setStyleSheet("QLabel {  color : red; }")
        self.StatusBar.addWidget(self.StatusProbe)

    def threadReceiveScan(self,info):
        # add data sended from thread scapy in Table
        if info not in self.Requests:
            Headers = []
            data = info.split('|')
            self.data['SSIDs'].append(data[1])
            self.data['MacAddress'].append(data[0])
            self.data['Devices'].append(data[2])
            for n, key in enumerate(reversed(self.data.keys())):
                Headers.append(key)
                for m, item in enumerate(self.data[key]):
                    item = QtGui.QTableWidgetItem(item)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
                    self.tables.setItem(m, n, item)
            Headers = []
            for key in reversed(self.data.keys()):
                Headers.append(key)
            self.tables.setHorizontalHeaderLabels(Headers)
            self.Requests.append(info)

    def StopProbeResquest(self):
        # disable mode monitor card and stop attack
        self.ThreadProbe.stop()
        set_monitor_mode(self.get_placa.currentText()).setDisable()
        self.btn_stop.setEnabled(False)
        self.btn_scan.setEnabled(True)
        self.StartedProbe(False)

    def StartProbeResquest(self):
        if self.get_placa.currentText() == '':
            return QtGui.QMessageBox.information(self, 'Network Adapter', 'Network Adapter is not found. Try again.')
        self.btn_stop.setEnabled(True)
        self.btn_scan.setEnabled(False)
        set_monitor_mode(self.get_placa.currentText()).setEnable()
        self.ThreadProbe = ThreadProbeScan(str(self.get_placa.currentText()))
        self.connect(self.ThreadProbe,QtCore.SIGNAL('Activated ( QString ) '), self.threadReceiveScan)
        self.ThreadProbe.setObjectName('::ThreadScanProbe')
        self.ThreadProbe.start()
        self.StartedProbe(True)