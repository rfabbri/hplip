# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/upgradeform_base.ui'
#
# Created: Thu Feb 9 20:00:42 2012
#      by: The PyQt User Interface Compiler (pyuic) 3.18.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class UpgradeForm_base(QDialog):
    def __init__(self,parent = None,name = "",modal = 0,fl = 0,distro_type =1 , msg="" ):
        QDialog.__init__(self,parent,name,modal,fl)

        if name == "":
            self.setName("HPLIP_Upgrade")
        self.msg=msg
        self.distro_type = distro_type

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(10,10,310,50))


        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setGeometry(QRect(10,60,300,110))

        self.installRadioBtton = QRadioButton(self.buttonGroup1,"installRadioBtton")
        self.installRadioBtton.setGeometry(QRect(10,20,250,20))
        self.installRadioBtton.setChecked(True)


        self.remindRadioBtton = QRadioButton(self.buttonGroup1,"remindRadioBtton")
        self.remindRadioBtton.setGeometry(QRect(10,50,130,20))


        self.daysSpinBox = QSpinBox(self.buttonGroup1,"daysSpinBox")
        self.daysSpinBox.setGeometry(QRect(139,50,50,20))
        self.daysSpinBox.setMinValue(1)
        self.daysSpinBox.setMaxValue(365)
#        self.daysSpinBox.setEnabled(False)


        self.daysLabel = QLabel(self.buttonGroup1,"daysLabel")

        self.daysLabel.setGeometry(QRect(200,50,68,20))


        self.dontRemindRadioBtton = QRadioButton(self.buttonGroup1,"dontRemindRadioBtton")
        self.dontRemindRadioBtton.setGeometry(QRect(10,80,160,20))


        self.NextButton = QPushButton(self,"NextButton")
        self.NextButton.setGeometry(QRect(140,190,90,25))

        self.CancelButton = QPushButton(self,"CancelButton")
        self.CancelButton.setGeometry(QRect(240,190,80,25))

        self.languageChange()
        self.resize(QSize(328,225).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.daysSpinBox,SIGNAL("valueChanged(int)"),self.daysSpinBox_change)

    def daysSpinBox_change(self):
        self.remindRadioBtton.setChecked(True)
        
    def languageChange(self):
        self.setCaption(self.__tr("HPLIP Upgrade Manager"))
        self.textLabel1.setText(self.__tr(self.msg))
        if self.distro_type == 1:
            self.installRadioBtton.setText(self.__tr("Download and Install"))
        else:
            self.installRadioBtton.setText(self.__tr("Follow steps from www.hplip.net"))
        self.remindRadioBtton.setText(self.__tr("Remind me after"))
        self.daysLabel.setText(self.__tr("days"))
        self.dontRemindRadioBtton.setText(self.__tr("Don't remind again"))
        self.NextButton.setText(self.__tr("Ok"))
        self.CancelButton.setText(self.__tr("Cancel"))



    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
