# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/nodevicesform_base.ui'
#
# Created: Tue Jun 10 13:34:02 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class NoDevicesForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("NoDevicesForm_base")


        NoDevicesForm_baseLayout = QGridLayout(self,1,1,11,6,"NoDevicesForm_baseLayout")

        self.Icon = QLabel(self,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setFrameShape(QLabel.NoFrame)
        self.Icon.setScaledContents(1)

        NoDevicesForm_baseLayout.addWidget(self.Icon,0,0)
        spacer3 = QSpacerItem(20,280,QSizePolicy.Minimum,QSizePolicy.Expanding)
        NoDevicesForm_baseLayout.addItem(spacer3,1,0)
        spacer2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        NoDevicesForm_baseLayout.addItem(spacer2,2,2)

        self.textLabel7 = QLabel(self,"textLabel7")
        self.textLabel7.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        NoDevicesForm_baseLayout.addMultiCellWidget(self.textLabel7,0,1,1,4)
        spacer43 = QSpacerItem(400,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        NoDevicesForm_baseLayout.addMultiCell(spacer43,3,3,0,1)

        self.setupPushButton = QPushButton(self,"setupPushButton")

        NoDevicesForm_baseLayout.addWidget(self.setupPushButton,3,2)

        self.CUPSButton = QPushButton(self,"CUPSButton")

        NoDevicesForm_baseLayout.addWidget(self.CUPSButton,3,3)

        self.ExitButton = QPushButton(self,"ExitButton")
        self.ExitButton.setDefault(1)

        NoDevicesForm_baseLayout.addWidget(self.ExitButton,3,4)

        self.languageChange()

        self.resize(QSize(525,440).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CUPSButton,SIGNAL("clicked()"),self.CUPSButton_clicked)
        self.connect(self.ExitButton,SIGNAL("clicked()"),self.ExitButton_clicked)
        self.connect(self.setupPushButton,SIGNAL("clicked()"),self.setupPushButton_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - No Installed HP Devices Found"))
        self.textLabel7.setText(self.__tr("<b><font size=\"+2\">No Installed HP Devices Found.</font></b><p>To install a device, use one of the following methods:<p>\n"
"1.Run <b>hp-setup</b> (in a shell/terminal or click <tt>Setup Device...</tt> below).<p>\n"
"2. <b>CUPS web interface</b> (open a browser to: <u>http://localhost:631</u> or press the button below),<p>\n"
"3. The <b>printer installation utility</b> that came with your operating system (YaST, PrinterDrake, etc).\n"
"<p><p>After setting up a printer, you may have to press <tt>F6</tt> or choose <tt>Device | Refresh All</tt> for the printer to appear in the HP Device Manager.<p>\n"
"<i><b>Note: Only devices installed with the <tt>hp:</tt> or <tt>hpfax:</tt> CUPS backend will appear in the HP Device Manager.</b></i><p>"))
        self.setupPushButton.setText(self.__tr("Setup Device..."))
        self.CUPSButton.setText(self.__tr("CUPS Web Interface"))
        self.ExitButton.setText(self.__tr("Close"))


    def CUPSButton_clicked(self):
        print "NoDevicesForm_base.CUPSButton_clicked(): Not implemented yet"

    def ExitButton_clicked(self):
        print "NoDevicesForm_base.ExitButton_clicked(): Not implemented yet"

    def setupPushButton_clicked(self):
        print "NoDevicesForm_base.setupPushButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("NoDevicesForm_base",s,c)
