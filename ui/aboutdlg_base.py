# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/aboutdlg_base.ui'
#
# Created: Mon Oct 15 16:07:30 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class AboutDlg_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AboutDlg_base")


        AboutDlg_baseLayout = QGridLayout(self,1,1,11,6,"AboutDlg_baseLayout")

        self.textLabel1 = QLabel(self,"textLabel1")

        AboutDlg_baseLayout.addWidget(self.textLabel1,0,0)

        layout17 = QHBoxLayout(None,0,6,"layout17")
        spacer27 = QSpacerItem(150,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout17.addItem(spacer27)

        self.logoPixmap = QLabel(self,"logoPixmap")
        self.logoPixmap.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.logoPixmap.sizePolicy().hasHeightForWidth()))
        self.logoPixmap.setMinimumSize(QSize(100,110))
        self.logoPixmap.setMaximumSize(QSize(100,110))
        self.logoPixmap.setScaledContents(1)
        layout17.addWidget(self.logoPixmap)
        spacer28 = QSpacerItem(151,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout17.addItem(spacer28)

        AboutDlg_baseLayout.addLayout(layout17,1,0)

        self.pushButton15 = QPushButton(self,"pushButton15")

        AboutDlg_baseLayout.addWidget(self.pushButton15,8,0)

        layout1 = QHBoxLayout(None,0,6,"layout1")

        self.textLabel4 = QLabel(self,"textLabel4")
        layout1.addWidget(self.textLabel4)

        self.VersionText = QLabel(self,"VersionText")
        layout1.addWidget(self.VersionText)

        AboutDlg_baseLayout.addLayout(layout1,2,0)

        layout1_2 = QHBoxLayout(None,0,6,"layout1_2")

        self.textLabel4_2 = QLabel(self,"textLabel4_2")
        layout1_2.addWidget(self.textLabel4_2)

        self.ToolboxVersionText = QLabel(self,"ToolboxVersionText")
        layout1_2.addWidget(self.ToolboxVersionText)

        AboutDlg_baseLayout.addLayout(layout1_2,3,0)

        self.textLabel2 = QLabel(self,"textLabel2")

        AboutDlg_baseLayout.addWidget(self.textLabel2,5,0)

        self.textLabel3 = QLabel(self,"textLabel3")

        AboutDlg_baseLayout.addWidget(self.textLabel3,4,0)

        layout18 = QHBoxLayout(None,0,6,"layout18")

        self.pyPixmap = QLabel(self,"pyPixmap")
        self.pyPixmap.setMinimumSize(QSize(200,62))
        self.pyPixmap.setMaximumSize(QSize(200,62))
        self.pyPixmap.setScaledContents(1)
        layout18.addWidget(self.pyPixmap)

        self.osiPixmap = QLabel(self,"osiPixmap")
        self.osiPixmap.setMinimumSize(QSize(75,65))
        self.osiPixmap.setMaximumSize(QSize(75,65))
        self.osiPixmap.setScaledContents(1)
        layout18.addWidget(self.osiPixmap)

        AboutDlg_baseLayout.addLayout(layout18,6,0)
        spacer29 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        AboutDlg_baseLayout.addItem(spacer29,7,0)

        self.languageChange()

        self.resize(QSize(481,560).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton15,SIGNAL("clicked()"),self.close)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - About"))
        self.textLabel1.setText(self.__tr("<font size=\"+3\"><p align=\"center\">HP Linux Imaging and Printing (HPLIP)</p></font>"))
        self.pushButton15.setText(self.__tr("Close"))
        self.textLabel4.setText(self.__tr("<b>HPLIP Software Version:</b>"))
        self.VersionText.setText(self.__tr("0.0.0"))
        self.textLabel4_2.setText(self.__tr("<b>Device Manager Software Version:</b>"))
        self.ToolboxVersionText.setText(self.__tr("0.0.0"))
        self.textLabel2.setText(self.__tr("<b>Authors and Contributors:</b>\nDavid Suffield, Don Welch, Shiyun Yie, Raghothama Cauligi, John Oleinik, Cory Meisch, Foster Nuffer, Pete Parks, Jacqueline Pitter, David Paschal,\nSteve DeRoos, Mark Overton, Aaron Albright, Smith Kennedy, John Hosszu, Chris Wiesner, Henrique M. Holschuh, Till Kamppeter, Linus Araque, Mark Crawford, Charlie Moore, Naga Samrat Choudary, Suma Byrappa, Parul Singh, Srikant Lokare, Sanjay Kumar, Sarbeswar Meher, Goutam Kodu, Gaurav Sood, Raghavendra Chitpadi, Amarnath Chitumalla"))
        self.textLabel3.setText(self.__tr("<b>License and Copyright:</b>\n(c) Copyright 2007 Hewlett-Packard Development Company, L.P. This software is licensed under the GNU General Public License (GPL), BSD, and MIT licenses. See the software sources for details."))


    def __tr(self,s,c = None):
        return qApp.translate("AboutDlg_base",s,c)
