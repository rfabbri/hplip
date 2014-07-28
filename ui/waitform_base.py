# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waitform_base.ui'
#
# Created: Wed Oct 26 13:21:40 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class WaitForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("WaitForm_base")


        WaitForm_baseLayout = QGridLayout(self,1,1,11,6,"WaitForm_baseLayout")

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.textLabel3 = QLabel(self,"textLabel3")
        layout2.addWidget(self.textLabel3)

        self.ProgressBar = QProgressBar(self,"ProgressBar")
        layout2.addWidget(self.ProgressBar)

        WaitForm_baseLayout.addMultiCellLayout(layout2,0,0,0,2)
        spacer10 = QSpacerItem(20,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        WaitForm_baseLayout.addItem(spacer10,1,1)

        self.cancelPushButton = QPushButton(self,"cancelPushButton")
        self.cancelPushButton.setEnabled(0)

        WaitForm_baseLayout.addWidget(self.cancelPushButton,2,1)
        spacer2 = QSpacerItem(121,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        WaitForm_baseLayout.addItem(spacer2,2,2)
        spacer3 = QSpacerItem(131,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        WaitForm_baseLayout.addItem(spacer3,2,0)

        self.languageChange()

        self.resize(QSize(424,115).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelPushButton,SIGNAL("clicked()"),self.cancelPushButton_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Waiting"))
        self.textLabel3.setText(self.__tr("<b>Waiting for procedure to finish...</b>"))
        self.cancelPushButton.setText(self.__tr("Cancel"))


    def cancelPushButton_clicked(self):
        print "WaitForm_base.cancelPushButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("WaitForm_base",s,c)
