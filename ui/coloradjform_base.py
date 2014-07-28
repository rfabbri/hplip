# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/coloradjform_base.ui'
#
# Created: Wed Jul 13 09:36:13 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ColorAdjForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ColorAdjForm_base")


        ColorAdjForm_baseLayout = QGridLayout(self,1,1,11,6,"ColorAdjForm_baseLayout")

        self.CancelButton = QPushButton(self,"CancelButton")

        ColorAdjForm_baseLayout.addWidget(self.CancelButton,1,2)

        self.ContinueButton = QPushButton(self,"ContinueButton")

        ColorAdjForm_baseLayout.addWidget(self.ContinueButton,1,3)
        spacer1 = QSpacerItem(270,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ColorAdjForm_baseLayout.addItem(spacer1,1,1)

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

        buttonGroupLayout.addMultiCellWidget(self.textLabel2_2,0,0,1,2)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.radioButton1 = QRadioButton(self.buttonGroup,"radioButton1")
        radioButton1_font = QFont(self.radioButton1.font())
        radioButton1_font.setPointSize(8)
        self.radioButton1.setFont(radioButton1_font)
        layout2.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton(self.buttonGroup,"radioButton2")
        radioButton2_font = QFont(self.radioButton2.font())
        radioButton2_font.setPointSize(8)
        self.radioButton2.setFont(radioButton2_font)
        layout2.addWidget(self.radioButton2)

        self.radioButton3 = QRadioButton(self.buttonGroup,"radioButton3")
        radioButton3_font = QFont(self.radioButton3.font())
        radioButton3_font.setPointSize(8)
        self.radioButton3.setFont(radioButton3_font)
        layout2.addWidget(self.radioButton3)

        self.radioButton4 = QRadioButton(self.buttonGroup,"radioButton4")
        radioButton4_font = QFont(self.radioButton4.font())
        radioButton4_font.setPointSize(8)
        self.radioButton4.setFont(radioButton4_font)
        layout2.addWidget(self.radioButton4)

        self.radioButton5 = QRadioButton(self.buttonGroup,"radioButton5")
        radioButton5_font = QFont(self.radioButton5.font())
        radioButton5_font.setPointSize(8)
        self.radioButton5.setFont(radioButton5_font)
        layout2.addWidget(self.radioButton5)

        self.radioButton6 = QRadioButton(self.buttonGroup,"radioButton6")
        radioButton6_font = QFont(self.radioButton6.font())
        radioButton6_font.setPointSize(8)
        self.radioButton6.setFont(radioButton6_font)
        layout2.addWidget(self.radioButton6)

        self.radioButton7 = QRadioButton(self.buttonGroup,"radioButton7")
        radioButton7_font = QFont(self.radioButton7.font())
        radioButton7_font.setPointSize(8)
        self.radioButton7.setFont(radioButton7_font)
        layout2.addWidget(self.radioButton7)

        self.radioButton8 = QRadioButton(self.buttonGroup,"radioButton8")
        radioButton8_font = QFont(self.radioButton8.font())
        radioButton8_font.setPointSize(8)
        self.radioButton8.setFont(radioButton8_font)
        layout2.addWidget(self.radioButton8)

        self.radioButton9 = QRadioButton(self.buttonGroup,"radioButton9")
        radioButton9_font = QFont(self.radioButton9.font())
        radioButton9_font.setPointSize(8)
        self.radioButton9.setFont(radioButton9_font)
        layout2.addWidget(self.radioButton9)

        self.radioButton10 = QRadioButton(self.buttonGroup,"radioButton10")
        radioButton10_font = QFont(self.radioButton10.font())
        radioButton10_font.setPointSize(8)
        self.radioButton10.setFont(radioButton10_font)
        layout2.addWidget(self.radioButton10)

        self.radioButton11 = QRadioButton(self.buttonGroup,"radioButton11")
        radioButton11_font = QFont(self.radioButton11.font())
        radioButton11_font.setPointSize(8)
        self.radioButton11.setFont(radioButton11_font)
        self.radioButton11.setChecked(1)
        layout2.addWidget(self.radioButton11)

        self.radioButton12 = QRadioButton(self.buttonGroup,"radioButton12")
        radioButton12_font = QFont(self.radioButton12.font())
        radioButton12_font.setPointSize(8)
        self.radioButton12.setFont(radioButton12_font)
        layout2.addWidget(self.radioButton12)

        self.radioButton13 = QRadioButton(self.buttonGroup,"radioButton13")
        radioButton13_font = QFont(self.radioButton13.font())
        radioButton13_font.setPointSize(8)
        self.radioButton13.setFont(radioButton13_font)
        layout2.addWidget(self.radioButton13)

        self.radioButton14 = QRadioButton(self.buttonGroup,"radioButton14")
        radioButton14_font = QFont(self.radioButton14.font())
        radioButton14_font.setPointSize(8)
        self.radioButton14.setFont(radioButton14_font)
        layout2.addWidget(self.radioButton14)

        self.radioButton15 = QRadioButton(self.buttonGroup,"radioButton15")
        radioButton15_font = QFont(self.radioButton15.font())
        radioButton15_font.setPointSize(8)
        self.radioButton15.setFont(radioButton15_font)
        layout2.addWidget(self.radioButton15)

        self.radioButton16 = QRadioButton(self.buttonGroup,"radioButton16")
        radioButton16_font = QFont(self.radioButton16.font())
        radioButton16_font.setPointSize(8)
        self.radioButton16.setFont(radioButton16_font)
        layout2.addWidget(self.radioButton16)

        self.radioButton17 = QRadioButton(self.buttonGroup,"radioButton17")
        radioButton17_font = QFont(self.radioButton17.font())
        radioButton17_font.setPointSize(8)
        self.radioButton17.setFont(radioButton17_font)
        layout2.addWidget(self.radioButton17)

        self.radioButton18 = QRadioButton(self.buttonGroup,"radioButton18")
        radioButton18_font = QFont(self.radioButton18.font())
        radioButton18_font.setPointSize(8)
        self.radioButton18.setFont(radioButton18_font)
        layout2.addWidget(self.radioButton18)

        self.radioButton19 = QRadioButton(self.buttonGroup,"radioButton19")
        radioButton19_font = QFont(self.radioButton19.font())
        radioButton19_font.setPointSize(8)
        self.radioButton19.setFont(radioButton19_font)
        layout2.addWidget(self.radioButton19)

        self.radioButton20 = QRadioButton(self.buttonGroup,"radioButton20")
        radioButton20_font = QFont(self.radioButton20.font())
        radioButton20_font.setPointSize(8)
        self.radioButton20.setFont(radioButton20_font)
        layout2.addWidget(self.radioButton20)

        self.radioButton21 = QRadioButton(self.buttonGroup,"radioButton21")
        radioButton21_font = QFont(self.radioButton21.font())
        radioButton21_font.setPointSize(8)
        self.radioButton21.setFont(radioButton21_font)
        layout2.addWidget(self.radioButton21)

        buttonGroupLayout.addMultiCellLayout(layout2,1,1,1,2)
        spacer2 = QSpacerItem(750,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonGroupLayout.addItem(spacer2,2,2)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.LineLabel_2 = QLabel(self.buttonGroup,"LineLabel_2")
        LineLabel_2_font = QFont(self.LineLabel_2.font())
        LineLabel_2_font.setFamily("Times New Roman")
        self.LineLabel_2.setFont(LineLabel_2_font)
        layout3.addWidget(self.LineLabel_2)

        self.LineLabel = QLabel(self.buttonGroup,"LineLabel")
        LineLabel_font = QFont(self.LineLabel.font())
        LineLabel_font.setFamily("Times New Roman")
        self.LineLabel.setFont(LineLabel_font)
        layout3.addWidget(self.LineLabel)

        buttonGroupLayout.addMultiCellLayout(layout3,2,2,0,1)

        ColorAdjForm_baseLayout.addMultiCellWidget(self.buttonGroup,0,0,0,3)

        self.languageChange()

        self.resize(QSize(1013,164).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonGroup,SIGNAL("clicked(int)"),self.buttonGroup_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Color Adjustment"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.ContinueButton.setText(self.__tr("Next >"))
        self.buttonGroup.setTitle(QString.null)
        self.textLabel2_2.setText(self.__tr("Choose the numbered colored box that the color <b>best </b>matches the background color of the bar."))
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
        self.radioButton14.setText(self.__tr("14"))
        self.radioButton15.setText(self.__tr("15"))
        self.radioButton16.setText(self.__tr("16"))
        self.radioButton17.setText(self.__tr("17"))
        self.radioButton18.setText(self.__tr("18"))
        self.radioButton19.setText(self.__tr("19"))
        self.radioButton20.setText(self.__tr("20"))
        self.radioButton21.setText(self.__tr("21"))
        self.LineLabel_2.setText(self.__tr("<b><font size=\"+1\">Line</font></b>"))
        self.LineLabel.setText(self.__tr("<b><font size=\"+1\">X</font></b>"))


    def buttonGroup_clicked(self,a0):
        print "ColorAdjForm_base.buttonGroup_clicked(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ColorAdjForm_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ColorAdjForm_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
