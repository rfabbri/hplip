# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/setupmanualfind_base.ui'
#
# Created: Fri Apr 25 15:08:10 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SetupManualFind_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SetupManualFind_base")


        SetupManualFind_baseLayout = QGridLayout(self,1,1,11,6,"SetupManualFind_baseLayout")
        spacer19 = QSpacerItem(331,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupManualFind_baseLayout.addItem(spacer19,3,0)

        self.findHeadingText = QLabel(self,"findHeadingText")
        self.findHeadingText.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        SetupManualFind_baseLayout.addMultiCellWidget(self.findHeadingText,0,0,0,2)

        self.pushButton12 = QPushButton(self,"pushButton12")

        SetupManualFind_baseLayout.addWidget(self.pushButton12,3,1)

        self.pushButton11 = QPushButton(self,"pushButton11")
        self.pushButton11.setDefault(1)

        SetupManualFind_baseLayout.addWidget(self.pushButton11,3,2)
        spacer21 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        SetupManualFind_baseLayout.addItem(spacer21,2,0)

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.findLineEdit = QLineEdit(self,"findLineEdit")
        self.findLineEdit.setMaxLength(50)

        layout3.addWidget(self.findLineEdit,0,1)

        self.hintTextLabel = QLabel(self,"hintTextLabel")
        self.hintTextLabel.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout3.addWidget(self.hintTextLabel,1,1)

        self.findTextLabel = QLabel(self,"findTextLabel")

        layout3.addWidget(self.findTextLabel,0,0)

        SetupManualFind_baseLayout.addMultiCellLayout(layout3,1,1,0,2)

        self.languageChange()

        self.resize(QSize(646,226).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton12,SIGNAL("clicked()"),self.reject)
        self.connect(self.pushButton11,SIGNAL("clicked()"),self.accept)
        self.connect(self.findLineEdit,SIGNAL("textChanged(const QString&)"),self.findLineEdit_textChanged)

        self.setTabOrder(self.findLineEdit,self.pushButton12)
        self.setTabOrder(self.pushButton12,self.pushButton11)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Manually Find Device"))
        self.findHeadingText.setText(self.__tr("TEXT"))
        self.pushButton12.setText(self.__tr("Cancel"))
        self.pushButton11.setText(self.__tr("Find"))
        self.hintTextLabel.setText(self.__tr("textLabel1"))
        self.findTextLabel.setText(self.__tr("IP/HN/SER/USB/DEV:"))


    def findLineEdit_textChanged(self,a0):
        print "SetupManualFind_base.findLineEdit_textChanged(const QString&): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SetupManualFind_base",s,c)
