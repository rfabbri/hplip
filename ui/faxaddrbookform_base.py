# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'faxaddrbookform_base.ui'
#
# Created: Thu Feb 7 16:26:14 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class FaxAddrBookForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FaxAddrBookForm_base")


        FaxAddrBookForm_baseLayout = QGridLayout(self,1,1,11,6,"FaxAddrBookForm_baseLayout")

        self.OKButton = QPushButton(self,"OKButton")

        FaxAddrBookForm_baseLayout.addWidget(self.OKButton,2,8)

        self.newButton = QPushButton(self,"newButton")

        FaxAddrBookForm_baseLayout.addWidget(self.newButton,2,0)

        self.editButton = QPushButton(self,"editButton")

        FaxAddrBookForm_baseLayout.addWidget(self.editButton,2,1)

        self.deleteButton = QPushButton(self,"deleteButton")

        FaxAddrBookForm_baseLayout.addWidget(self.deleteButton,2,2)

        self.addressListView = QListView(self,"addressListView")
        self.addressListView.addColumn(self.__tr("Nickname"))
        self.addressListView.addColumn(self.__tr("Title"))
        self.addressListView.addColumn(self.__tr("First Name"))
        self.addressListView.addColumn(self.__tr("Last Name"))
        self.addressListView.addColumn(self.__tr("Fax Number"))
        self.addressListView.addColumn(self.__tr("Member of Group(s)"))
        self.addressListView.addColumn(self.__tr("Notes/Other Information"))
        self.addressListView.setMidLineWidth(0)
        self.addressListView.setSelectionMode(QListView.Single)
        self.addressListView.setAllColumnsShowFocus(1)
        self.addressListView.setShowSortIndicator(0)

        FaxAddrBookForm_baseLayout.addMultiCellWidget(self.addressListView,1,1,0,8)

        self.textLabel11 = QLabel(self,"textLabel11")

        FaxAddrBookForm_baseLayout.addMultiCellWidget(self.textLabel11,0,0,0,2)

        self.groupButton = QPushButton(self,"groupButton")

        FaxAddrBookForm_baseLayout.addWidget(self.groupButton,2,4)

        self.line8 = QFrame(self,"line8")
        self.line8.setFrameShape(QFrame.VLine)
        self.line8.setFrameShadow(QFrame.Sunken)
        self.line8.setFrameShape(QFrame.VLine)

        FaxAddrBookForm_baseLayout.addWidget(self.line8,2,3)

        self.line8_2 = QFrame(self,"line8_2")
        self.line8_2.setFrameShape(QFrame.VLine)
        self.line8_2.setFrameShadow(QFrame.Sunken)
        self.line8_2.setFrameShape(QFrame.VLine)

        FaxAddrBookForm_baseLayout.addWidget(self.line8_2,2,5)

        self.importPushButton = QPushButton(self,"importPushButton")

        FaxAddrBookForm_baseLayout.addWidget(self.importPushButton,2,6)
        spacer29 = QSpacerItem(300,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FaxAddrBookForm_baseLayout.addItem(spacer29,2,7)

        self.languageChange()

        self.resize(QSize(861,358).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.OKButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.newButton,SIGNAL("clicked()"),self.newButton_clicked)
        self.connect(self.editButton,SIGNAL("clicked()"),self.editButton_clicked)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteButton_clicked)
        self.connect(self.addressListView,SIGNAL("rightButtonClicked(QListViewItem*,const QPoint&,int)"),self.addressListView_rightButtonClicked)
        self.connect(self.addressListView,SIGNAL("currentChanged(QListViewItem*)"),self.addressListView_currentChanged)
        self.connect(self.addressListView,SIGNAL("doubleClicked(QListViewItem*)"),self.addressListView_doubleClicked)
        self.connect(self.groupButton,SIGNAL("clicked()"),self.groupButton_clicked)
        self.connect(self.importPushButton,SIGNAL("clicked()"),self.importPushButton_clicked)

        self.setTabOrder(self.addressListView,self.newButton)
        self.setTabOrder(self.newButton,self.editButton)
        self.setTabOrder(self.editButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.groupButton)
        self.setTabOrder(self.groupButton,self.OKButton)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Fax Address Book"))
        self.OKButton.setText(self.__tr("OK"))
        self.newButton.setText(self.__tr("New..."))
        self.editButton.setText(self.__tr("Edit..."))
        self.deleteButton.setText(self.__tr("Delete..."))
        self.addressListView.header().setLabel(0,self.__tr("Nickname"))
        self.addressListView.header().setLabel(1,self.__tr("Title"))
        self.addressListView.header().setLabel(2,self.__tr("First Name"))
        self.addressListView.header().setLabel(3,self.__tr("Last Name"))
        self.addressListView.header().setLabel(4,self.__tr("Fax Number"))
        self.addressListView.header().setLabel(5,self.__tr("Member of Group(s)"))
        self.addressListView.header().setLabel(6,self.__tr("Notes/Other Information"))
        self.textLabel11.setText(self.__tr("<b>Fax Addresses:</b>"))
        self.groupButton.setText(self.__tr("Groups..."))
        self.importPushButton.setText(self.__tr("Import..."))


    def newButton_clicked(self):
        print "FaxAddrBookForm_base.newButton_clicked(): Not implemented yet"

    def editButton_clicked(self):
        print "FaxAddrBookForm_base.editButton_clicked(): Not implemented yet"

    def deleteButton_clicked(self):
        print "FaxAddrBookForm_base.deleteButton_clicked(): Not implemented yet"

    def addressListView_rightButtonClicked(self,a0,a1,a2):
        print "FaxAddrBookForm_base.addressListView_rightButtonClicked(QListViewItem*,const QPoint&,int): Not implemented yet"

    def addressListView_currentChanged(self,a0):
        print "FaxAddrBookForm_base.addressListView_currentChanged(QListViewItem*): Not implemented yet"

    def addressListView_doubleClicked(self,a0):
        print "FaxAddrBookForm_base.addressListView_doubleClicked(QListViewItem*): Not implemented yet"

    def groupButton_clicked(self):
        print "FaxAddrBookForm_base.groupButton_clicked(): Not implemented yet"

    def importPushButton_clicked(self):
        print "FaxAddrBookForm_base.importPushButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookForm_base",s,c)
