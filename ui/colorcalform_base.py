# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/colorcalform_base.ui'
#
# Created: Wed Jul 13 09:36:13 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ColorCalForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ColorCalForm_base")


        ColorCalForm_baseLayout = QGridLayout(self,1,1,11,6,"ColorCalForm_baseLayout")

        self.ContinueButton = QPushButton(self,"ContinueButton")

        ColorCalForm_baseLayout.addWidget(self.ContinueButton,1,3)
        spacer1 = QSpacerItem(335,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ColorCalForm_baseLayout.addItem(spacer1,1,1)

        self.CancelButton = QPushButton(self,"CancelButton")

        ColorCalForm_baseLayout.addWidget(self.CancelButton,1,2)

        self.ColorCalGroup = QButtonGroup(self,"ColorCalGroup")
        self.ColorCalGroup.setColumnLayout(0,Qt.Vertical)
        self.ColorCalGroup.layout().setSpacing(6)
        self.ColorCalGroup.layout().setMargin(11)
        ColorCalGroupLayout = QGridLayout(self.ColorCalGroup.layout())
        ColorCalGroupLayout.setAlignment(Qt.AlignTop)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.radioButton12 = QRadioButton(self.ColorCalGroup,"radioButton12")
        layout2.addWidget(self.radioButton12)

        self.radioButton13 = QRadioButton(self.ColorCalGroup,"radioButton13")
        layout2.addWidget(self.radioButton13)

        self.radioButton14 = QRadioButton(self.ColorCalGroup,"radioButton14")
        layout2.addWidget(self.radioButton14)

        self.radioButton15 = QRadioButton(self.ColorCalGroup,"radioButton15")
        self.radioButton15.setChecked(1)
        layout2.addWidget(self.radioButton15)

        self.radioButton16 = QRadioButton(self.ColorCalGroup,"radioButton16")
        layout2.addWidget(self.radioButton16)

        self.radioButton17 = QRadioButton(self.ColorCalGroup,"radioButton17")
        layout2.addWidget(self.radioButton17)

        self.radioButton18 = QRadioButton(self.ColorCalGroup,"radioButton18")
        layout2.addWidget(self.radioButton18)

        ColorCalGroupLayout.addLayout(layout2,1,0)

        self.textLabel2_2 = QLabel(self.ColorCalGroup,"textLabel2_2")
        self.textLabel2_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        ColorCalGroupLayout.addWidget(self.textLabel2_2,0,0)

        ColorCalForm_baseLayout.addMultiCellWidget(self.ColorCalGroup,0,0,0,3)

        self.languageChange()

        self.resize(QSize(610,220).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.ColorCalGroup,SIGNAL("clicked(int)"),self.ColorCalGroup_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Color Calibration"))
        self.ContinueButton.setText(self.__tr("Next >"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.ColorCalGroup.setTitle(self.__tr("Color Calibration"))
        self.radioButton12.setText(self.__tr("1"))
        self.radioButton13.setText(self.__tr("2"))
        self.radioButton14.setText(self.__tr("3"))
        self.radioButton15.setText(self.__tr("4"))
        self.radioButton16.setText(self.__tr("5"))
        self.radioButton17.setText(self.__tr("6"))
        self.radioButton18.setText(self.__tr("7"))
        self.textLabel2_2.setText(self.__tr("Choose the numbered image labeled \"1\" thru \"7\" that is <b>best color matched</b> to the image labeled \"X\"."))


    def buttonGroup2_clicked(self,a0):
        print "ColorCalForm_base.buttonGroup2_clicked(int): Not implemented yet"

    def ColorCalGroup_released(self,a0):
        print "ColorCalForm_base.ColorCalGroup_released(int): Not implemented yet"

    def ColorCalGroup_clicked(self,a0):
        print "ColorCalForm_base.ColorCalGroup_clicked(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ColorCalForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ColorCalForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
