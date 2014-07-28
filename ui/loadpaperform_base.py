# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/loadpaperform_base.ui'
#
# Created: Fri Apr 1 14:51:29 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class LoadPaperForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("LoadPaperForm_base")


        LoadPaperForm_baseLayout = QGridLayout(self,1,1,11,6,"LoadPaperForm_baseLayout")

        self.ContinueButton = QPushButton(self,"ContinueButton")

        LoadPaperForm_baseLayout.addWidget(self.ContinueButton,1,3)

        self.CancelButton = QPushButton(self,"CancelButton")

        LoadPaperForm_baseLayout.addWidget(self.CancelButton,1,2)
        spacer7 = QSpacerItem(391,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        LoadPaperForm_baseLayout.addMultiCell(spacer7,1,1,0,1)

        self.textLabel7 = QLabel(self,"textLabel7")
        self.textLabel7.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        LoadPaperForm_baseLayout.addMultiCellWidget(self.textLabel7,0,0,1,3)

        self.Icon = QLabel(self,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setScaledContents(1)

        LoadPaperForm_baseLayout.addWidget(self.Icon,0,0)

        self.languageChange()

        self.resize(QSize(621,178).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Load Plain Paper"))
        self.ContinueButton.setText(self.__tr("Continue"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.textLabel7.setText(self.__tr("A page will be printed. Please load <b>plain paper</b> in the printer and then press continue."))


    def __tr(self,s,c = None):
        return qApp.translate("LoadPaperForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LoadPaperForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
