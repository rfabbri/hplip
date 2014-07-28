# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upgradedialog_base.ui'
#
# Created: Thu Feb  9 18:16:03 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog, distro_tier,msg):
        self.distro_tier = distro_tier
        self.msg= msg 
        Dialog.setObjectName("Dialog")
        Dialog.resize(369, 205)
        self.centralwidget = QtGui.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.MainLabel = QtGui.QLabel(self.centralwidget)
        self.MainLabel.setGeometry(QtCore.QRect(10, 10, 351, 51))
        self.MainLabel.setObjectName("MainLabel")
        self.installRadioBtton = QtGui.QRadioButton(self.centralwidget)
        self.installRadioBtton.setGeometry(QtCore.QRect(10, 65, 350, 22))
        self.installRadioBtton.setChecked(True)
        self.installRadioBtton.setObjectName("installRadioBtton")
        self.remindRadioBtton = QtGui.QRadioButton(self.centralwidget)
        self.remindRadioBtton.setGeometry(QtCore.QRect(10, 96, 141, 22))
        self.remindRadioBtton.setObjectName("remindRadioBtton")
        self.dontRemindRadioBtton = QtGui.QRadioButton(self.centralwidget)
        self.dontRemindRadioBtton.setGeometry(QtCore.QRect(10, 126, 161, 22))
        self.dontRemindRadioBtton.setObjectName("dontRemindRadioBtton")
        self.daysSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.daysSpinBox.setGeometry(QtCore.QRect(152, 94, 55, 27))
        self.daysSpinBox.setMinimum(1)
        self.daysSpinBox.setMaximum(365)
        self.daysSpinBox.setEnabled(False)
        self.daysSpinBox.setObjectName("daysSpinBox")
        self.DaysLabel = QtGui.QLabel(self.centralwidget)
        self.DaysLabel.setGeometry(QtCore.QRect(211, 98, 67, 21))
        self.DaysLabel.setObjectName("DaysLabel")
        self.CancelButton = QtGui.QPushButton(self.centralwidget)
        self.CancelButton.setGeometry(QtCore.QRect(270, 160, 91, 31))
        self.CancelButton.setObjectName("CancelButton")
        self.NextButton = QtGui.QPushButton(self.centralwidget)
        self.NextButton.setGeometry(QtCore.QRect(159, 160, 96, 31))
        self.NextButton.setObjectName("NextButton")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Upgrade Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.MainLabel.setText(QtGui.QApplication.translate("Dialog", self.msg, None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        if self.distro_tier == 1:
            self.installRadioBtton.setText(QtGui.QApplication.translate("Dialog", "Download and Install", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.installRadioBtton.setText(QtGui.QApplication.translate("Dialog", "Follow steps from www.hplip.net", None, QtGui.QApplication.UnicodeUTF8))
        self.remindRadioBtton.setText(QtGui.QApplication.translate("Dialog", "Remind me after", None, QtGui.QApplication.UnicodeUTF8))
        self.dontRemindRadioBtton.setText(QtGui.QApplication.translate("Dialog", "Don\'t remind again", None, QtGui.QApplication.UnicodeUTF8))
        self.DaysLabel.setText(QtGui.QApplication.translate("Dialog", "days", None, QtGui.QApplication.UnicodeUTF8))
