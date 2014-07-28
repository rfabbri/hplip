# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/setupsettings_base.ui'
#
# Created: Wed Sep 27 09:51:56 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SetupSettings_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SetupSettings_base")


        SetupSettings_baseLayout = QGridLayout(self,1,1,11,6,"SetupSettings_baseLayout")

        self.filterButtonGroup = QButtonGroup(self,"filterButtonGroup")
        self.filterButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.filterButtonGroup.layout().setSpacing(6)
        self.filterButtonGroup.layout().setMargin(11)
        filterButtonGroupLayout = QGridLayout(self.filterButtonGroup.layout())
        filterButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.allRadioButton = QRadioButton(self.filterButtonGroup,"allRadioButton")
        self.allRadioButton.setChecked(1)

        filterButtonGroupLayout.addMultiCellWidget(self.allRadioButton,0,0,0,1)

        self.filterRadioButton = QRadioButton(self.filterButtonGroup,"filterRadioButton")

        filterButtonGroupLayout.addMultiCellWidget(self.filterRadioButton,1,1,0,2)

        layout8 = QGridLayout(None,1,1,8,6,"layout8")

        self.copyCheckBox = QCheckBox(self.filterButtonGroup,"copyCheckBox")
        self.copyCheckBox.setEnabled(0)

        layout8.addWidget(self.copyCheckBox,3,0)

        self.pcardCheckBox = QCheckBox(self.filterButtonGroup,"pcardCheckBox")
        self.pcardCheckBox.setEnabled(0)

        layout8.addWidget(self.pcardCheckBox,2,0)

        self.scanCheckBox = QCheckBox(self.filterButtonGroup,"scanCheckBox")
        self.scanCheckBox.setEnabled(0)

        layout8.addWidget(self.scanCheckBox,1,0)

        self.faxCheckBox = QCheckBox(self.filterButtonGroup,"faxCheckBox")
        self.faxCheckBox.setEnabled(0)

        layout8.addWidget(self.faxCheckBox,0,0)

        filterButtonGroupLayout.addLayout(layout8,2,1)
        spacer14 = QSpacerItem(301,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        filterButtonGroupLayout.addItem(spacer14,2,2)

        SetupSettings_baseLayout.addMultiCellWidget(self.filterButtonGroup,0,0,0,3)

        self.okPushButton = QPushButton(self,"okPushButton")
        self.okPushButton.setDefault(1)

        SetupSettings_baseLayout.addWidget(self.okPushButton,4,3)

        self.cancelPushButton = QPushButton(self,"cancelPushButton")

        SetupSettings_baseLayout.addWidget(self.cancelPushButton,4,2)

        self.defaultsPushButton = QPushButton(self,"defaultsPushButton")

        SetupSettings_baseLayout.addWidget(self.defaultsPushButton,4,0)
        spacer16 = QSpacerItem(140,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupSettings_baseLayout.addItem(spacer16,4,1)

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.textLabel6 = QLabel(self.groupBox2,"textLabel6")

        groupBox2Layout.addWidget(self.textLabel6,0,0)

        self.searchTermLineEdit = QLineEdit(self.groupBox2,"searchTermLineEdit")
        self.searchTermLineEdit.setMaxLength(255)

        groupBox2Layout.addWidget(self.searchTermLineEdit,0,1)

        SetupSettings_baseLayout.addMultiCellWidget(self.groupBox2,1,1,0,3)

        self.groupBox3 = QGroupBox(self,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        layout10 = QGridLayout(None,1,1,0,6,"layout10")

        self.timeoutSpinBox = QSpinBox(self.groupBox3,"timeoutSpinBox")
        self.timeoutSpinBox.setMaxValue(45)
        self.timeoutSpinBox.setMinValue(1)

        layout10.addWidget(self.timeoutSpinBox,1,1)

        self.textLabel7 = QLabel(self.groupBox3,"textLabel7")

        layout10.addWidget(self.textLabel7,0,0)

        self.textLabel8 = QLabel(self.groupBox3,"textLabel8")

        layout10.addWidget(self.textLabel8,1,0)

        self.ttlSpinBox = QSpinBox(self.groupBox3,"ttlSpinBox")
        self.ttlSpinBox.setMaxValue(255)
        self.ttlSpinBox.setMinValue(1)

        layout10.addWidget(self.ttlSpinBox,0,1)

        groupBox3Layout.addLayout(layout10,0,0)
        spacer15 = QSpacerItem(261,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox3Layout.addItem(spacer15,0,1)

        SetupSettings_baseLayout.addMultiCellWidget(self.groupBox3,2,2,0,3)
        spacer12 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        SetupSettings_baseLayout.addItem(spacer12,3,0)

        self.languageChange()

        self.resize(QSize(473,421).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelPushButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.okPushButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.filterRadioButton,SIGNAL("toggled(bool)"),self.faxCheckBox.setEnabled)
        self.connect(self.filterRadioButton,SIGNAL("toggled(bool)"),self.scanCheckBox.setEnabled)
        self.connect(self.filterRadioButton,SIGNAL("toggled(bool)"),self.pcardCheckBox.setEnabled)
        self.connect(self.filterRadioButton,SIGNAL("toggled(bool)"),self.copyCheckBox.setEnabled)
        self.connect(self.faxCheckBox,SIGNAL("toggled(bool)"),self.faxCheckBox_toggled)
        self.connect(self.scanCheckBox,SIGNAL("toggled(bool)"),self.scanCheckBox_toggled)
        self.connect(self.pcardCheckBox,SIGNAL("toggled(bool)"),self.pcardCheckBox_toggled)
        self.connect(self.copyCheckBox,SIGNAL("toggled(bool)"),self.copyCheckBox_toggled)
        self.connect(self.filterButtonGroup,SIGNAL("clicked(int)"),self.filterButtonGroup_clicked)
        self.connect(self.searchTermLineEdit,SIGNAL("textChanged(const QString&)"),self.searchTermLineEdit_textChanged)
        self.connect(self.ttlSpinBox,SIGNAL("valueChanged(int)"),self.ttlSpinBox_valueChanged)
        self.connect(self.timeoutSpinBox,SIGNAL("valueChanged(int)"),self.timeoutSpinBox_valueChanged)
        self.connect(self.defaultsPushButton,SIGNAL("clicked()"),self.defaultsPushButton_clicked)

        self.setTabOrder(self.allRadioButton,self.faxCheckBox)
        self.setTabOrder(self.faxCheckBox,self.scanCheckBox)
        self.setTabOrder(self.scanCheckBox,self.pcardCheckBox)
        self.setTabOrder(self.pcardCheckBox,self.copyCheckBox)
        self.setTabOrder(self.copyCheckBox,self.searchTermLineEdit)
        self.setTabOrder(self.searchTermLineEdit,self.ttlSpinBox)
        self.setTabOrder(self.ttlSpinBox,self.timeoutSpinBox)
        self.setTabOrder(self.timeoutSpinBox,self.cancelPushButton)
        self.setTabOrder(self.cancelPushButton,self.okPushButton)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Setup Filters, Search and Settings"))
        self.filterButtonGroup.setTitle(self.__tr("Discovery Filter"))
        self.allRadioButton.setText(self.__tr("Discover all devices"))
        self.filterRadioButton.setText(self.__tr("Only discover devices that support the following functionality:"))
        self.copyCheckBox.setText(self.__tr("PC Initiated Copying"))
        self.pcardCheckBox.setText(self.__tr("PC Photocard Access"))
        self.scanCheckBox.setText(self.__tr("Scan to PC"))
        self.faxCheckBox.setText(self.__tr("PC Send Fax"))
        self.okPushButton.setText(self.__tr("OK"))
        self.cancelPushButton.setText(self.__tr("Cancel"))
        self.defaultsPushButton.setText(self.__tr("Defaults"))
        self.groupBox2.setTitle(self.__tr("Discovery Search"))
        self.textLabel6.setText(self.__tr("Search Term:"))
        self.groupBox3.setTitle(self.__tr("Network Discovery Settings"))
        self.textLabel7.setText(self.__tr("TTL:"))
        self.textLabel8.setText(self.__tr("Timeout (secs):"))


    def faxCheckBox_toggled(self,a0):
        print "SetupSettings_base.faxCheckBox_toggled(bool): Not implemented yet"

    def scanCheckBox_toggled(self,a0):
        print "SetupSettings_base.scanCheckBox_toggled(bool): Not implemented yet"

    def pcardCheckBox_toggled(self,a0):
        print "SetupSettings_base.pcardCheckBox_toggled(bool): Not implemented yet"

    def copyCheckBox_toggled(self,a0):
        print "SetupSettings_base.copyCheckBox_toggled(bool): Not implemented yet"

    def filterButtonGroup_clicked(self,a0):
        print "SetupSettings_base.filterButtonGroup_clicked(int): Not implemented yet"

    def searchTermLineEdit_textChanged(self,a0):
        print "SetupSettings_base.searchTermLineEdit_textChanged(const QString&): Not implemented yet"

    def ttlSpinBox_valueChanged(self,a0):
        print "SetupSettings_base.ttlSpinBox_valueChanged(int): Not implemented yet"

    def timeoutSpinBox_valueChanged(self,a0):
        print "SetupSettings_base.timeoutSpinBox_valueChanged(int): Not implemented yet"

    def defaultsPushButton_clicked(self):
        print "SetupSettings_base.defaultsPushButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SetupSettings_base",s,c)
