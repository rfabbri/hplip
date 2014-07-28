# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/devmgr4_base.ui'
#
# Created: Fri Feb 3 12:00:32 2012
#      by: The PyQt User Interface Compiler (pyuic) 3.18.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class DevMgr4_base(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0,latest_available_version="",Is_autoInstaller_distro=False):
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar()

        if not name:
            self.setName("DevMgr4_base")

        self.latest_available_version= latest_available_version
        self.Is_autoInstaller_distro= Is_autoInstaller_distro

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        DevMgr4_baseLayout = QGridLayout(self.centralWidget(),1,1,11,6,"DevMgr4_baseLayout")

        self.splitter2 = QSplitter(self.centralWidget(),"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter2,"layout8")
        layout8 = QVBoxLayout(LayoutWidget,11,6,"layout8")

        self.DeviceList = QIconView(LayoutWidget,"DeviceList")
        self.DeviceList.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred,0,0,self.DeviceList.sizePolicy().hasHeightForWidth()))
        self.DeviceList.setMinimumSize(QSize(0,0))
        self.DeviceList.setMaximumSize(QSize(32767,32767))
        self.DeviceList.setResizePolicy(QIconView.Manual)
        self.DeviceList.setArrangement(QIconView.TopToBottom)
        self.DeviceList.setResizeMode(QIconView.Adjust)
        layout8.addWidget(self.DeviceList)

        self.Tabs = QTabWidget(self.splitter2,"Tabs")

        self.FunctionsTab = QWidget(self.Tabs,"FunctionsTab")
        FunctionsTabLayout = QGridLayout(self.FunctionsTab,1,1,11,6,"FunctionsTabLayout")

        self.iconList = QIconView(self.FunctionsTab,"iconList")
        self.iconList.setFrameShape(QIconView.StyledPanel)
        self.iconList.setFrameShadow(QIconView.Sunken)
        self.iconList.setSelectionMode(QIconView.Single)
        self.iconList.setGridX(100)
        self.iconList.setGridY(100)
        self.iconList.setResizeMode(QIconView.Adjust)
        self.iconList.setShowToolTips(0)

        FunctionsTabLayout.addWidget(self.iconList,0,0)
        self.Tabs.insertTab(self.FunctionsTab,QString.fromLatin1(""))

        self.StatusTab = QWidget(self.Tabs,"StatusTab")
        StatusTabLayout = QGridLayout(self.StatusTab,1,1,11,6,"StatusTabLayout")

        self.statusListView = QListView(self.StatusTab,"statusListView")
        self.statusListView.addColumn(QString.null)
        self.statusListView.addColumn(self.__tr("Description"))
        self.statusListView.addColumn(self.__tr("Date and Time"))
        self.statusListView.addColumn(self.__tr("Code"))
        self.statusListView.addColumn(self.__tr("Job ID"))
        self.statusListView.addColumn(self.__tr("User"))
        self.statusListView.setSelectionMode(QListView.NoSelection)
        self.statusListView.setAllColumnsShowFocus(1)
        self.statusListView.setResizeMode(QListView.NoColumn)

        StatusTabLayout.addWidget(self.statusListView,1,0)

        layout11 = QHBoxLayout(None,0,6,"layout11")
        spacer3 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer3)

        self.panel = QLabel(self.StatusTab,"panel")
        self.panel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.panel.sizePolicy().hasHeightForWidth()))
        self.panel.setMinimumSize(QSize(254,40))
        self.panel.setScaledContents(1)
        layout11.addWidget(self.panel)
        spacer4 = QSpacerItem(21,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer4)

        StatusTabLayout.addLayout(layout11,0,0)
        self.Tabs.insertTab(self.StatusTab,QString.fromLatin1(""))

        self.SuppliesTab = QWidget(self.Tabs,"SuppliesTab")
        SuppliesTabLayout = QGridLayout(self.SuppliesTab,1,1,11,6,"SuppliesTabLayout")

        self.suppliesList = QListView(self.SuppliesTab,"suppliesList")
        self.suppliesList.addColumn(QString.null)
        self.suppliesList.addColumn(self.__tr("Description"))
        self.suppliesList.addColumn(self.__tr("HP Part No."))
        self.suppliesList.addColumn(self.__tr("Approx. Level"))
        self.suppliesList.addColumn(self.__tr("Status"))
        self.suppliesList.setSelectionMode(QListView.NoSelection)
        self.suppliesList.setAllColumnsShowFocus(1)
        self.suppliesList.setResizeMode(QListView.NoColumn)

        SuppliesTabLayout.addWidget(self.suppliesList,0,0)
        self.Tabs.insertTab(self.SuppliesTab,QString.fromLatin1(""))

        self.PrintSettingsTab = QWidget(self.Tabs,"PrintSettingsTab")
        self.Tabs.insertTab(self.PrintSettingsTab,QString.fromLatin1(""))

        self.PrintJobsTab = QWidget(self.Tabs,"PrintJobsTab")
        PrintJobsTabLayout = QGridLayout(self.PrintJobsTab,1,1,11,6,"PrintJobsTabLayout")

        self.groupBox2 = QGroupBox(self.PrintJobsTab,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.jobList = QListView(self.groupBox2,"jobList")
        self.jobList.addColumn(QString.null)
        self.jobList.addColumn(QString.null)
        self.jobList.addColumn(self.__tr("Title/Description"))
        self.jobList.addColumn(self.__tr("Status"))
        self.jobList.addColumn(self.__tr("Job ID"))
        self.jobList.setSelectionMode(QListView.NoSelection)
        self.jobList.setAllColumnsShowFocus(1)
        self.jobList.setResizeMode(QListView.NoColumn)

        groupBox2Layout.addMultiCellWidget(self.jobList,0,0,0,2)

        self.cancelToolButton = QToolButton(self.groupBox2,"cancelToolButton")
        self.cancelToolButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.cancelToolButton.sizePolicy().hasHeightForWidth()))
        self.cancelToolButton.setMinimumSize(QSize(32,32))

        groupBox2Layout.addWidget(self.cancelToolButton,1,0)

        self.infoToolButton = QToolButton(self.groupBox2,"infoToolButton")
        self.infoToolButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.infoToolButton.sizePolicy().hasHeightForWidth()))
        self.infoToolButton.setMinimumSize(QSize(32,32))

        groupBox2Layout.addWidget(self.infoToolButton,1,1)
        spacer5 = QSpacerItem(360,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer5,1,2)

        PrintJobsTabLayout.addMultiCellWidget(self.groupBox2,2,2,0,3)

        self.groupBox1 = QGroupBox(self.PrintJobsTab,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.defaultPushButton = QPushButton(self.groupBox1,"defaultPushButton")

        groupBox1Layout.addWidget(self.defaultPushButton,0,2)

        self.rejectacceptPushButton = QPushButton(self.groupBox1,"rejectacceptPushButton")

        groupBox1Layout.addWidget(self.rejectacceptPushButton,0,1)

        self.stopstartPushButton = QPushButton(self.groupBox1,"stopstartPushButton")

        groupBox1Layout.addWidget(self.stopstartPushButton,0,0)

        PrintJobsTabLayout.addMultiCellWidget(self.groupBox1,1,1,0,3)
        spacer6 = QSpacerItem(20,20,QSizePolicy.Preferred,QSizePolicy.Minimum)
        PrintJobsTabLayout.addItem(spacer6,0,0)
        spacer7 = QSpacerItem(20,20,QSizePolicy.Preferred,QSizePolicy.Minimum)
        PrintJobsTabLayout.addItem(spacer7,0,3)

        self.PrintJobPrinterCombo = QComboBox(0,self.PrintJobsTab,"PrintJobPrinterCombo")
        self.PrintJobPrinterCombo.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.PrintJobPrinterCombo.sizePolicy().hasHeightForWidth()))
        self.PrintJobPrinterCombo.setMinimumSize(QSize(0,0))

        PrintJobsTabLayout.addWidget(self.PrintJobPrinterCombo,0,2)

        self.printerTextLabel = QLabel(self.PrintJobsTab,"printerTextLabel")

        PrintJobsTabLayout.addWidget(self.printerTextLabel,0,1)
        self.Tabs.insertTab(self.PrintJobsTab,QString.fromLatin1(""))
        if self.latest_available_version is not "":
            self.UpgradeTab = QWidget(self.Tabs,"UpgradeTab")
            self.UpgradeLabel = QLabel(self.UpgradeTab,"UpgradeLabel")
            msg="Latest 'HPLIP-%s' version available for Installation"%self.latest_available_version
            self.UpgradeLabel.setText(self.__tr(msg))
            self.UpgradeLabel.setGeometry(QRect(17,43,330,20))
            if self.Is_autoInstaller_distro:
                self.InstallPushButton = QPushButton(self.UpgradeTab,"InstallPushButton")
                self.InstallPushButton.setText(self.__tr("Install Now"))
                self.InstallPushButton.setGeometry(QRect(390,40,111,30))
            else:
                self.ManualInfoLabel = QLabel(self.UpgradeTab,"ManualInfoLabel")
                msg="Please install manually as mentioned in "
                self.ManualInfoLabel.setText(self.__tr(msg))
                self.ManualInfoLabel.setGeometry(QRect(17,70,300,30))
                
                self.InstallPushButton = QPushButton(self.UpgradeTab,"InstallPushButton")
                self.InstallPushButton.setText(self.__tr("HPLIP website"))
                self.InstallPushButton.setGeometry(QRect(260,70,100,25))
            
            self.Tabs.insertTab(self.UpgradeTab,QString.fromLatin1(""))
            

        DevMgr4_baseLayout.addWidget(self.splitter2,0,0)

        self.helpContentsAction = QAction(self,"helpContentsAction")
        self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpIndexAction.setEnabled(0)
        self.helpAboutAction = QAction(self,"helpAboutAction")
        self.deviceRescanAction = QAction(self,"deviceRescanAction")
        self.deviceExitAction = QAction(self,"deviceExitAction")
        self.settingsPopupAlertsAction = QAction(self,"settingsPopupAlertsAction")
        self.settingsEmailAlertsAction = QAction(self,"settingsEmailAlertsAction")
        self.settingsConfigure = QAction(self,"settingsConfigure")
        self.deviceRefreshAll = QAction(self,"deviceRefreshAll")
        self.autoRefresh = QAction(self,"autoRefresh")
        self.autoRefresh.setToggleAction(1)
        self.autoRefresh.setOn(1)
        self.setupDevice = QAction(self,"setupDevice")
        self.setupDevice.setEnabled(0)
        self.viewSupportAction = QAction(self,"viewSupportAction")
        self.deviceInstallAction = QAction(self,"deviceInstallAction")
        self.deviceRemoveAction = QAction(self,"deviceRemoveAction")


        self.Toolbar = QToolBar(QString(""),self,Qt.DockTop)



        self.MenuBar = QMenuBar(self,"MenuBar")

        self.MenuBar.setAcceptDrops(0)

        self.Device = QPopupMenu(self)
        self.setupDevice.addTo(self.Device)
        self.Device.insertSeparator()
        self.deviceRescanAction.addTo(self.Device)
        self.deviceRefreshAll.addTo(self.Device)
        self.Device.insertSeparator()
        self.deviceInstallAction.addTo(self.Device)
        self.deviceRemoveAction.addTo(self.Device)
        self.Device.insertSeparator()
        self.deviceExitAction.addTo(self.Device)
        self.MenuBar.insertItem(QString(""),self.Device,2)

        self.Configure = QPopupMenu(self)
        self.settingsConfigure.addTo(self.Configure)
        self.MenuBar.insertItem(QString(""),self.Configure,3)

        self.helpMenu = QPopupMenu(self)
        self.helpContentsAction.addTo(self.helpMenu)
        self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.MenuBar.insertItem(QString(""),self.helpMenu,4)

        self.MenuBar.insertSeparator(5)


        self.languageChange()

        self.resize(QSize(778,505).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
        self.connect(self.helpContentsAction,SIGNAL("activated()"),self.helpContents)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)
        self.connect(self.deviceExitAction,SIGNAL("activated()"),self.close)
        self.connect(self.deviceRescanAction,SIGNAL("activated()"),self.deviceRescanAction_activated)
        self.connect(self.settingsConfigure,SIGNAL("activated()"),self.settingsConfigure_activated)
        self.connect(self.DeviceList,SIGNAL("currentChanged(QIconViewItem*)"),self.DeviceList_currentChanged)
        self.connect(self.deviceRefreshAll,SIGNAL("activated()"),self.deviceRefreshAll_activated)
        self.connect(self.DeviceList,SIGNAL("clicked(QIconViewItem*)"),self.DeviceList_clicked)
        self.connect(self.DeviceList,SIGNAL("rightButtonClicked(QIconViewItem*,const QPoint&)"),self.DeviceList_rightButtonClicked)
        self.connect(self.setupDevice,SIGNAL("activated()"),self.setupDevice_activated)
        self.connect(self.viewSupportAction,SIGNAL("activated()"),self.viewSupportAction_activated)
        self.connect(self.deviceInstallAction,SIGNAL("activated()"),self.deviceInstallAction_activated)
        self.connect(self.deviceRemoveAction,SIGNAL("activated()"),self.deviceRemoveAction_activated)
        self.connect(self.DeviceList,SIGNAL("onItem(QIconViewItem*)"),self.DeviceList_onItem)
        self.connect(self.Tabs,SIGNAL("currentChanged(QWidget*)"),self.Tabs_currentChanged)
        self.connect(self.PrintJobPrinterCombo,SIGNAL("activated(const QString&)"),self.PrintJobPrinterCombo_activated)
        self.connect(self.stopstartPushButton,SIGNAL("clicked()"),self.stopstartPushButton_clicked)
        self.connect(self.rejectacceptPushButton,SIGNAL("clicked()"),self.rejectacceptPushButton_clicked)
        self.connect(self.defaultPushButton,SIGNAL("clicked()"),self.defaultPushButton_clicked)
        self.connect(self.iconList,SIGNAL("clicked(QIconViewItem*)"),self.iconList_clicked)
        self.connect(self.iconList,SIGNAL("contextMenuRequested(QIconViewItem*,const QPoint&)"),self.iconList_contextMenuRequested)
        self.connect(self.iconList,SIGNAL("returnPressed(QIconViewItem*)"),self.iconList_returnPressed)
        self.connect(self.jobList,SIGNAL("clicked(QListViewItem*)"),self.jobList_clicked)
        self.connect(self.infoToolButton,SIGNAL("clicked()"),self.infoToolButton_clicked)
        self.connect(self.cancelToolButton,SIGNAL("clicked()"),self.cancelToolButton_clicked)
        self.connect(self.jobList,SIGNAL("contextMenuRequested(QListViewItem*,const QPoint&,int)"),self.jobList_contextMenuRequested)
        if self.latest_available_version is not "":
            self.connect(self.InstallPushButton,SIGNAL("clicked()"),self.InstallPushButton_clicked)

    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager"))
        self.Tabs.changeTab(self.FunctionsTab,self.__tr("Actions"))
        self.statusListView.header().setLabel(0,QString.null)
        self.statusListView.header().setLabel(1,self.__tr("Description"))
        self.statusListView.header().setLabel(2,self.__tr("Date and Time"))
        self.statusListView.header().setLabel(3,self.__tr("Code"))
        self.statusListView.header().setLabel(4,self.__tr("Job ID"))
        self.statusListView.header().setLabel(5,self.__tr("User"))
        self.Tabs.changeTab(self.StatusTab,self.__tr("Status"))
        self.suppliesList.header().setLabel(0,QString.null)
        self.suppliesList.header().setLabel(1,self.__tr("Description"))
        self.suppliesList.header().setLabel(2,self.__tr("HP Part No."))
        self.suppliesList.header().setLabel(3,self.__tr("Approx. Level"))
        self.suppliesList.header().setLabel(4,self.__tr("Status"))
        self.Tabs.changeTab(self.SuppliesTab,self.__tr("Supplies"))
        self.Tabs.changeTab(self.PrintSettingsTab,self.__tr("Print Settings"))
        self.groupBox2.setTitle(self.__tr("Active Jobs"))
        self.jobList.header().setLabel(0,QString.null)
        self.jobList.header().setLabel(1,QString.null)
        self.jobList.header().setLabel(2,self.__tr("Title/Description"))
        self.jobList.header().setLabel(3,self.__tr("Status"))
        self.jobList.header().setLabel(4,self.__tr("Job ID"))
        self.cancelToolButton.setText(QString.null)
        self.infoToolButton.setText(QString.null)
        self.groupBox1.setTitle(self.__tr("Printer Queue Control"))
        self.defaultPushButton.setText(self.__tr("Set As Default"))
        self.rejectacceptPushButton.setText(self.__tr("Reject Jobs"))
        self.stopstartPushButton.setText(self.__tr("Stop Printer"))
        self.printerTextLabel.setText(self.__tr("Printer Name:"))
        self.Tabs.changeTab(self.PrintJobsTab,self.__tr("Print Control"))
        if self.latest_available_version is not "":
            self.Tabs.changeTab(self.UpgradeTab,self.__tr("Upgrade"))
        self.helpContentsAction.setText(self.__tr("Contents"))
        self.helpContentsAction.setMenuText(self.__tr("&Contents..."))
        self.helpContentsAction.setToolTip(self.__tr("Help Contents (F1)"))
        self.helpContentsAction.setAccel(self.__tr("F1"))
        self.helpIndexAction.setText(self.__tr("Index"))
        self.helpIndexAction.setMenuText(self.__tr("&Index..."))
        self.helpIndexAction.setAccel(QString.null)
        self.helpAboutAction.setText(self.__tr("&About..."))
        self.helpAboutAction.setMenuText(self.__tr("&About..."))
        self.helpAboutAction.setToolTip(self.__tr("About HP Device Manager..."))
        self.deviceRescanAction.setText(self.__tr("Refresh Device"))
        self.deviceRescanAction.setMenuText(self.__tr("Refresh Device"))
        self.deviceRescanAction.setToolTip(self.__tr("Refresh Device (F5)"))
        self.deviceRescanAction.setAccel(self.__tr("F5"))
        self.deviceExitAction.setText(self.__tr("Exit"))
        self.deviceExitAction.setMenuText(self.__tr("Exit"))
        self.deviceExitAction.setToolTip(self.__tr("Exit HP Device Manager"))
        self.deviceExitAction.setAccel(self.__tr("Ctrl+Q"))
        self.settingsPopupAlertsAction.setText(self.__tr("Popup Alerts..."))
        self.settingsPopupAlertsAction.setMenuText(self.__tr("Popup alerts..."))
        self.settingsPopupAlertsAction.setToolTip(self.__tr("Configure popup alerts"))
        self.settingsEmailAlertsAction.setText(self.__tr("Email alerts..."))
        self.settingsEmailAlertsAction.setMenuText(self.__tr("Email alerts..."))
        self.settingsEmailAlertsAction.setToolTip(self.__tr("Configure email alerts"))
        self.settingsConfigure.setText(self.__tr("Settings..."))
        self.settingsConfigure.setAccel(self.__tr("F2"))
        self.deviceRefreshAll.setText(self.__tr("Refresh All"))
        self.deviceRefreshAll.setAccel(self.__tr("F6"))
        self.autoRefresh.setText(self.__tr("Auto Refresh"))
        self.autoRefresh.setToolTip(self.__tr("Turn on/off Auto Refresh (Ctrl+A)"))
        self.autoRefresh.setAccel(self.__tr("Ctrl+A"))
        self.setupDevice.setText(self.__tr("Action"))
        self.setupDevice.setMenuText(self.__tr("Settings..."))
        self.setupDevice.setToolTip(self.__tr("Device Settings (F3)"))
        self.setupDevice.setAccel(self.__tr("F3"))
        self.viewSupportAction.setText(self.__tr("Support..."))
        self.deviceInstallAction.setText(self.__tr("Setup New Device..."))
        self.deviceInstallAction.setMenuText(self.__tr("Setup New Device..."))
        self.deviceInstallAction.setAccel(self.__tr("Ins"))
        self.deviceRemoveAction.setText(self.__tr("Remove Device..."))
        self.deviceRemoveAction.setMenuText(self.__tr("Remove Device..."))
        self.deviceRemoveAction.setAccel(self.__tr("Del"))
        self.Toolbar.setLabel(self.__tr("Toolbar"))
        if self.MenuBar.findItem(2):
            self.MenuBar.findItem(2).setText(self.__tr("Device"))
        if self.MenuBar.findItem(3):
            self.MenuBar.findItem(3).setText(self.__tr("Configure"))
        if self.MenuBar.findItem(4):
            self.MenuBar.findItem(4).setText(self.__tr("&Help"))


    def fileNew(self):
        print "DevMgr4_base.fileNew(): Not implemented yet"

    def fileOpen(self):
        print "DevMgr4_base.fileOpen(): Not implemented yet"

    def fileSave(self):
        print "DevMgr4_base.fileSave(): Not implemented yet"

    def fileSaveAs(self):
        print "DevMgr4_base.fileSaveAs(): Not implemented yet"

    def filePrint(self):
        print "DevMgr4_base.filePrint(): Not implemented yet"

    def fileExit(self):
        print "DevMgr4_base.fileExit(): Not implemented yet"

    def editUndo(self):
        print "DevMgr4_base.editUndo(): Not implemented yet"

    def editRedo(self):
        print "DevMgr4_base.editRedo(): Not implemented yet"

    def editCut(self):
        print "DevMgr4_base.editCut(): Not implemented yet"

    def editCopy(self):
        print "DevMgr4_base.editCopy(): Not implemented yet"

    def editPaste(self):
        print "DevMgr4_base.editPaste(): Not implemented yet"

    def editFind(self):
        print "DevMgr4_base.editFind(): Not implemented yet"

    def helpIndex(self):
        print "DevMgr4_base.helpIndex(): Not implemented yet"

    def helpContents(self):
        print "DevMgr4_base.helpContents(): Not implemented yet"

    def helpAbout(self):
        print "DevMgr4_base.helpAbout(): Not implemented yet"

    def deviceRescanAction_activated(self):
        print "DevMgr4_base.deviceRescanAction_activated(): Not implemented yet"

    def settingsEmailAlertsAction_activated(self):
        print "DevMgr4_base.settingsEmailAlertsAction_activated(): Not implemented yet"

    def DeviceList_currentChanged(self,a0):
        print "DevMgr4_base.DeviceList_currentChanged(QIconViewItem*): Not implemented yet"

    def CleanPensButton_clicked(self):
        print "DevMgr4_base.CleanPensButton_clicked(): Not implemented yet"

    def AlignPensButton_clicked(self):
        print "DevMgr4_base.AlignPensButton_clicked(): Not implemented yet"

    def PrintTestPageButton_clicked(self):
        print "DevMgr4_base.PrintTestPageButton_clicked(): Not implemented yet"

    def AdvancedInfoButton_clicked(self):
        print "DevMgr4_base.AdvancedInfoButton_clicked(): Not implemented yet"

    def ColorCalibrationButton_clicked(self):
        print "DevMgr4_base.ColorCalibrationButton_clicked(): Not implemented yet"

    def settingsConfigure_activated(self):
        print "DevMgr4_base.settingsConfigure_activated(): Not implemented yet"

    def PrintButton_clicked(self):
        print "DevMgr4_base.PrintButton_clicked(): Not implemented yet"

    def ScanButton_clicked(self):
        print "DevMgr4_base.ScanButton_clicked(): Not implemented yet"

    def PCardButton_clicked(self):
        print "DevMgr4_base.PCardButton_clicked(): Not implemented yet"

    def SendFaxButton_clicked(self):
        print "DevMgr4_base.SendFaxButton_clicked(): Not implemented yet"

    def MakeCopiesButton_clicked(self):
        print "DevMgr4_base.MakeCopiesButton_clicked(): Not implemented yet"

    def ConfigureFeaturesButton_clicked(self):
        print "DevMgr4_base.ConfigureFeaturesButton_clicked(): Not implemented yet"

    def CancelJobButton_clicked(self):
        print "DevMgr4_base.CancelJobButton_clicked(): Not implemented yet"

    def deviceRefreshAll_activated(self):
        print "DevMgr4_base.deviceRefreshAll_activated(): Not implemented yet"

    def DeviceList_clicked(self,a0):
        print "DevMgr4_base.DeviceList_clicked(QIconViewItem*): Not implemented yet"

    def autoRefresh_toggled(self,a0):
        print "DevMgr4_base.autoRefresh_toggled(bool): Not implemented yet"

    def PrintJobList_currentChanged(self,a0):
        print "DevMgr4_base.PrintJobList_currentChanged(QListViewItem*): Not implemented yet"

    def CancelPrintJobButton_clicked(self):
        print "DevMgr4_base.CancelPrintJobButton_clicked(): Not implemented yet"

    def PrintJobList_selectionChanged(self,a0):
        print "DevMgr4_base.PrintJobList_selectionChanged(QListViewItem*): Not implemented yet"

    def DeviceList_rightButtonClicked(self,a0,a1):
        print "DevMgr4_base.DeviceList_rightButtonClicked(QIconViewItem*,const QPoint&): Not implemented yet"

    def OpenEmbeddedBrowserButton_clicked(self):
        print "DevMgr4_base.OpenEmbeddedBrowserButton_clicked(): Not implemented yet"

    def deviceSettingsButton_clicked(self):
        print "DevMgr4_base.deviceSettingsButton_clicked(): Not implemented yet"

    def faxSetupWizardButton_clicked(self):
        print "DevMgr4_base.faxSetupWizardButton_clicked(): Not implemented yet"

    def faxSettingsButton_clicked(self):
        print "DevMgr4_base.faxSettingsButton_clicked(): Not implemented yet"

    def setupDevice_activated(self):
        print "DevMgr4_base.setupDevice_activated(): Not implemented yet"

    def viewSupportAction_activated(self):
        print "DevMgr4_base.viewSupportAction_activated(): Not implemented yet"

    def installDevice_activated(self):
        print "DevMgr4_base.installDevice_activated(): Not implemented yet"

    def deviceInstallAction_activated(self):
        print "DevMgr4_base.deviceInstallAction_activated(): Not implemented yet"

    def deviceRemoveAction_activated(self):
        print "DevMgr4_base.deviceRemoveAction_activated(): Not implemented yet"

    def Tabs_currentChanged(self,a0):
        print "DevMgr4_base.Tabs_currentChanged(QWidget*): Not implemented yet"

    def DeviceList_onItem(self,a0):
        print "DevMgr4_base.DeviceList_onItem(QIconViewItem*): Not implemented yet"

    def iconList_doubleClicked(self,a0):
        print "DevMgr4_base.iconList_doubleClicked(QIconViewItem*): Not implemented yet"

    def iconList_rightButtonClicked(self,a0,a1):
        print "DevMgr4_base.iconList_rightButtonClicked(QIconViewItem*,const QPoint&): Not implemented yet"

    def iconList_clicked(self,a0):
        print "DevMgr4_base.iconList_clicked(QIconViewItem*): Not implemented yet"

    def iconList_contextMenuRequested(self,a0,a1):
        print "DevMgr4_base.iconList_contextMenuRequested(QIconViewItem*,const QPoint&): Not implemented yet"

    def iconList_returnPressed(self,a0):
        print "DevMgr4_base.iconList_returnPressed(QIconViewItem*): Not implemented yet"

    def stopstartPushButton_clicked(self):
        print "DevMgr4_base.stopstartPushButton_clicked(): Not implemented yet"

    def rejectacceptPushButton_clicked(self):
        print "DevMgr4_base.rejectacceptPushButton_clicked(): Not implemented yet"

    def defaultPushButton_clicked(self):
        print "DevMgr4_base.defaultPushButton_clicked(): Not implemented yet"

    def PrintJobPrinterCombo_activated(self,a0):
        print "DevMgr4_base.PrintJobPrinterCombo_activated(const QString&): Not implemented yet"

    def PrintSettingsPrinterCombo_activated(self,a0):
        print "DevMgr4_base.PrintSettingsPrinterCombo_activated(const QString&): Not implemented yet"

    def jobList_rightButtonClicked(self,a0,a1,a2):
        print "DevMgr4_base.jobList_rightButtonClicked(QListViewItem*,const QPoint&,int): Not implemented yet"

    def jobList_clicked(self,a0):
        print "DevMgr4_base.jobList_clicked(QListViewItem*): Not implemented yet"

    def infoToolButton_clicked(self):
        print "DevMgr4_base.infoToolButton_clicked(): Not implemented yet"

    def cancelToolButton_clicked(self):
        print "DevMgr4_base.cancelToolButton_clicked(): Not implemented yet"

    def InstallPushButton_clicked(self):
        print "DevMgr4_base.InstallPushButton_clicked(): Not implemented yet"
        
    def jobList_contextMenuRequested(self,a0,a1,a2):
        print "DevMgr4_base.jobList_contextMenuRequested(QListViewItem*,const QPoint&,int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("DevMgr4_base",s,c)
