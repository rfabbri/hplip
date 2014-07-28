# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/colorcal4form_base.ui'
#
# Created: Tue May 17 16:20:37 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ColorCal4Form_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ColorCal4Form_base")


        ColorCal4Form_baseLayout = QGridLayout(self,1,1,6,6,"ColorCal4Form_baseLayout")

        self.pushButton1 = QPushButton(self,"pushButton1")

        ColorCal4Form_baseLayout.addWidget(self.pushButton1,4,4)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setTextFormat(QLabel.RichText)
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        ColorCal4Form_baseLayout.addMultiCellWidget(self.textLabel1,0,1,0,2)
        spacer16 = QSpacerItem(20,101,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ColorCal4Form_baseLayout.addMultiCell(spacer16,2,3,0,0)
        spacer17 = QSpacerItem(20,101,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ColorCal4Form_baseLayout.addItem(spacer17,3,4)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(6)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)
        spacer3 = QSpacerItem(60,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1Layout.addItem(spacer3,1,4)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.GrayLetterComboBox = QComboBox(0,self.groupBox1,"GrayLetterComboBox")
        GrayLetterComboBox_font = QFont(self.GrayLetterComboBox.font())
        GrayLetterComboBox_font.setFamily("Courier [Adobe]")
        GrayLetterComboBox_font.setBold(1)
        self.GrayLetterComboBox.setFont(GrayLetterComboBox_font)
        layout2.addWidget(self.GrayLetterComboBox)

        self.GrayNumberComboBox = QComboBox(0,self.groupBox1,"GrayNumberComboBox")
        GrayNumberComboBox_font = QFont(self.GrayNumberComboBox.font())
        GrayNumberComboBox_font.setFamily("Courier [Adobe]")
        GrayNumberComboBox_font.setBold(1)
        self.GrayNumberComboBox.setFont(GrayNumberComboBox_font)
        layout2.addWidget(self.GrayNumberComboBox)

        groupBox1Layout.addMultiCellLayout(layout2,1,1,1,3)
        spacer4 = QSpacerItem(60,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1Layout.addItem(spacer4,1,0)

        self.gray_plot_png = QLabel(self.groupBox1,"gray_plot_png")
        self.gray_plot_png.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.gray_plot_png.sizePolicy().hasHeightForWidth()))
        self.gray_plot_png.setMinimumSize(QSize(75,75))
        self.gray_plot_png.setMaximumSize(QSize(75,75))
        self.gray_plot_png.setScaledContents(1)

        groupBox1Layout.addWidget(self.gray_plot_png,0,2)
        spacer1 = QSpacerItem(50,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1Layout.addMultiCell(spacer1,0,0,3,4)
        spacer2 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1Layout.addMultiCell(spacer2,0,0,0,1)

        ColorCal4Form_baseLayout.addMultiCellWidget(self.groupBox1,0,0,3,4)

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(6)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.color_plot_png = QLabel(self.groupBox2,"color_plot_png")
        self.color_plot_png.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.color_plot_png.sizePolicy().hasHeightForWidth()))
        self.color_plot_png.setMinimumSize(QSize(75,75))
        self.color_plot_png.setMaximumSize(QSize(75,75))
        self.color_plot_png.setScaledContents(1)

        groupBox2Layout.addWidget(self.color_plot_png,0,2)
        spacer12 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addMultiCell(spacer12,0,0,0,1)
        spacer14 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addMultiCell(spacer14,0,0,3,4)
        spacer15 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer15,1,4)
        spacer13 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer13,1,0)

        layout1 = QHBoxLayout(None,0,6,"layout1")

        self.ColorLetterComboBox = QComboBox(0,self.groupBox2,"ColorLetterComboBox")
        ColorLetterComboBox_font = QFont(self.ColorLetterComboBox.font())
        ColorLetterComboBox_font.setFamily("Courier [Adobe]")
        ColorLetterComboBox_font.setBold(1)
        self.ColorLetterComboBox.setFont(ColorLetterComboBox_font)
        layout1.addWidget(self.ColorLetterComboBox)

        self.ColorNumberComboBox = QComboBox(0,self.groupBox2,"ColorNumberComboBox")
        ColorNumberComboBox_font = QFont(self.ColorNumberComboBox.font())
        ColorNumberComboBox_font.setFamily("Courier [Adobe]")
        ColorNumberComboBox_font.setBold(1)
        self.ColorNumberComboBox.setFont(ColorNumberComboBox_font)
        layout1.addWidget(self.ColorNumberComboBox)

        groupBox2Layout.addMultiCellLayout(layout1,1,1,1,3)

        ColorCal4Form_baseLayout.addMultiCellWidget(self.groupBox2,1,2,3,4)
        spacer9 = QSpacerItem(310,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ColorCal4Form_baseLayout.addItem(spacer9,4,0)

        self.pushButton2 = QPushButton(self,"pushButton2")

        ColorCal4Form_baseLayout.addWidget(self.pushButton2,4,1)

        self.UseDefaultsButton = QPushButton(self,"UseDefaultsButton")

        ColorCal4Form_baseLayout.addMultiCellWidget(self.UseDefaultsButton,4,4,2,3)

        self.languageChange()

        self.resize(QSize(656,380).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.pushButton1,SIGNAL("clicked()"),self.accept)
        self.connect(self.ColorNumberComboBox,SIGNAL("highlighted(const QString&)"),self.ColorNumberComboBox_highlighted)
        self.connect(self.ColorLetterComboBox,SIGNAL("highlighted(const QString&)"),self.ColorLetterComboBox_highlighted)
        self.connect(self.GrayLetterComboBox,SIGNAL("highlighted(const QString&)"),self.GrayLetterComboBox_highlighted)
        self.connect(self.GrayNumberComboBox,SIGNAL("highlighted(const QString&)"),self.GrayNumberComboBox_highlighted)
        self.connect(self.UseDefaultsButton,SIGNAL("clicked()"),self.UseDefaultsButton_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Color Calibration"))
        self.pushButton1.setText(self.__tr("Calibrate"))
        self.textLabel1.setText(self.__tr("1. Hold the calibration page at arm's length in front of your eyes.\n"
"<p><p>\n"
"2. Tilt the page away from you. Look at the two large squares, each containing colored patches. For each large square, find the colored path that <b>most closely</b> matches the background color. Each patch has an associated letter and number.\n"
"<p><p>\n"
"3. Choose the letter and number for the matching patches for the gray and color plots.\n"
"<p><p>\n"
"4. Click <i>\"Calibrate\".</i> to continue.\n"
"<p><p>\n"
"(To reset the printer to known defaults, click <i>\"Use Factory Defaults\"</i>)"))
        self.groupBox1.setTitle(self.__tr("Gray Plot"))
        self.GrayLetterComboBox.clear()
        self.GrayLetterComboBox.insertItem(self.__tr("A"))
        self.GrayLetterComboBox.insertItem(self.__tr("B"))
        self.GrayLetterComboBox.insertItem(self.__tr("C"))
        self.GrayLetterComboBox.insertItem(self.__tr("D"))
        self.GrayLetterComboBox.insertItem(self.__tr("E"))
        self.GrayLetterComboBox.insertItem(self.__tr("F"))
        self.GrayLetterComboBox.insertItem(self.__tr("G"))
        self.GrayLetterComboBox.insertItem(self.__tr("H"))
        self.GrayLetterComboBox.insertItem(self.__tr("I"))
        self.GrayLetterComboBox.insertItem(self.__tr("J"))
        self.GrayLetterComboBox.insertItem(self.__tr("K"))
        self.GrayLetterComboBox.insertItem(self.__tr("L"))
        self.GrayLetterComboBox.insertItem(self.__tr("M"))
        self.GrayLetterComboBox.insertItem(self.__tr("N"))
        self.GrayNumberComboBox.clear()
        self.GrayNumberComboBox.insertItem(self.__tr("1"))
        self.GrayNumberComboBox.insertItem(self.__tr("2"))
        self.GrayNumberComboBox.insertItem(self.__tr("3"))
        self.GrayNumberComboBox.insertItem(self.__tr("4"))
        self.GrayNumberComboBox.insertItem(self.__tr("5"))
        self.GrayNumberComboBox.insertItem(self.__tr("6"))
        self.GrayNumberComboBox.insertItem(self.__tr("7"))
        self.GrayNumberComboBox.insertItem(self.__tr("8"))
        self.GrayNumberComboBox.insertItem(self.__tr("9"))
        self.GrayNumberComboBox.insertItem(self.__tr("10"))
        self.GrayNumberComboBox.insertItem(self.__tr("11"))
        self.GrayNumberComboBox.insertItem(self.__tr("12"))
        self.GrayNumberComboBox.insertItem(self.__tr("13"))
        self.GrayNumberComboBox.insertItem(self.__tr("14"))
        self.groupBox2.setTitle(self.__tr("Color Plot"))
        self.ColorLetterComboBox.clear()
        self.ColorLetterComboBox.insertItem(self.__tr("P"))
        self.ColorLetterComboBox.insertItem(self.__tr("Q"))
        self.ColorLetterComboBox.insertItem(self.__tr("R"))
        self.ColorLetterComboBox.insertItem(self.__tr("S"))
        self.ColorLetterComboBox.insertItem(self.__tr("T"))
        self.ColorLetterComboBox.insertItem(self.__tr("U"))
        self.ColorLetterComboBox.insertItem(self.__tr("V"))
        self.ColorNumberComboBox.clear()
        self.ColorNumberComboBox.insertItem(self.__tr("1"))
        self.ColorNumberComboBox.insertItem(self.__tr("2"))
        self.ColorNumberComboBox.insertItem(self.__tr("3"))
        self.ColorNumberComboBox.insertItem(self.__tr("4"))
        self.ColorNumberComboBox.insertItem(self.__tr("5"))
        self.ColorNumberComboBox.insertItem(self.__tr("6"))
        self.ColorNumberComboBox.insertItem(self.__tr("7"))
        self.pushButton2.setText(self.__tr("Cancel"))
        self.UseDefaultsButton.setText(self.__tr("Use Factory Defaults"))


    def ColorNumberComboBox_highlighted(self,a0):
        print "ColorCal4Form_base.ColorNumberComboBox_highlighted(const QString&): Not implemented yet"

    def ColorLetterComboBox_highlighted(self,a0):
        print "ColorCal4Form_base.ColorLetterComboBox_highlighted(const QString&): Not implemented yet"

    def GrayLetterComboBox_highlighted(self,a0):
        print "ColorCal4Form_base.GrayLetterComboBox_highlighted(const QString&): Not implemented yet"

    def GrayNumberComboBox_highlighted(self,a0):
        print "ColorCal4Form_base.GrayNumberComboBox_highlighted(const QString&): Not implemented yet"

    def UseDefaultsButton_clicked(self):
        print "ColorCal4Form_base.UseDefaultsButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ColorCal4Form_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ColorCal4Form_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
