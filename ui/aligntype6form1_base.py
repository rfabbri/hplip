# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/aligntype6form1_base.ui'
#
# Created: Fri Apr 1 14:51:30 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AlignType6Form1_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AlignType6Form1_base")


        AlignType6Form1_baseLayout = QGridLayout(self,1,1,11,6,"AlignType6Form1_baseLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        AlignType6Form1_baseLayout.addMultiCellWidget(self.textLabel1,0,0,0,2)

        self.pushButton2 = QPushButton(self,"pushButton2")

        AlignType6Form1_baseLayout.addWidget(self.pushButton2,1,2)

        self.pushButton3 = QPushButton(self,"pushButton3")

        AlignType6Form1_baseLayout.addWidget(self.pushButton3,1,1)
        spacer2 = QSpacerItem(351,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        AlignType6Form1_baseLayout.addItem(spacer2,1,0)

        self.languageChange()

        self.resize(QSize(627,188).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.accept)
        self.connect(self.pushButton3,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Alignment"))
        self.textLabel1.setText(self.__tr("To perform alignment, you will need the <b>alignment page</b> that is automatically printed after you install a print cartridge.\n"
"<p> If you do <b>not</b> have this page, click <i>Print Page</i>.\n"
"<p>If you already have this page, click <i>Next ></i>."))
        self.pushButton2.setText(self.__tr("Next >"))
        self.pushButton3.setText(self.__tr("Print Page"))


    def __tr(self,s,c = None):
        return qApp.translate("AlignType6Form1_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AlignType6Form1_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
