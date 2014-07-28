# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/colorcalform2_base.ui'
#
# Created: Wed Jul 13 09:36:13 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ColorCalForm2_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ColorCalForm2_base")


        ColorCalForm2_baseLayout = QGridLayout(self,1,1,11,6,"ColorCalForm2_baseLayout")

        self.CancelButton = QPushButton(self,"CancelButton")

        ColorCalForm2_baseLayout.addWidget(self.CancelButton,1,2)

        self.ContinueButton = QPushButton(self,"ContinueButton")

        ColorCalForm2_baseLayout.addWidget(self.ContinueButton,1,3)
        spacer1 = QSpacerItem(270,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ColorCalForm2_baseLayout.addItem(spacer1,1,1)

        self.buttonGroup = QButtonGroup(self,"buttonGroup")
        self.buttonGroup.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup.layout().setSpacing(6)
        self.buttonGroup.layout().setMargin(11)
        buttonGroupLayout = QGridLayout(self.buttonGroup.layout())
        buttonGroupLayout.setAlignment(Qt.AlignTop)

        self.Icon = QLabel(self.buttonGroup,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setScaledContents(1)

        buttonGroupLayout.addWidget(self.Icon,0,0)

        self.textLabel2_2 = QLabel(self.buttonGroup,"textLabel2_2")
        self.textLabel2_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        buttonGroupLayout.addMultiCellWidget(self.textLabel2_2,0,0,1,4)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.textLabel1 = QLabel(self.buttonGroup,"textLabel1")
        layout3.addWidget(self.textLabel1)

        self.SpinBox = QSpinBox(self.buttonGroup,"SpinBox")
        self.SpinBox.setMaxValue(81)
        self.SpinBox.setMinValue(1)
        layout3.addWidget(self.SpinBox)

        buttonGroupLayout.addMultiCellLayout(layout3,2,2,2,3)
        spacer3 = QSpacerItem(351,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonGroupLayout.addItem(spacer3,2,4)
        spacer4 = QSpacerItem(251,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonGroupLayout.addMultiCell(spacer4,2,2,0,1)
        spacer5 = QSpacerItem(20,21,QSizePolicy.Minimum,QSizePolicy.Expanding)
        buttonGroupLayout.addItem(spacer5,1,2)
        spacer6 = QSpacerItem(20,61,QSizePolicy.Minimum,QSizePolicy.Expanding)
        buttonGroupLayout.addItem(spacer6,3,3)

        ColorCalForm2_baseLayout.addMultiCellWidget(self.buttonGroup,0,0,0,3)

        self.languageChange()

        self.resize(QSize(952,327).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.SpinBox,SIGNAL("valueChanged(int)"),self.SpinBox_valueChanged)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Color Calibration"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.ContinueButton.setText(self.__tr("Next >"))
        self.buttonGroup.setTitle(QString.null)
        self.textLabel2_2.setText(self.__tr("<b>A page of color patches is printing. When it is complete, follow these steps:</b>\n"
"<p><b>1.</b> Hold the page approximately 8 inches (~20cm) in front of your eyes.\n"
"<p><b>2.</b> Slowly move the page away from you until the numbered patches fade to match the background.\n"
"<p><b>3.</b> Select the number (below) between <i>1</i> and <i>81 </i>of the numbered patch that <b>best </b>matches the background:"))
        self.textLabel1.setText(self.__tr("Number of best matching patch (1-81):"))


    def buttonGroup_clicked(self,a0):
        print "ColorCalForm2_base.buttonGroup_clicked(int): Not implemented yet"

    def SpinBox_valueChanged(self,a0):
        print "ColorCalForm2_base.SpinBox_valueChanged(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ColorCalForm2_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ColorCalForm2_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
