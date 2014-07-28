# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/paperedgealignform_base.ui'
#
# Created: Wed Jul 13 09:36:14 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PaperEdgeAlignForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PaperEdgeAlignForm_base")


        PaperEdgeAlignForm_baseLayout = QGridLayout(self,1,1,11,6,"PaperEdgeAlignForm_baseLayout")
        spacer37 = QSpacerItem(80,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PaperEdgeAlignForm_baseLayout.addItem(spacer37,1,1)

        self.ContinueButton = QPushButton(self,"ContinueButton")

        PaperEdgeAlignForm_baseLayout.addWidget(self.ContinueButton,1,3)

        self.CancelButton = QPushButton(self,"CancelButton")

        PaperEdgeAlignForm_baseLayout.addWidget(self.CancelButton,1,2)

        self.buttonGroup = QButtonGroup(self,"buttonGroup")
        self.buttonGroup.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.buttonGroup.sizePolicy().hasHeightForWidth()))
        self.buttonGroup.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup.layout().setSpacing(6)
        self.buttonGroup.layout().setMargin(11)
        buttonGroupLayout = QGridLayout(self.buttonGroup.layout())
        buttonGroupLayout.setAlignment(Qt.AlignTop)

        layout24 = QHBoxLayout(None,0,6,"layout24")

        self.radioButton1 = QRadioButton(self.buttonGroup,"radioButton1")
        self.radioButton1.setChecked(1)
        layout24.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton(self.buttonGroup,"radioButton2")
        layout24.addWidget(self.radioButton2)

        self.radioButton3 = QRadioButton(self.buttonGroup,"radioButton3")
        layout24.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton(self.buttonGroup,"radioButton4")
        layout24.addWidget(self.radioButton4)

        self.radioButton5 = QRadioButton(self.buttonGroup,"radioButton5")
        layout24.addWidget(self.radioButton5)

        self.radioButton6 = QRadioButton(self.buttonGroup,"radioButton6")
        layout24.addWidget(self.radioButton6)

        self.radioButton7 = QRadioButton(self.buttonGroup,"radioButton7")
        layout24.addWidget(self.radioButton7)

        self.radioButton8 = QRadioButton(self.buttonGroup,"radioButton8")
        layout24.addWidget(self.radioButton8)

        self.radioButton9 = QRadioButton(self.buttonGroup,"radioButton9")
        layout24.addWidget(self.radioButton9)

        self.radioButton10 = QRadioButton(self.buttonGroup,"radioButton10")
        layout24.addWidget(self.radioButton10)

        self.radioButton11 = QRadioButton(self.buttonGroup,"radioButton11")
        layout24.addWidget(self.radioButton11)

        self.radioButton12 = QRadioButton(self.buttonGroup,"radioButton12")
        layout24.addWidget(self.radioButton12)

        self.radioButton13 = QRadioButton(self.buttonGroup,"radioButton13")
        layout24.addWidget(self.radioButton13)

        buttonGroupLayout.addMultiCellLayout(layout24,1,1,0,1)

        self.Icon = QLabel(self.buttonGroup,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setScaledContents(1)

        buttonGroupLayout.addWidget(self.Icon,0,0)

        self.textLabel4_2 = QLabel(self.buttonGroup,"textLabel4_2")
        self.textLabel4_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        buttonGroupLayout.addWidget(self.textLabel4_2,0,1)

        PaperEdgeAlignForm_baseLayout.addMultiCellWidget(self.buttonGroup,0,0,0,3)

        self.languageChange()

        self.resize(QSize(618,233).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonGroup,SIGNAL("clicked(int)"),self.buttonGroup_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Paper Edge Alignment"))
        self.ContinueButton.setText(self.__tr("Next >"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.buttonGroup.setTitle(self.__tr("Paper Edge"))
        self.radioButton1.setText(self.__tr("1"))
        self.radioButton2.setText(self.__tr("2"))
        self.radioButton3.setText(self.__tr("3"))
        self.radioButton4.setText(self.__tr("4"))
        self.radioButton5.setText(self.__tr("5"))
        self.radioButton6.setText(self.__tr("6"))
        self.radioButton7.setText(self.__tr("7"))
        self.radioButton8.setText(self.__tr("8"))
        self.radioButton9.setText(self.__tr("9"))
        self.radioButton10.setText(self.__tr("10"))
        self.radioButton11.setText(self.__tr("11"))
        self.radioButton12.setText(self.__tr("12"))
        self.radioButton13.setText(self.__tr("13"))
        self.textLabel4_2.setText(self.__tr("Choose the <b>numbered arrow</b> that <b>best </b>marks the edge of the paper."))


    def buttonGroup_clicked(self,a0):
        print "PaperEdgeAlignForm_base.buttonGroup_clicked(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PaperEdgeAlignForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PaperEdgeAlignForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
