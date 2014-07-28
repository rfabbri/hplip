# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/cleaningform2_base.ui'
#
# Created: Fri Apr 1 14:51:32 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class CleaningForm2_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("CleaningForm2_base")

        self.setSizeGripEnabled(1)

        CleaningForm2_baseLayout = QGridLayout(self,1,1,6,6,"CleaningForm2_baseLayout")

        self.Icon = QLabel(self,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setMinimumSize(QSize(71,65))
        self.Icon.setMaximumSize(QSize(71,65))
        self.Icon.setScaledContents(1)

        CleaningForm2_baseLayout.addWidget(self.Icon,1,0)

        self.Finish = QPushButton(self,"Finish")

        CleaningForm2_baseLayout.addWidget(self.Finish,3,3)
        spacer2 = QSpacerItem(211,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        CleaningForm2_baseLayout.addMultiCell(spacer2,3,3,0,1)

        self.CleaningText = QLabel(self,"CleaningText")

        CleaningForm2_baseLayout.addMultiCellWidget(self.CleaningText,1,1,1,3)
        spacer5 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        CleaningForm2_baseLayout.addItem(spacer5,2,2)

        self.CleaningTitle = QLabel(self,"CleaningTitle")

        CleaningForm2_baseLayout.addMultiCellWidget(self.CleaningTitle,0,0,1,3)

        self.languageChange()

        self.resize(QSize(562,186).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.Finish,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Cleaning"))
        self.Finish.setText(self.__tr("Finish"))
        self.CleaningText.setText(self.__tr("Please wait while the test page is printed. Check this page to see if the problem was fixed. If the test page looks fine click <b>Finish </b>to quit the cleaning procedure. Otherwise, replace the print cartridges and click <b>Finish</b>."))
        self.CleaningTitle.setText(self.__tr("<b>Cleaning Level 3 Performed</b>"))


    def __tr(self,s,c = None):
        return qApp.translate("CleaningForm2_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = CleaningForm2_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
