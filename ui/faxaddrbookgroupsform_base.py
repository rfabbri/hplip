# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/faxaddrbookgroupsform_base.ui'
#
# Created: Mon May 9 13:35:56 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class FaxAddrBookGroupsForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FaxAddrBookGroupsForm_base")


        FaxAddrBookGroupsForm_baseLayout = QGridLayout(self,1,1,11,6,"FaxAddrBookGroupsForm_baseLayout")

        self.groupListView = QListView(self,"groupListView")
        self.groupListView.addColumn(self.__tr("Group Name"))
        self.groupListView.addColumn(self.__tr("Group Members"))
        self.groupListView.setAllColumnsShowFocus(1)

        FaxAddrBookGroupsForm_baseLayout.addMultiCellWidget(self.groupListView,1,1,0,4)

        self.newButton = QPushButton(self,"newButton")

        FaxAddrBookGroupsForm_baseLayout.addWidget(self.newButton,2,0)

        self.deleteButton = QPushButton(self,"deleteButton")

        FaxAddrBookGroupsForm_baseLayout.addWidget(self.deleteButton,2,2)

        self.editButton = QPushButton(self,"editButton")

        FaxAddrBookGroupsForm_baseLayout.addWidget(self.editButton,2,1)
        spacer35 = QSpacerItem(120,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FaxAddrBookGroupsForm_baseLayout.addItem(spacer35,2,3)

        self.pushButton42 = QPushButton(self,"pushButton42")

        FaxAddrBookGroupsForm_baseLayout.addWidget(self.pushButton42,2,4)

        self.textLabel10 = QLabel(self,"textLabel10")

        FaxAddrBookGroupsForm_baseLayout.addMultiCellWidget(self.textLabel10,0,0,0,1)

        self.languageChange()

        self.resize(QSize(376,359).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.newButton,SIGNAL("clicked()"),self.newButton_clicked)
        self.connect(self.editButton,SIGNAL("clicked()"),self.editButton_clicked)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteButton_clicked)
        self.connect(self.pushButton42,SIGNAL("clicked()"),self.close)
        self.connect(self.groupListView,SIGNAL("currentChanged(QListViewItem*)"),self.groupListView_currentChanged)
        self.connect(self.groupListView,SIGNAL("doubleClicked(QListViewItem*)"),self.groupListView_doubleClicked)
        self.connect(self.groupListView,SIGNAL("rightButtonClicked(QListViewItem*,const QPoint&,int)"),self.groupListView_rightButtonClicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Fax Address Book Groups"))
        self.groupListView.header().setLabel(0,self.__tr("Group Name"))
        self.groupListView.header().setLabel(1,self.__tr("Group Members"))
        self.newButton.setText(self.__tr("New..."))
        self.deleteButton.setText(self.__tr("Delete..."))
        self.editButton.setText(self.__tr("Edit..."))
        self.pushButton42.setText(self.__tr("OK"))
        self.textLabel10.setText(self.__tr("<b>Groups:</b>"))


    def newButton_clicked(self):
        print "FaxAddrBookGroupsForm_base.newButton_clicked(): Not implemented yet"

    def editButton_clicked(self):
        print "FaxAddrBookGroupsForm_base.editButton_clicked(): Not implemented yet"

    def deleteButton_clicked(self):
        print "FaxAddrBookGroupsForm_base.deleteButton_clicked(): Not implemented yet"

    def groupListView_currentChanged(self,a0):
        print "FaxAddrBookGroupsForm_base.groupListView_currentChanged(QListViewItem*): Not implemented yet"

    def groupListView_doubleClicked(self,a0):
        print "FaxAddrBookGroupsForm_base.groupListView_doubleClicked(QListViewItem*): Not implemented yet"

    def groupListView_rightButtonClicked(self,a0,a1,a2):
        print "FaxAddrBookGroupsForm_base.groupListView_rightButtonClicked(QListViewItem*,const QPoint&,int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookGroupsForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = FaxAddrBookGroupsForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
