# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cleaningform_base.ui'
#
# Created: Tue Sep 5 14:21:27 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class CleaningForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("CleaningForm_base")

        self.setSizeGripEnabled(1)

        CleaningForm_baseLayout = QGridLayout(self,1,1,6,6,"CleaningForm_baseLayout")

        self.Icon = QLabel(self,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setMinimumSize(QSize(71,65))
        self.Icon.setMaximumSize(QSize(71,65))
        self.Icon.setScaledContents(1)

        CleaningForm_baseLayout.addWidget(self.Icon,1,0)

        self.Finish = QPushButton(self,"Finish")

        CleaningForm_baseLayout.addWidget(self.Finish,3,3)
        spacer2 = QSpacerItem(211,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        CleaningForm_baseLayout.addMultiCell(spacer2,3,3,0,1)

        self.Continue = QPushButton(self,"Continue")
        self.Continue.setEnabled(0)

        CleaningForm_baseLayout.addWidget(self.Continue,3,2)

        self.CleaningText = QLabel(self,"CleaningText")

        CleaningForm_baseLayout.addMultiCellWidget(self.CleaningText,1,1,1,3)
        spacer5 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        CleaningForm_baseLayout.addItem(spacer5,2,2)

        self.CleaningTitle = QLabel(self,"CleaningTitle")

        CleaningForm_baseLayout.addMultiCellWidget(self.CleaningTitle,0,0,1,3)

        self.languageChange()

        self.resize(QSize(562,186).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.Finish,SIGNAL("clicked()"),self.reject)
        self.connect(self.Continue,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Please Wait - Cleaning"))
        self.Finish.setText(self.__tr("Finish"))
        self.Continue.setText(self.__tr("Cleaning Level %s"))
        self.CleaningText.setText(self.__tr("Please wait while the test page is printed. Check this page to see if the problem was fixed. If the test page looks fine click <b>Finish </b>to quit the cleaning procedure. Otherwise, click <b>Cleaning Level %s</b> to continue with cleaning."))
        self.CleaningTitle.setText(self.__tr("<b>Please Wait - Cleaning Level %s Being Performed</b>"))


    def __tr(self,s,c = None):
        return qApp.translate("CleaningForm_base",s,c)
