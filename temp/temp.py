# Initializer For Plugins
        self.scenarioName = [self.check_noproxy]
        self.scenarioDesc = [self.check_noproxy.objectName()]
        self.scenarioSettings = [QtGui.QPushButton("None")]
        self.proxyGroup.addButton(self.check_noproxy)
        for scenario in self.main_method.proxymodel:
            self.scenarioName.append(scenario.plugin_radio)
            self.scenarioSettings.append(scenario.btnChangeSettings)
            self.scenarioDesc.append(scenario.plugin_radio.objectName())
            self.proxyGroup.addButton(scenario.plugin_radio)

        # table 1 for add plugins with QradioBtton
        self.THeadersPluginsProxy = OrderedDict(
            [('Plugins', self.scenarioName),
             ('Settings', self.scenarioSettings),
             ('Description', self.scenarioDesc)
             ])

        self.tableplugins.setRowCount(len(self.THeadersPluginsProxy['Plugins']))
        self.tableplugins.resizeRowsToContents()
        self.tableplugins.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.tableplugins.horizontalHeader().setStretchLastSection(True)
        self.tableplugins.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableplugins.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableplugins.verticalHeader().setVisible(False)
        self.tableplugins.verticalHeader().setDefaultSectionSize(23)
        self.tableplugins.setSortingEnabled(True)
        self.tableplugins.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())
        self.tableplugins.horizontalHeader().resizeSection(0, 158)
        self.tableplugins.horizontalHeader().resizeSection(1, 80)
        self.tableplugins.resizeRowsToContents()
        # add all widgets in Qtable 1 plgins
        Headers = []
        for n, key in enumerate(self.THeadersPluginsProxy.keys()):
            Headers.append(key)
            for m, item in enumerate(self.THeadersPluginsProxy[key]):
                if type(item) == type(QtGui.QRadioButton()) or type(item) == type(QtGui.QPushButton()):
                    self.tableplugins.setCellWidget(m, n, item)
                else:
                    item = QtGui.QTableWidgetItem(item)
                    self.tableplugins.setItem(m, n, item)
        self.tableplugins.setHorizontalHeaderLabels(self.THeadersPluginsProxy.keys())