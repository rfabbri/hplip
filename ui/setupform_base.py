# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/setupform_base.ui'
#
# Created: Thu Sep 20 11:45:16 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SetupForm_base(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SetupForm_base")



        self.ConnectionPage = QWidget(self,"ConnectionPage")
        ConnectionPageLayout = QGridLayout(self.ConnectionPage,1,1,11,6,"ConnectionPageLayout")

        self.connectionTypeButtonGroup = QButtonGroup(self.ConnectionPage,"connectionTypeButtonGroup")
        self.connectionTypeButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.connectionTypeButtonGroup.layout().setSpacing(6)
        self.connectionTypeButtonGroup.layout().setMargin(11)
        connectionTypeButtonGroupLayout = QGridLayout(self.connectionTypeButtonGroup.layout())
        connectionTypeButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.usbRadioButton = QRadioButton(self.connectionTypeButtonGroup,"usbRadioButton")

        connectionTypeButtonGroupLayout.addWidget(self.usbRadioButton,0,0)

        self.netRadioButton = QRadioButton(self.connectionTypeButtonGroup,"netRadioButton")

        connectionTypeButtonGroupLayout.addWidget(self.netRadioButton,1,0)

        self.parRadioButton = QRadioButton(self.connectionTypeButtonGroup,"parRadioButton")

        connectionTypeButtonGroupLayout.addWidget(self.parRadioButton,2,0)

        ConnectionPageLayout.addMultiCellWidget(self.connectionTypeButtonGroup,1,1,0,1)
        spacer12 = QSpacerItem(20,120,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ConnectionPageLayout.addItem(spacer12,2,0)
        spacer18 = QSpacerItem(321,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ConnectionPageLayout.addItem(spacer18,3,1)

        self.searchFiltersPushButton2 = QPushButton(self.ConnectionPage,"searchFiltersPushButton2")

        ConnectionPageLayout.addWidget(self.searchFiltersPushButton2,3,0)
        self.addPage(self.ConnectionPage,QString(""))

        self.ProbedDevicesPage = QWidget(self,"ProbedDevicesPage")
        ProbedDevicesPageLayout = QGridLayout(self.ProbedDevicesPage,1,1,11,6,"ProbedDevicesPageLayout")

        self.probedDevicesListView = QListView(self.ProbedDevicesPage,"probedDevicesListView")
        self.probedDevicesListView.setAllColumnsShowFocus(1)

        ProbedDevicesPageLayout.addMultiCellWidget(self.probedDevicesListView,1,1,0,3)

        self.searchFiltersPushButton = QPushButton(self.ProbedDevicesPage,"searchFiltersPushButton")

        ProbedDevicesPageLayout.addWidget(self.searchFiltersPushButton,2,0)

        self.probeHeadingTextLabel = QLabel(self.ProbedDevicesPage,"probeHeadingTextLabel")

        ProbedDevicesPageLayout.addMultiCellWidget(self.probeHeadingTextLabel,0,0,0,3)

        self.manualFindPushButton = QPushButton(self.ProbedDevicesPage,"manualFindPushButton")

        ProbedDevicesPageLayout.addWidget(self.manualFindPushButton,2,1)
        spacer13 = QSpacerItem(101,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ProbedDevicesPageLayout.addItem(spacer13,2,2)

        self.probeUpdatePushButton = QPushButton(self.ProbedDevicesPage,"probeUpdatePushButton")

        ProbedDevicesPageLayout.addWidget(self.probeUpdatePushButton,2,3)
        self.addPage(self.ProbedDevicesPage,QString(""))

        self.PPDPage = QWidget(self,"PPDPage")
        PPDPageLayout = QGridLayout(self.PPDPage,1,1,11,6,"PPDPageLayout")

        self.ppdListView = QListView(self.PPDPage,"ppdListView")
        self.ppdListView.addColumn(self.__tr("PPD File"))
        self.ppdListView.addColumn(self.__tr("Description"))
        self.ppdListView.setAllColumnsShowFocus(1)

        PPDPageLayout.addMultiCellWidget(self.ppdListView,1,1,0,2)

        self.otherPPDPushButton = QPushButton(self.PPDPage,"otherPPDPushButton")
        self.otherPPDPushButton.setEnabled(1)

        PPDPageLayout.addWidget(self.otherPPDPushButton,2,0)
        spacer9 = QSpacerItem(320,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PPDPageLayout.addItem(spacer9,2,1)

        self.ppdDefaultsPushButton = QPushButton(self.PPDPage,"ppdDefaultsPushButton")

        PPDPageLayout.addWidget(self.ppdDefaultsPushButton,2,2)

        self.textLabel1_5 = QLabel(self.PPDPage,"textLabel1_5")
        self.textLabel1_5.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        PPDPageLayout.addMultiCellWidget(self.textLabel1_5,0,0,0,2)
        self.addPage(self.PPDPage,QString(""))

        self.PrinterNamePage = QWidget(self,"PrinterNamePage")
        PrinterNamePageLayout = QGridLayout(self.PrinterNamePage,1,1,11,6,"PrinterNamePageLayout")

        self.groupBox4 = QGroupBox(self.PrinterNamePage,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.printerNameLineEdit = QLineEdit(self.groupBox4,"printerNameLineEdit")
        self.printerNameLineEdit.setMaxLength(50)

        groupBox4Layout.addWidget(self.printerNameLineEdit,0,1)

        self.defaultPrinterNamePushButton = QPushButton(self.groupBox4,"defaultPrinterNamePushButton")
        self.defaultPrinterNamePushButton.setEnabled(0)

        groupBox4Layout.addWidget(self.defaultPrinterNamePushButton,0,2)

        self.textLabel1_2 = QLabel(self.groupBox4,"textLabel1_2")

        groupBox4Layout.addWidget(self.textLabel1_2,1,0)

        self.textLabel1 = QLabel(self.groupBox4,"textLabel1")

        groupBox4Layout.addWidget(self.textLabel1,0,0)

        self.printerDescriptionLineEdit = QLineEdit(self.groupBox4,"printerDescriptionLineEdit")
        self.printerDescriptionLineEdit.setMaxLength(50)

        groupBox4Layout.addWidget(self.printerDescriptionLineEdit,2,1)

        self.printerLocationLineEdit = QLineEdit(self.groupBox4,"printerLocationLineEdit")
        self.printerLocationLineEdit.setMaxLength(50)

        groupBox4Layout.addWidget(self.printerLocationLineEdit,1,1)

        self.textLabel2 = QLabel(self.groupBox4,"textLabel2")

        groupBox4Layout.addWidget(self.textLabel2,2,0)

        PrinterNamePageLayout.addWidget(self.groupBox4,0,0)

        self.faxInfoGroupBox = QGroupBox(self.PrinterNamePage,"faxInfoGroupBox")
        self.faxInfoGroupBox.setColumnLayout(0,Qt.Vertical)
        self.faxInfoGroupBox.layout().setSpacing(6)
        self.faxInfoGroupBox.layout().setMargin(11)
        faxInfoGroupBoxLayout = QGridLayout(self.faxInfoGroupBox.layout())
        faxInfoGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.faxNameLineEdit = QLineEdit(self.faxInfoGroupBox,"faxNameLineEdit")

        faxInfoGroupBoxLayout.addWidget(self.faxNameLineEdit,1,1)

        self.textLabel1_3 = QLabel(self.faxInfoGroupBox,"textLabel1_3")

        faxInfoGroupBoxLayout.addWidget(self.textLabel1_3,1,0)

        self.textLabel3 = QLabel(self.faxInfoGroupBox,"textLabel3")

        faxInfoGroupBoxLayout.addWidget(self.textLabel3,3,0)

        self.textLabel2_2 = QLabel(self.faxInfoGroupBox,"textLabel2_2")

        faxInfoGroupBoxLayout.addWidget(self.textLabel2_2,2,0)

        self.faxCheckBox = QCheckBox(self.faxInfoGroupBox,"faxCheckBox")
        self.faxCheckBox.setChecked(1)

        faxInfoGroupBoxLayout.addMultiCellWidget(self.faxCheckBox,0,0,0,2)

        self.faxNumberLineEdit = QLineEdit(self.faxInfoGroupBox,"faxNumberLineEdit")
        self.faxNumberLineEdit.setMaxLength(50)

        faxInfoGroupBoxLayout.addWidget(self.faxNumberLineEdit,2,1)

        self.faxNameCoLineEdit = QLineEdit(self.faxInfoGroupBox,"faxNameCoLineEdit")
        self.faxNameCoLineEdit.setMaxLength(50)

        faxInfoGroupBoxLayout.addWidget(self.faxNameCoLineEdit,3,1)

        self.defaultFaxNamePushButton = QPushButton(self.faxInfoGroupBox,"defaultFaxNamePushButton")
        self.defaultFaxNamePushButton.setEnabled(0)

        faxInfoGroupBoxLayout.addWidget(self.defaultFaxNamePushButton,1,2)

        self.textLabel1_2_2 = QLabel(self.faxInfoGroupBox,"textLabel1_2_2")

        faxInfoGroupBoxLayout.addWidget(self.textLabel1_2_2,4,0)

        self.textLabel2_4 = QLabel(self.faxInfoGroupBox,"textLabel2_4")

        faxInfoGroupBoxLayout.addWidget(self.textLabel2_4,5,0)

        self.faxLocationLineEdit = QLineEdit(self.faxInfoGroupBox,"faxLocationLineEdit")
        self.faxLocationLineEdit.setMaxLength(50)

        faxInfoGroupBoxLayout.addWidget(self.faxLocationLineEdit,4,1)

        self.faxDescriptionLineEdit = QLineEdit(self.faxInfoGroupBox,"faxDescriptionLineEdit")
        self.faxDescriptionLineEdit.setMaxLength(50)

        faxInfoGroupBoxLayout.addWidget(self.faxDescriptionLineEdit,5,1)

        PrinterNamePageLayout.addWidget(self.faxInfoGroupBox,1,0)

        self.textLabel1_4 = QLabel(self.PrinterNamePage,"textLabel1_4")

        PrinterNamePageLayout.addWidget(self.textLabel1_4,3,0)
        spacer14 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PrinterNamePageLayout.addItem(spacer14,2,0)
        self.addPage(self.PrinterNamePage,QString(""))

        self.FinishedPage = QWidget(self,"FinishedPage")
        FinishedPageLayout = QGridLayout(self.FinishedPage,1,1,11,6,"FinishedPageLayout")

        self.printTestPageCheckBox = QCheckBox(self.FinishedPage,"printTestPageCheckBox")
        self.printTestPageCheckBox.setChecked(1)

        FinishedPageLayout.addWidget(self.printTestPageCheckBox,4,0)
        spacer7 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        FinishedPageLayout.addItem(spacer7,3,0)

        self.faxGroupBox = QGroupBox(self.FinishedPage,"faxGroupBox")
        self.faxGroupBox.setEnabled(0)
        self.faxGroupBox.setColumnLayout(0,Qt.Vertical)
        self.faxGroupBox.layout().setSpacing(6)
        self.faxGroupBox.layout().setMargin(11)
        faxGroupBoxLayout = QGridLayout(self.faxGroupBox.layout())
        faxGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.textLabel7 = QLabel(self.faxGroupBox,"textLabel7")

        faxGroupBoxLayout.addWidget(self.textLabel7,0,0)

        self.lineEdit5 = QLineEdit(self.faxGroupBox,"lineEdit5")
        self.lineEdit5.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit5.setReadOnly(1)

        faxGroupBoxLayout.addWidget(self.lineEdit5,0,1)

        self.lineEdit6 = QLineEdit(self.faxGroupBox,"lineEdit6")
        self.lineEdit6.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit6.setReadOnly(1)

        faxGroupBoxLayout.addWidget(self.lineEdit6,1,1)

        self.textLabel6 = QLabel(self.faxGroupBox,"textLabel6")

        faxGroupBoxLayout.addWidget(self.textLabel6,1,0)

        self.textLabel8 = QLabel(self.faxGroupBox,"textLabel8")

        faxGroupBoxLayout.addWidget(self.textLabel8,2,0)

        self.textLabel8_2 = QLabel(self.faxGroupBox,"textLabel8_2")

        faxGroupBoxLayout.addWidget(self.textLabel8_2,3,0)

        self.lineEdit7 = QLineEdit(self.faxGroupBox,"lineEdit7")
        self.lineEdit7.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit7.setReadOnly(1)

        faxGroupBoxLayout.addWidget(self.lineEdit7,2,1)

        self.textLabel8_3 = QLabel(self.faxGroupBox,"textLabel8_3")

        faxGroupBoxLayout.addWidget(self.textLabel8_3,4,0)

        self.lineEdit8 = QLineEdit(self.faxGroupBox,"lineEdit8")
        self.lineEdit8.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit8.setReadOnly(1)

        faxGroupBoxLayout.addWidget(self.lineEdit8,3,1)

        self.lineEdit9 = QLineEdit(self.faxGroupBox,"lineEdit9")
        self.lineEdit9.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit9.setReadOnly(1)

        faxGroupBoxLayout.addWidget(self.lineEdit9,4,1)

        FinishedPageLayout.addWidget(self.faxGroupBox,2,0)

        self.groupBox3 = QGroupBox(self.FinishedPage,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.textLabel4 = QLabel(self.groupBox3,"textLabel4")

        groupBox3Layout.addWidget(self.textLabel4,2,0)

        self.textLabel3_2 = QLabel(self.groupBox3,"textLabel3_2")

        groupBox3Layout.addWidget(self.textLabel3_2,1,0)

        self.lineEdit4 = QLineEdit(self.groupBox3,"lineEdit4")
        self.lineEdit4.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit4.setReadOnly(1)

        groupBox3Layout.addWidget(self.lineEdit4,3,1)

        self.textLabel2_3 = QLabel(self.groupBox3,"textLabel2_3")

        groupBox3Layout.addWidget(self.textLabel2_3,0,0)

        self.lineEdit3 = QLineEdit(self.groupBox3,"lineEdit3")
        self.lineEdit3.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit3.setReadOnly(1)

        groupBox3Layout.addWidget(self.lineEdit3,2,1)

        self.lineEdit2 = QLineEdit(self.groupBox3,"lineEdit2")
        self.lineEdit2.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit2.setReadOnly(1)

        groupBox3Layout.addWidget(self.lineEdit2,1,1)

        self.lineEdit1 = QLineEdit(self.groupBox3,"lineEdit1")
        self.lineEdit1.setFrameShape(QLineEdit.NoFrame)
        self.lineEdit1.setReadOnly(1)

        groupBox3Layout.addWidget(self.lineEdit1,0,1)

        self.textLabel5 = QLabel(self.groupBox3,"textLabel5")

        groupBox3Layout.addWidget(self.textLabel5,3,0)

        FinishedPageLayout.addWidget(self.groupBox3,1,0)

        self.textLabel2_5 = QLabel(self.FinishedPage,"textLabel2_5")
        self.textLabel2_5.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        FinishedPageLayout.addWidget(self.textLabel2_5,0,0)
        self.addPage(self.FinishedPage,QString(""))

        self.languageChange()

        self.resize(QSize(754,456).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.connectionTypeButtonGroup,SIGNAL("clicked(int)"),self.connectionTypeButtonGroup_clicked)
        self.connect(self.probedDevicesListView,SIGNAL("currentChanged(QListViewItem*)"),self.probedDevicesListView_currentChanged)
        self.connect(self.printerNameLineEdit,SIGNAL("textChanged(const QString&)"),self.printerNameLineEdit_textChanged)
        self.connect(self.defaultPrinterNamePushButton,SIGNAL("clicked()"),self.defaultPrinterNamePushButton_clicked)
        self.connect(self.ppdListView,SIGNAL("currentChanged(QListViewItem*)"),self.ppdListView_currentChanged)
        self.connect(self.searchFiltersPushButton,SIGNAL("clicked()"),self.searchFiltersPushButton_clicked)
        self.connect(self.searchFiltersPushButton2,SIGNAL("clicked()"),self.searchFiltersPushButton2_clicked)
        self.connect(self.probeUpdatePushButton,SIGNAL("clicked()"),self.probeUpdatePushButton_clicked)
        self.connect(self.manualFindPushButton,SIGNAL("clicked()"),self.manualFindPushButton_clicked)
        self.connect(self.printerLocationLineEdit,SIGNAL("textChanged(const QString&)"),self.printerLocationLineEdit_textChanged)
        self.connect(self.printerDescriptionLineEdit,SIGNAL("textChanged(const QString&)"),self.printerDescriptionLineEdit_textChanged)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxNameLineEdit.setEnabled)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxNumberLineEdit.setEnabled)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxNameCoLineEdit.setEnabled)
        self.connect(self.faxNameLineEdit,SIGNAL("textChanged(const QString&)"),self.faxNameLineEdit_textChanged)
        self.connect(self.faxNumberLineEdit,SIGNAL("textChanged(const QString&)"),self.faxNumberLineEdit_textChanged)
        self.connect(self.faxNameCoLineEdit,SIGNAL("textChanged(const QString&)"),self.faxNameCoLineEdit_textChanged)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxCheckBox_toggled)
        self.connect(self.printTestPageCheckBox,SIGNAL("toggled(bool)"),self.printTestPageCheckBox_toggled)
        self.connect(self.defaultFaxNamePushButton,SIGNAL("clicked()"),self.defaultFaxNamePushButton_clicked)
        self.connect(self.otherPPDPushButton,SIGNAL("clicked()"),self.otherPPDPushButton_clicked)
        self.connect(self.ppdDefaultsPushButton,SIGNAL("clicked()"),self.ppdDefaultsPushButton_clicked)
        self.connect(self.faxLocationLineEdit,SIGNAL("textChanged(const QString&)"),self.faxLocationLineEdit_textChanged)
        self.connect(self.faxDescriptionLineEdit,SIGNAL("textChanged(const QString&)"),self.faxDescriptionLineEdit_textChanged)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxLocationLineEdit.setEnabled)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxDescriptionLineEdit.setEnabled)

        self.setTabOrder(self.printerNameLineEdit,self.printerLocationLineEdit)
        self.setTabOrder(self.printerLocationLineEdit,self.printerDescriptionLineEdit)
        self.setTabOrder(self.printerDescriptionLineEdit,self.faxCheckBox)
        self.setTabOrder(self.faxCheckBox,self.faxNameLineEdit)
        self.setTabOrder(self.faxNameLineEdit,self.faxNumberLineEdit)
        self.setTabOrder(self.faxNumberLineEdit,self.faxNameCoLineEdit)
        self.setTabOrder(self.faxNameCoLineEdit,self.faxLocationLineEdit)
        self.setTabOrder(self.faxLocationLineEdit,self.faxDescriptionLineEdit)
        self.setTabOrder(self.faxDescriptionLineEdit,self.usbRadioButton)
        self.setTabOrder(self.usbRadioButton,self.netRadioButton)
        self.setTabOrder(self.netRadioButton,self.parRadioButton)
        self.setTabOrder(self.parRadioButton,self.searchFiltersPushButton2)
        self.setTabOrder(self.searchFiltersPushButton2,self.probedDevicesListView)
        self.setTabOrder(self.probedDevicesListView,self.searchFiltersPushButton)
        self.setTabOrder(self.searchFiltersPushButton,self.manualFindPushButton)
        self.setTabOrder(self.manualFindPushButton,self.probeUpdatePushButton)
        self.setTabOrder(self.probeUpdatePushButton,self.ppdListView)
        self.setTabOrder(self.ppdListView,self.otherPPDPushButton)
        self.setTabOrder(self.otherPPDPushButton,self.ppdDefaultsPushButton)
        self.setTabOrder(self.ppdDefaultsPushButton,self.defaultPrinterNamePushButton)
        self.setTabOrder(self.defaultPrinterNamePushButton,self.defaultFaxNamePushButton)
        self.setTabOrder(self.defaultFaxNamePushButton,self.lineEdit4)
        self.setTabOrder(self.lineEdit4,self.lineEdit3)
        self.setTabOrder(self.lineEdit3,self.lineEdit2)
        self.setTabOrder(self.lineEdit2,self.lineEdit1)
        self.setTabOrder(self.lineEdit1,self.printTestPageCheckBox)
        self.setTabOrder(self.printTestPageCheckBox,self.lineEdit5)
        self.setTabOrder(self.lineEdit5,self.lineEdit6)
        self.setTabOrder(self.lineEdit6,self.lineEdit7)
        self.setTabOrder(self.lineEdit7,self.lineEdit8)
        self.setTabOrder(self.lineEdit8,self.lineEdit9)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manger - Printer Setup Wizard"))
        self.connectionTypeButtonGroup.setTitle(self.__tr("Connection (I/O) Type"))
        self.usbRadioButton.setText(self.__tr("Universal Serial Bus (USB)"))
        self.netRadioButton.setText(self.__tr("Network/Ethernet/Wireless (direct connection or JetDirect)"))
        self.parRadioButton.setText(self.__tr("Parallel Port (LPT)"))
        self.searchFiltersPushButton2.setText(self.__tr("Advanced..."))
        self.setTitle(self.ConnectionPage,self.__tr("Choose Connection Type"))
        self.searchFiltersPushButton.setText(self.__tr("Advanced..."))
        self.probeHeadingTextLabel.setText(self.__tr("probeHeadingTextLabel"))
        self.manualFindPushButton.setText(self.__tr("Find Manually..."))
        self.probeUpdatePushButton.setText(self.__tr("Refresh"))
        self.setTitle(self.ProbedDevicesPage,self.__tr("Select from Discovered Devices"))
        self.ppdListView.header().setLabel(0,self.__tr("PPD File"))
        self.ppdListView.header().setLabel(1,self.__tr("Description"))
        self.otherPPDPushButton.setText(self.__tr("Select Other..."))
        self.ppdDefaultsPushButton.setText(self.__tr("Defaults"))
        self.textLabel1_5.setText(self.__tr("Please choose the PPD file (by name and description) that most closely matches your printer. <i>Note: The model name of the printer may vary somewhat from the PPD file name, for example, a Deskjet 5550 may have a PPD file with the model name of Deskjet_5500_series.</i>"))
        self.setTitle(self.PPDPage,self.__tr("Select/Confirm PPD File"))
        self.groupBox4.setTitle(self.__tr("Printer Information"))
        self.defaultPrinterNamePushButton.setText(self.__tr("Default"))
        self.textLabel1_2.setText(self.__tr("Location:"))
        self.textLabel1.setText(self.__tr("Printer Name:"))
        self.textLabel2.setText(self.__tr("Description:"))
        self.faxInfoGroupBox.setTitle(self.__tr("Fax Information"))
        self.textLabel1_3.setText(self.__tr("Fax Name:"))
        self.textLabel3.setText(self.__tr("Name/Company:"))
        self.textLabel2_2.setText(self.__tr("Fax Number:"))
        self.faxCheckBox.setText(self.__tr("Setup PC send fax"))
        self.defaultFaxNamePushButton.setText(self.__tr("Default"))
        self.textLabel1_2_2.setText(self.__tr("Location:"))
        self.textLabel2_4.setText(self.__tr("Description:"))
        self.textLabel1_4.setText(self.__tr("Click \"Next >\" to install the printer on your system."))
        self.setTitle(self.PrinterNamePage,self.__tr("Enter Printer Information"))
        self.printTestPageCheckBox.setText(self.__tr("Send test page to printer"))
        self.faxGroupBox.setTitle(self.__tr("Fax Summary"))
        self.textLabel7.setText(self.__tr("Fax Number:"))
        self.textLabel6.setText(self.__tr("Fax Name:"))
        self.textLabel8.setText(self.__tr("Name/Company:"))
        self.textLabel8_2.setText(self.__tr("Location:"))
        self.textLabel8_3.setText(self.__tr("Description:"))
        self.groupBox3.setTitle(self.__tr("Printer Summary"))
        self.textLabel4.setText(self.__tr("Description:"))
        self.textLabel3_2.setText(self.__tr("Location:"))
        self.textLabel2_3.setText(self.__tr("Printer Name:"))
        self.textLabel5.setText(self.__tr("PPD File:"))
        self.textLabel2_5.setText(self.__tr("The printer has been successfully installed on your system."))
        self.setTitle(self.FinishedPage,self.__tr("Finished Adding Printer"))


    def connectionTypeButtonGroup_clicked(self,a0):
        print "SetupForm_base.connectionTypeButtonGroup_clicked(int): Not implemented yet"

    def probedDevicesListView_currentChanged(self,a0):
        print "SetupForm_base.probedDevicesListView_currentChanged(QListViewItem*): Not implemented yet"

    def printerNameLineEdit_textChanged(self,a0):
        print "SetupForm_base.printerNameLineEdit_textChanged(const QString&): Not implemented yet"

    def defaultPrinterNamePushButton_clicked(self):
        print "SetupForm_base.defaultPrinterNamePushButton_clicked(): Not implemented yet"

    def ppdBrowsePushButton_clicked(self):
        print "SetupForm_base.ppdBrowsePushButton_clicked(): Not implemented yet"

    def ppdFileLineEdit_textChanged(self,a0):
        print "SetupForm_base.ppdFileLineEdit_textChanged(const QString&): Not implemented yet"

    def ppdListView_currentChanged(self,a0):
        print "SetupForm_base.ppdListView_currentChanged(QListViewItem*): Not implemented yet"

    def probeUpdatePushButton_clicked(self):
        print "SetupForm_base.probeUpdatePushButton_clicked(): Not implemented yet"

    def searchFiltersPushButton_clicked(self):
        print "SetupForm_base.searchFiltersPushButton_clicked(): Not implemented yet"

    def searchFiltersPushButton2_clicked(self):
        print "SetupForm_base.searchFiltersPushButton2_clicked(): Not implemented yet"

    def manualFindPushButton_clicked(self):
        print "SetupForm_base.manualFindPushButton_clicked(): Not implemented yet"

    def printerLocationLineEdit_textChanged(self,a0):
        print "SetupForm_base.printerLocationLineEdit_textChanged(const QString&): Not implemented yet"

    def printerDescriptionLineEdit_textChanged(self,a0):
        print "SetupForm_base.printerDescriptionLineEdit_textChanged(const QString&): Not implemented yet"

    def faxNameLineEdit_textChanged(self,a0):
        print "SetupForm_base.faxNameLineEdit_textChanged(const QString&): Not implemented yet"

    def faxNumberLineEdit_textChanged(self,a0):
        print "SetupForm_base.faxNumberLineEdit_textChanged(const QString&): Not implemented yet"

    def faxNameCoLineEdit_textChanged(self,a0):
        print "SetupForm_base.faxNameCoLineEdit_textChanged(const QString&): Not implemented yet"

    def printTestPageCheckBox_clicked(self):
        print "SetupForm_base.printTestPageCheckBox_clicked(): Not implemented yet"

    def faxCheckBox_clicked(self):
        print "SetupForm_base.faxCheckBox_clicked(): Not implemented yet"

    def faxCheckBox_toggled(self,a0):
        print "SetupForm_base.faxCheckBox_toggled(bool): Not implemented yet"

    def printTestPageCheckBox_toggled(self,a0):
        print "SetupForm_base.printTestPageCheckBox_toggled(bool): Not implemented yet"

    def defaultFaxNamePushButton_clicked(self):
        print "SetupForm_base.defaultFaxNamePushButton_clicked(): Not implemented yet"

    def otherPPDPushButton_clicked(self):
        print "SetupForm_base.otherPPDPushButton_clicked(): Not implemented yet"

    def ppdDefaultsPushButton_clicked(self):
        print "SetupForm_base.ppdDefaultsPushButton_clicked(): Not implemented yet"

    def faxLocationLineEdit_textChanged(self,a0):
        print "SetupForm_base.faxLocationLineEdit_textChanged(const QString&): Not implemented yet"

    def faxDescriptionLineEdit_textChanged(self,a0):
        print "SetupForm_base.faxDescriptionLineEdit_textChanged(const QString&): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SetupForm_base",s,c)
