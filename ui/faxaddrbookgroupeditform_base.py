# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/faxaddrbookgroupeditform_base.ui'
#
# Created: Mon May 9 13:35:55 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class FaxAddrBookGroupEditForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FaxAddrBookGroupEditForm_base")


        FaxAddrBookGroupEditForm_baseLayout = QGridLayout(self,1,1,11,6,"FaxAddrBookGroupEditForm_baseLayout")

        self.textLabel8 = QLabel(self,"textLabel8")

        FaxAddrBookGroupEditForm_baseLayout.addWidget(self.textLabel8,0,0)

        self.textLabel9 = QLabel(self,"textLabel9")

        FaxAddrBookGroupEditForm_baseLayout.addMultiCellWidget(self.textLabel9,2,2,0,3)

        self.entriesListView = QListView(self,"entriesListView")
        self.entriesListView.addColumn(self.__tr("Group Members"))
        self.entriesListView.setSelectionMode(QListView.NoSelection)

        FaxAddrBookGroupEditForm_baseLayout.addMultiCellWidget(self.entriesListView,3,3,0,3)

        self.groupnameEdit = QLineEdit(self,"groupnameEdit")

        FaxAddrBookGroupEditForm_baseLayout.addMultiCellWidget(self.groupnameEdit,0,0,1,3)

        self.line11 = QFrame(self,"line11")
        self.line11.setFrameShape(QFrame.HLine)
        self.line11.setFrameShadow(QFrame.Sunken)
        self.line11.setFrameShape(QFrame.HLine)

        FaxAddrBookGroupEditForm_baseLayout.addMultiCellWidget(self.line11,1,1,0,3)

        self.okButton = QPushButton(self,"okButton")

        FaxAddrBookGroupEditForm_baseLayout.addWidget(self.okButton,4,3)

        self.cancelButton = QPushButton(self,"cancelButton")

        FaxAddrBookGroupEditForm_baseLayout.addWidget(self.cancelButton,4,2)
        spacer36 = QSpacerItem(150,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FaxAddrBookGroupEditForm_baseLayout.addMultiCell(spacer36,4,4,0,1)

        self.languageChange()

        self.resize(QSize(377,359).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.groupnameEdit,SIGNAL("textChanged(const QString&)"),self.groupnameEdit_textChanged)
        self.connect(self.entriesListView,SIGNAL("clicked(QListViewItem*)"),self.entriesListView_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Fax Address Book Group"))
        self.textLabel8.setText(self.__tr("<b>Group Name:</b>"))
        self.textLabel9.setText(self.__tr("<b>Member Address Book Entries:</b>"))
        self.entriesListView.header().setLabel(0,self.__tr("Group Members"))
        self.okButton.setText(self.__tr("OK"))
        self.cancelButton.setText(self.__tr("Cancel"))


    def groupnameEdit_textChanged(self,a0):
        print "FaxAddrBookGroupEditForm_base.groupnameEdit_textChanged(const QString&): Not implemented yet"

    def entriesListView_clicked(self,a0):
        print "FaxAddrBookGroupEditForm_base.entriesListView_clicked(QListViewItem*): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookGroupEditForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = FaxAddrBookGroupEditForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
