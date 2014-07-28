# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settingsdialog_base.ui'
#
# Created: Mon Apr 21 09:46:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SettingsDialog_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SettingsDialog_base")


        SettingsDialog_baseLayout = QGridLayout(self,1,1,11,6,"SettingsDialog_baseLayout")

        self.pushButton30 = QPushButton(self,"pushButton30")

        SettingsDialog_baseLayout.addWidget(self.pushButton30,1,2)

        self.pushButton31 = QPushButton(self,"pushButton31")

        SettingsDialog_baseLayout.addWidget(self.pushButton31,1,1)
        spacer40 = QSpacerItem(430,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SettingsDialog_baseLayout.addItem(spacer40,1,0)

        self.TabWidget = QTabWidget(self,"TabWidget")

        self.CleaningLevels = QWidget(self.TabWidget,"CleaningLevels")
        CleaningLevelsLayout = QGridLayout(self.CleaningLevels,1,1,11,6,"CleaningLevelsLayout")

        self.textLabel3_2_2 = QLabel(self.CleaningLevels,"textLabel3_2_2")

        CleaningLevelsLayout.addWidget(self.textLabel3_2_2,0,0)

        self.line1_2_2 = QFrame(self.CleaningLevels,"line1_2_2")
        self.line1_2_2.setFrameShape(QFrame.HLine)
        self.line1_2_2.setFrameShadow(QFrame.Sunken)
        self.line1_2_2.setFrameShape(QFrame.HLine)

        CleaningLevelsLayout.addWidget(self.line1_2_2,1,0)
        spacer8 = QSpacerItem(20,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        CleaningLevelsLayout.addItem(spacer8,5,0)

        self.autoRefreshCheckBox = QCheckBox(self.CleaningLevels,"autoRefreshCheckBox")

        CleaningLevelsLayout.addWidget(self.autoRefreshCheckBox,2,0)

        self.CleaningLevel = QButtonGroup(self.CleaningLevels,"CleaningLevel")
        self.CleaningLevel.setColumnLayout(0,Qt.Vertical)
        self.CleaningLevel.layout().setSpacing(6)
        self.CleaningLevel.layout().setMargin(11)
        CleaningLevelLayout = QGridLayout(self.CleaningLevel.layout())
        CleaningLevelLayout.setAlignment(Qt.AlignTop)
        spacer9_2 = QSpacerItem(290,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        CleaningLevelLayout.addItem(spacer9_2,0,2)

        self.textLabel1_4 = QLabel(self.CleaningLevel,"textLabel1_4")

        CleaningLevelLayout.addWidget(self.textLabel1_4,0,0)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.AutoRefreshRate = QSpinBox(self.CleaningLevel,"AutoRefreshRate")
        self.AutoRefreshRate.setEnabled(0)
        self.AutoRefreshRate.setWrapping(1)
        self.AutoRefreshRate.setButtonSymbols(QSpinBox.PlusMinus)
        self.AutoRefreshRate.setMaxValue(60)
        self.AutoRefreshRate.setMinValue(5)
        self.AutoRefreshRate.setValue(6)
        layout7.addWidget(self.AutoRefreshRate)

        self.textLabel1_3 = QLabel(self.CleaningLevel,"textLabel1_3")
        layout7.addWidget(self.textLabel1_3)

        CleaningLevelLayout.addLayout(layout7,0,1)

        CleaningLevelsLayout.addWidget(self.CleaningLevel,3,0)

        self.refreshScopeButtonGroup = QButtonGroup(self.CleaningLevels,"refreshScopeButtonGroup")
        self.refreshScopeButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.refreshScopeButtonGroup.layout().setSpacing(6)
        self.refreshScopeButtonGroup.layout().setMargin(11)
        refreshScopeButtonGroupLayout = QGridLayout(self.refreshScopeButtonGroup.layout())
        refreshScopeButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.radioButton1 = QRadioButton(self.refreshScopeButtonGroup,"radioButton1")
        self.radioButton1.setEnabled(0)
        self.radioButton1.setChecked(1)

        refreshScopeButtonGroupLayout.addWidget(self.radioButton1,0,0)

        self.radioButton2 = QRadioButton(self.refreshScopeButtonGroup,"radioButton2")
        self.radioButton2.setEnabled(0)

        refreshScopeButtonGroupLayout.addWidget(self.radioButton2,1,0)

        CleaningLevelsLayout.addWidget(self.refreshScopeButtonGroup,4,0)
        self.TabWidget.insertTab(self.CleaningLevels,QString.fromLatin1(""))

        self.FunctionCommands = QWidget(self.TabWidget,"FunctionCommands")
        FunctionCommandsLayout = QGridLayout(self.FunctionCommands,1,1,11,6,"FunctionCommandsLayout")

        self.line1_2_2_3 = QFrame(self.FunctionCommands,"line1_2_2_3")
        self.line1_2_2_3.setFrameShape(QFrame.HLine)
        self.line1_2_2_3.setFrameShadow(QFrame.Sunken)
        self.line1_2_2_3.setFrameShape(QFrame.HLine)

        FunctionCommandsLayout.addMultiCellWidget(self.line1_2_2_3,1,1,0,1)

        self.textLabel3_2_2_2 = QLabel(self.FunctionCommands,"textLabel3_2_2_2")

        FunctionCommandsLayout.addMultiCellWidget(self.textLabel3_2_2_2,0,0,0,1)

        self.DefaultsButton = QPushButton(self.FunctionCommands,"DefaultsButton")
        self.DefaultsButton.setEnabled(1)

        FunctionCommandsLayout.addWidget(self.DefaultsButton,4,0)
        spacer8_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FunctionCommandsLayout.addItem(spacer8_2,4,1)

        self.groupBox3 = QGroupBox(self.FunctionCommands,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.textLabel1_2 = QLabel(self.groupBox3,"textLabel1_2")

        groupBox3Layout.addWidget(self.textLabel1_2,0,0)

        self.PrintCommand = QLineEdit(self.groupBox3,"PrintCommand")
        self.PrintCommand.setEnabled(1)

        groupBox3Layout.addWidget(self.PrintCommand,1,0)

        self.textLabel2_2 = QLabel(self.groupBox3,"textLabel2_2")

        groupBox3Layout.addWidget(self.textLabel2_2,2,0)

        self.textLabel3_3 = QLabel(self.groupBox3,"textLabel3_3")

        groupBox3Layout.addWidget(self.textLabel3_3,4,0)

        self.textLabel4 = QLabel(self.groupBox3,"textLabel4")

        groupBox3Layout.addWidget(self.textLabel4,6,0)

        self.ScanCommand = QLineEdit(self.groupBox3,"ScanCommand")

        groupBox3Layout.addWidget(self.ScanCommand,3,0)

        self.SendFaxCommand = QLineEdit(self.groupBox3,"SendFaxCommand")
        self.SendFaxCommand.setEnabled(1)

        groupBox3Layout.addWidget(self.SendFaxCommand,5,0)

        self.AccessPCardCommand = QLineEdit(self.groupBox3,"AccessPCardCommand")
        self.AccessPCardCommand.setEnabled(1)

        groupBox3Layout.addWidget(self.AccessPCardCommand,7,0)

        self.textLabel5 = QLabel(self.groupBox3,"textLabel5")

        groupBox3Layout.addWidget(self.textLabel5,8,0)

        self.MakeCopiesCommand = QLineEdit(self.groupBox3,"MakeCopiesCommand")
        self.MakeCopiesCommand.setEnabled(1)

        groupBox3Layout.addWidget(self.MakeCopiesCommand,9,0)

        FunctionCommandsLayout.addMultiCellWidget(self.groupBox3,2,2,0,1)
        spacer49 = QSpacerItem(20,60,QSizePolicy.Minimum,QSizePolicy.Expanding)
        FunctionCommandsLayout.addItem(spacer49,3,0)
        self.TabWidget.insertTab(self.FunctionCommands,QString.fromLatin1(""))

        SettingsDialog_baseLayout.addMultiCellWidget(self.TabWidget,0,0,0,2)

        self.languageChange()

        self.resize(QSize(460,565).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton31,SIGNAL("clicked()"),self.reject)
        self.connect(self.pushButton30,SIGNAL("clicked()"),self.accept)
        self.connect(self.CleaningLevel,SIGNAL("clicked(int)"),self.CleaningLevel_clicked)
        self.connect(self.DefaultsButton,SIGNAL("clicked()"),self.DefaultsButton_clicked)
        self.connect(self.TabWidget,SIGNAL("currentChanged(QWidget*)"),self.TabWidget_currentChanged)
        self.connect(self.autoRefreshCheckBox,SIGNAL("clicked()"),self.autoRefreshCheckBox_clicked)
        self.connect(self.autoRefreshCheckBox,SIGNAL("toggled(bool)"),self.AutoRefreshRate.setEnabled)
        self.connect(self.autoRefreshCheckBox,SIGNAL("toggled(bool)"),self.radioButton1.setEnabled)
        self.connect(self.autoRefreshCheckBox,SIGNAL("toggled(bool)"),self.radioButton2.setEnabled)
        self.connect(self.refreshScopeButtonGroup,SIGNAL("clicked(int)"),self.refreshScopeButtonGroup_clicked)

        self.setTabOrder(self.TabWidget,self.pushButton30)
        self.setTabOrder(self.pushButton30,self.pushButton31)
        self.setTabOrder(self.pushButton31,self.PrintCommand)
        self.setTabOrder(self.PrintCommand,self.ScanCommand)
        self.setTabOrder(self.ScanCommand,self.AccessPCardCommand)
        self.setTabOrder(self.AccessPCardCommand,self.SendFaxCommand)
        self.setTabOrder(self.SendFaxCommand,self.MakeCopiesCommand)
        self.setTabOrder(self.MakeCopiesCommand,self.DefaultsButton)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Settings"))
        self.pushButton30.setText(self.__tr("OK"))
        self.pushButton31.setText(self.__tr("Cancel"))
        self.textLabel3_2_2.setText(self.__tr("<b>Configure if and when device(s) are automatically refreshed</b>"))
        self.autoRefreshCheckBox.setText(self.__tr("Enable device auto refresh"))
        self.CleaningLevel.setTitle(self.__tr("Auto Interval"))
        self.textLabel1_4.setText(self.__tr("Refresh every:"))
        self.textLabel1_3.setText(self.__tr("seconds"))
        self.refreshScopeButtonGroup.setTitle(self.__tr("Device(s) to Refresh "))
        self.radioButton1.setText(self.__tr("Only currently selected device"))
        self.radioButton2.setText(self.__tr("All devices"))
        self.TabWidget.changeTab(self.CleaningLevels,self.__tr("Auto Refresh"))
        self.textLabel3_2_2_2.setText(self.__tr("<b>Configure what commands to run for device functions</b>"))
        self.DefaultsButton.setText(self.__tr("Set Defaults"))
        self.groupBox3.setTitle(self.__tr("Commands"))
        self.textLabel1_2.setText(self.__tr("Print:"))
        self.textLabel2_2.setText(self.__tr("Scan:"))
        self.textLabel3_3.setText(self.__tr("Send PC Fax:"))
        self.textLabel4.setText(self.__tr("Unload Photo Cards:"))
        self.textLabel5.setText(self.__tr("Make Copies:"))
        self.TabWidget.changeTab(self.FunctionCommands,self.__tr("Commands (Advanced)"))


    def PrintCmdChangeButton_clicked(self):
        print "SettingsDialog_base.PrintCmdChangeButton_clicked(): Not implemented yet"

    def ScanCmdChangeButton_clicked(self):
        print "SettingsDialog_base.ScanCmdChangeButton_clicked(): Not implemented yet"

    def AccessPCardCmdChangeButton_clicked(self):
        print "SettingsDialog_base.AccessPCardCmdChangeButton_clicked(): Not implemented yet"

    def SendFaxCmdChangeButton_clicked(self):
        print "SettingsDialog_base.SendFaxCmdChangeButton_clicked(): Not implemented yet"

    def MakeCopiesCmdChangeButton_clicked(self):
        print "SettingsDialog_base.MakeCopiesCmdChangeButton_clicked(): Not implemented yet"

    def CleaningLevel_clicked(self,a0):
        print "SettingsDialog_base.CleaningLevel_clicked(int): Not implemented yet"

    def pushButton5_clicked(self):
        print "SettingsDialog_base.pushButton5_clicked(): Not implemented yet"

    def DefaultsButton_clicked(self):
        print "SettingsDialog_base.DefaultsButton_clicked(): Not implemented yet"

    def TabWidget_currentChanged(self,a0):
        print "SettingsDialog_base.TabWidget_currentChanged(QWidget*): Not implemented yet"

    def pushButton6_clicked(self):
        print "SettingsDialog_base.pushButton6_clicked(): Not implemented yet"

    def EmailTestButton_clicked(self):
        print "SettingsDialog_base.EmailTestButton_clicked(): Not implemented yet"

    def autoRefreshCheckBox_clicked(self):
        print "SettingsDialog_base.autoRefreshCheckBox_clicked(): Not implemented yet"

    def refreshScopeButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.refreshScopeButtonGroup_clicked(int): Not implemented yet"

    def printButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.printButtonGroup_clicked(int): Not implemented yet"

    def scanButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.scanButtonGroup_clicked(int): Not implemented yet"

    def faxButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.faxButtonGroup_clicked(int): Not implemented yet"

    def pcardButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.pcardButtonGroup_clicked(int): Not implemented yet"

    def copyButtonGroup_clicked(self,a0):
        print "SettingsDialog_base.copyButtonGroup_clicked(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SettingsDialog_base",s,c)
