# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/aligntype6form2_base.ui'
#
# Created: Fri Apr 1 14:51:27 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AlignType6Form2_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AlignType6Form2_base")


        AlignType6Form2_baseLayout = QGridLayout(self,1,1,11,6,"AlignType6Form2_baseLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setTextFormat(QLabel.RichText)
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        AlignType6Form2_baseLayout.addMultiCellWidget(self.textLabel1,0,0,0,1)

        self.pushButton4 = QPushButton(self,"pushButton4")

        AlignType6Form2_baseLayout.addWidget(self.pushButton4,1,1)
        spacer3 = QSpacerItem(581,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        AlignType6Form2_baseLayout.addItem(spacer3,1,0)

        self.languageChange()

        self.resize(QSize(626,211).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton4,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Alignment"))
        self.textLabel1.setText(self.__tr("<b>Follow these steps to complete the alignment:</b>\n"
"<p><b>1.</b> Place the alignment page, with the printed side facing down, on the scanner.\n"
"<p><b>2.</b> Press the <i>Enter</i> or <i>Scan</i> button on the printer.\n"
"<p><b>3.</b> \"Alignment Complete\" will be displayed when the process is finished (on some models).."))
        self.pushButton4.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("AlignType6Form2_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AlignType6Form2_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
