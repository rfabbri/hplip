# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/faxaddrbookeditform_base.ui'
#
# Created: Wed Jul 18 16:05:44 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class FaxAddrBookEditForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FaxAddrBookEditForm_base")


        FaxAddrBookEditForm_baseLayout = QGridLayout(self,1,1,11,6,"FaxAddrBookEditForm_baseLayout")

        self.pushButton34 = QPushButton(self,"pushButton34")

        FaxAddrBookEditForm_baseLayout.addWidget(self.pushButton34,8,1)

        self.line5 = QFrame(self,"line5")
        self.line5.setFrameShape(QFrame.HLine)
        self.line5.setFrameShadow(QFrame.Sunken)
        self.line5.setFrameShape(QFrame.HLine)

        FaxAddrBookEditForm_baseLayout.addMultiCellWidget(self.line5,6,6,0,2)

        self.OKButton = QPushButton(self,"OKButton")
        self.OKButton.setEnabled(0)

        FaxAddrBookEditForm_baseLayout.addWidget(self.OKButton,8,2)
        spacer31 = QSpacerItem(401,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        FaxAddrBookEditForm_baseLayout.addItem(spacer31,8,0)

        self.line5_2_2 = QFrame(self,"line5_2_2")
        self.line5_2_2.setFrameShape(QFrame.HLine)
        self.line5_2_2.setFrameShadow(QFrame.Sunken)
        self.line5_2_2.setFrameShape(QFrame.HLine)

        FaxAddrBookEditForm_baseLayout.addMultiCellWidget(self.line5_2_2,9,9,0,2)

        self.line5_2 = QFrame(self,"line5_2")
        self.line5_2.setFrameShape(QFrame.HLine)
        self.line5_2.setFrameShadow(QFrame.Sunken)
        self.line5_2.setFrameShape(QFrame.HLine)

        FaxAddrBookEditForm_baseLayout.addMultiCellWidget(self.line5_2,4,4,0,2)

        layout1 = QHBoxLayout(None,0,6,"layout1")

        self.textLabel7 = QLabel(self,"textLabel7")
        layout1.addWidget(self.textLabel7)

        self.faxEdit = QLineEdit(self,"faxEdit")
        layout1.addWidget(self.faxEdit)

        FaxAddrBookEditForm_baseLayout.addMultiCellLayout(layout1,5,5,0,2)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.textLabel3 = QLabel(self,"textLabel3")
        layout2.addWidget(self.textLabel3)

        self.nicknameEdit = QLineEdit(self,"nicknameEdit")
        layout2.addWidget(self.nicknameEdit)

        FaxAddrBookEditForm_baseLayout.addMultiCellLayout(layout2,0,0,0,2)

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.textLabel4 = QLabel(self,"textLabel4")
        layout6.addWidget(self.textLabel4)

        self.groupListView = QListView(self,"groupListView")
        self.groupListView.addColumn(self.__tr("Group Name"))
        self.groupListView.setSelectionMode(QListView.NoSelection)
        layout6.addWidget(self.groupListView)

        FaxAddrBookEditForm_baseLayout.addMultiCellLayout(layout6,3,3,0,2)

        layout7 = QVBoxLayout(None,0,6,"layout7")

        self.textLabel6 = QLabel(self,"textLabel6")
        layout7.addWidget(self.textLabel6)

        self.notesEdit = QTextEdit(self,"notesEdit")
        layout7.addWidget(self.notesEdit)

        FaxAddrBookEditForm_baseLayout.addMultiCellLayout(layout7,7,7,0,2)

        self.textLabel12 = QLabel(self,"textLabel12")

        FaxAddrBookEditForm_baseLayout.addMultiCellWidget(self.textLabel12,10,10,0,2)

        self.line12 = QFrame(self,"line12")
        self.line12.setFrameShape(QFrame.HLine)
        self.line12.setFrameShadow(QFrame.Sunken)
        self.line12.setFrameShape(QFrame.HLine)

        FaxAddrBookEditForm_baseLayout.addMultiCellWidget(self.line12,1,1,0,2)

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        layout9 = QVBoxLayout(None,0,6,"layout9")

        self.textLabel5 = QLabel(self,"textLabel5")
        layout9.addWidget(self.textLabel5)

        self.textLabel1 = QLabel(self,"textLabel1")
        layout9.addWidget(self.textLabel1)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout9.addWidget(self.textLabel2)

        layout11.addLayout(layout9,0,0)

        layout10 = QVBoxLayout(None,0,6,"layout10")

        self.titleEdit = QLineEdit(self,"titleEdit")
        layout10.addWidget(self.titleEdit)

        self.firstnameEdit = QLineEdit(self,"firstnameEdit")
        layout10.addWidget(self.firstnameEdit)

        self.lastnameEdit = QLineEdit(self,"lastnameEdit")
        layout10.addWidget(self.lastnameEdit)

        layout11.addLayout(layout10,0,1)

        FaxAddrBookEditForm_baseLayout.addMultiCellLayout(layout11,2,2,0,2)

        self.languageChange()

        self.resize(QSize(532,555).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton34,SIGNAL("clicked()"),self.reject)
        self.connect(self.OKButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.firstnameEdit,SIGNAL("textChanged(const QString&)"),self.firstnameEdit_textChanged)
        self.connect(self.lastnameEdit,SIGNAL("textChanged(const QString&)"),self.lastnameEdit_textChanged)
        self.connect(self.nicknameEdit,SIGNAL("textChanged(const QString&)"),self.nicknameEdit_textChanged)
        self.connect(self.faxEdit,SIGNAL("textChanged(const QString&)"),self.faxEdit_textChanged)

        self.setTabOrder(self.nicknameEdit,self.titleEdit)
        self.setTabOrder(self.titleEdit,self.firstnameEdit)
        self.setTabOrder(self.firstnameEdit,self.lastnameEdit)
        self.setTabOrder(self.lastnameEdit,self.faxEdit)
        self.setTabOrder(self.faxEdit,self.notesEdit)
        self.setTabOrder(self.notesEdit,self.pushButton34)
        self.setTabOrder(self.pushButton34,self.OKButton)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Fax Address Book Entry"))
        self.pushButton34.setText(self.__tr("Cancel"))
        self.OKButton.setText(self.__tr("OK"))
        self.textLabel7.setText(self.__tr("<b>Fax Number:</b>"))
        self.textLabel3.setText(self.__tr("<b>Name/Nickname:<b>"))
        self.textLabel4.setText(self.__tr("Member of Group(s):"))
        self.groupListView.header().setLabel(0,self.__tr("Group Name"))
        self.textLabel6.setText(self.__tr("Notes/Other Information:"))
        self.textLabel12.setText(self.__tr("Note: Items in <b>bold</b> are required fields."))
        self.textLabel5.setText(self.__tr("Title:"))
        self.textLabel1.setText(self.__tr("First Name:"))
        self.textLabel2.setText(self.__tr("Last Name:"))


    def firstnameEdit_textChanged(self,a0):
        print "FaxAddrBookEditForm_base.firstnameEdit_textChanged(const QString&): Not implemented yet"

    def lastnameEdit_textChanged(self,a0):
        print "FaxAddrBookEditForm_base.lastnameEdit_textChanged(const QString&): Not implemented yet"

    def checkBox3_toggled(self,a0):
        print "FaxAddrBookEditForm_base.checkBox3_toggled(bool): Not implemented yet"

    def isGroupCheckBox_toggled(self,a0):
        print "FaxAddrBookEditForm_base.isGroupCheckBox_toggled(bool): Not implemented yet"

    def groupsButton2_clicked(self):
        print "FaxAddrBookEditForm_base.groupsButton2_clicked(): Not implemented yet"

    def nicknameEdit_textChanged(self,a0):
        print "FaxAddrBookEditForm_base.nicknameEdit_textChanged(const QString&): Not implemented yet"

    def faxEdit_textChanged(self,a0):
        print "FaxAddrBookEditForm_base.faxEdit_textChanged(const QString&): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookEditForm_base",s,c)
