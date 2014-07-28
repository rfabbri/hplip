# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'faxsettingsform_base.ui'
#
# Created: Mon Dec 12 16:15:55 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class FaxSettingsForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FaxSettingsForm_base")


        FaxSettingsForm_baseLayout = QGridLayout(self,1,1,11,6,"FaxSettingsForm_baseLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.groupBox1 = QGroupBox(self.tab,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")

        groupBox1Layout.addWidget(self.textLabel2,2,0)

        self.faxEdit = QLineEdit(self.groupBox1,"faxEdit")

        groupBox1Layout.addWidget(self.faxEdit,2,1)

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")

        groupBox1Layout.addWidget(self.textLabel1,1,0)

        self.nameEdit = QLineEdit(self.groupBox1,"nameEdit")

        groupBox1Layout.addWidget(self.nameEdit,1,1)

        self.textLabel3 = QLabel(self.groupBox1,"textLabel3")
        self.textLabel3.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        groupBox1Layout.addMultiCellWidget(self.textLabel3,0,0,0,1)

        tabLayout.addWidget(self.groupBox1,0,0)
        spacer10 = QSpacerItem(20,60,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer10,2,0)

        self.groupBox4 = QGroupBox(self.tab,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.emailEdit = QLineEdit(self.groupBox4,"emailEdit")

        groupBox4Layout.addWidget(self.emailEdit,2,1)

        self.textLabel1_2 = QLabel(self.groupBox4,"textLabel1_2")

        groupBox4Layout.addWidget(self.textLabel1_2,1,0)

        self.voiceEdit = QLineEdit(self.groupBox4,"voiceEdit")

        groupBox4Layout.addWidget(self.voiceEdit,1,1)

        self.textLabel2_2 = QLabel(self.groupBox4,"textLabel2_2")

        groupBox4Layout.addWidget(self.textLabel2_2,2,0)

        self.textLabel3_2 = QLabel(self.groupBox4,"textLabel3_2")
        self.textLabel3_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        groupBox4Layout.addMultiCellWidget(self.textLabel3_2,0,0,0,1)

        tabLayout.addWidget(self.groupBox4,1,0)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        FaxSettingsForm_baseLayout.addMultiCellWidget(self.tabWidget2,2,2,0,3)

        self.textLabel3_2_2 = QLabel(self,"textLabel3_2_2")

        FaxSettingsForm_baseLayout.addMultiCellWidget(self.textLabel3_2_2,0,0,0,3)

        self.line1_2_2 = QFrame(self,"line1_2_2")
        self.line1_2_2.setFrameShape(QFrame.HLine)
        self.line1_2_2.setFrameShadow(QFrame.Sunken)
        self.line1_2_2.setFrameShape(QFrame.HLine)

        FaxSettingsForm_baseLayout.addMultiCellWidget(self.line1_2_2,1,1,0,3)

        self.pushButton31 = QPushButton(self,"pushButton31")

        FaxSettingsForm_baseLayout.addWidget(self.pushButton31,3,2)

        self.pushButtonOK = QPushButton(self,"pushButtonOK")
        self.pushButtonOK.setEnabled(0)

        FaxSettingsForm_baseLayout.addWidget(self.pushButtonOK,3,3)
        spacer40 = QSpacerItem(386,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FaxSettingsForm_baseLayout.addItem(spacer40,3,1)

        self.languageChange()

        self.resize(QSize(600,388).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton31,SIGNAL("clicked()"),self.reject)
        self.connect(self.pushButtonOK,SIGNAL("clicked()"),self.accept)
        self.connect(self.faxEdit,SIGNAL("textChanged(const QString&)"),self.faxEdit_textChanged)
        self.connect(self.nameEdit,SIGNAL("textChanged(const QString&)"),self.nameEdit_textChanged)

        self.setTabOrder(self.nameEdit,self.faxEdit)
        self.setTabOrder(self.faxEdit,self.voiceEdit)
        self.setTabOrder(self.voiceEdit,self.emailEdit)
        self.setTabOrder(self.emailEdit,self.pushButton31)
        self.setTabOrder(self.pushButton31,self.pushButtonOK)
        self.setTabOrder(self.pushButtonOK,self.tabWidget2)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Fax Settings"))
        self.groupBox1.setTitle(self.__tr("Fax Header Information"))
        self.textLabel2.setText(self.__tr("Device Fax Number:"))
        self.textLabel1.setText(self.__tr("Name and/or Company:"))
        self.textLabel3.setText(self.__tr("<i>This information will appear at the top of each fax that you send.</i>"))
        self.groupBox4.setTitle(self.__tr("Coverpage Information"))
        self.textLabel1_2.setText(self.__tr("Voice phone number:"))
        self.textLabel2_2.setText(self.__tr("Email address:"))
        self.textLabel3_2.setText(self.__tr("<i>This information will appear on any coverpage that you send.</i>"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Information"))
        self.textLabel3_2_2.setText(self.__tr("<b>Configure device settings for sending faxes.</b>"))
        self.pushButton31.setText(self.__tr("Cancel"))
        self.pushButtonOK.setText(self.__tr("OK"))


    def faxEdit_textChanged(self,a0):
        print "FaxSettingsForm_base.faxEdit_textChanged(const QString&): Not implemented yet"

    def nameEdit_textChanged(self,a0):
        print "FaxSettingsForm_base.nameEdit_textChanged(const QString&): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FaxSettingsForm_base",s,c)
