# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'align10form_base.ui'
#
# Created: Wed Aug 10 21:07:52 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class Align10Form_Base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Align10Form_base")


        Align10Form_baseLayout = QGridLayout(self,1,1,11,6,"Align10Form_baseLayout")

        self.textLabel2 = QLabel(self,"textLabel2")

        Align10Form_baseLayout.addMultiCellWidget(self.textLabel2,0,0,0,2)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")

        self.comboBoxF = QComboBox(0,self,"comboBoxF")

        layout2.addWidget(self.comboBoxF,5,1)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        layout2.addWidget(self.textLabel1_2,1,0)

        self.textLabel1_6 = QLabel(self,"textLabel1_6")

        layout2.addWidget(self.textLabel1_6,5,0)

        self.comboBoxD = QComboBox(0,self,"comboBoxD")

        layout2.addWidget(self.comboBoxD,3,1)

        self.comboBoxE = QComboBox(0,self,"comboBoxE")

        layout2.addWidget(self.comboBoxE,4,1)

        self.textLabel1_3 = QLabel(self,"textLabel1_3")

        layout2.addWidget(self.textLabel1_3,2,0)

        self.textLabel1_4 = QLabel(self,"textLabel1_4")

        layout2.addWidget(self.textLabel1_4,3,0)

        self.comboBoxC = QComboBox(0,self,"comboBoxC")

        layout2.addWidget(self.comboBoxC,2,1)

        self.comboBoxA = QComboBox(0,self,"comboBoxA")

        layout2.addWidget(self.comboBoxA,0,1)

        self.comboBoxH = QComboBox(0,self,"comboBoxH")

        layout2.addWidget(self.comboBoxH,7,1)

        self.textLabel1_7 = QLabel(self,"textLabel1_7")

        layout2.addWidget(self.textLabel1_7,6,0)

        self.textLabel1 = QLabel(self,"textLabel1")

        layout2.addWidget(self.textLabel1,0,0)

        self.textLabel1_5 = QLabel(self,"textLabel1_5")

        layout2.addWidget(self.textLabel1_5,4,0)

        self.textLabel1_8 = QLabel(self,"textLabel1_8")

        layout2.addWidget(self.textLabel1_8,7,0)

        self.comboBoxB = QComboBox(0,self,"comboBoxB")

        layout2.addWidget(self.comboBoxB,1,1)

        self.comboBoxG = QComboBox(0,self,"comboBoxG")

        layout2.addWidget(self.comboBoxG,6,1)

        Align10Form_baseLayout.addMultiCellLayout(layout2,0,1,4,5)
        spacer2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Align10Form_baseLayout.addItem(spacer2,0,3)
        spacer3 = QSpacerItem(20,41,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Align10Form_baseLayout.addItem(spacer3,2,5)

        self.pushButton1 = QPushButton(self,"pushButton1")

        Align10Form_baseLayout.addWidget(self.pushButton1,3,5)

        self.pushButton2 = QPushButton(self,"pushButton2")

        Align10Form_baseLayout.addMultiCellWidget(self.pushButton2,3,3,3,4)
        spacer1 = QSpacerItem(320,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Align10Form_baseLayout.addMultiCell(spacer1,3,3,0,2)
        spacer5 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Align10Form_baseLayout.addItem(spacer5,1,0)

        self.Icon = QLabel(self,"Icon")
        self.Icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth()))
        self.Icon.setMinimumSize(QSize(192,93))
        self.Icon.setMaximumSize(QSize(192,93))
        self.Icon.setScaledContents(1)

        Align10Form_baseLayout.addWidget(self.Icon,1,1)
        spacer4 = QSpacerItem(60,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Align10Form_baseLayout.addMultiCell(spacer4,1,1,2,3)

        self.languageChange()

        self.resize(QSize(520,326).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self.accept)
        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Alignment"))
        self.textLabel2.setText(self.__tr("Examine the page that was printed. Several rows of boxes, each made up of thin lines, appear on the printed page.<p>\n"
"For each row, select the label representing the box in which the shorter inner lines are the most aligned with the longer outer lines.."))
        self.textLabel1_2.setText(self.__tr("<b><font face=\"Courier\">B:</font></b>"))
        self.textLabel1_6.setText(self.__tr("<b><font face=\"Courier\">F:</font></b>"))
        self.textLabel1_3.setText(self.__tr("<b><font face=\"Courier\">C:</font></b>"))
        self.textLabel1_4.setText(self.__tr("<b><font face=\"Courier\">D:</font></b>"))
        self.textLabel1_7.setText(self.__tr("<b><font face=\"Courier\">G:</font></b>"))
        self.textLabel1.setText(self.__tr("<b><font face=\"Courier\">A:</font></b>"))
        self.textLabel1_5.setText(self.__tr("<b><font face=\"Courier\">E:</font></b>"))
        self.textLabel1_8.setText(self.__tr("<b><font face=\"Courier\">H:</font></b>"))
        self.pushButton1.setText(self.__tr("Next >"))
        self.pushButton2.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("Align10Form_Base",s,c)
