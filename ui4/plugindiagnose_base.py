# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/plugindialog_base.ui'
#
#** Created: Mon Nov 14 15:31:49 2011
#**      by: Qt User Interface Compiler version 4.7.0
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog, upgrade=False):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 180)
        self.upgradePlugin=upgrade
        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
        self.StackedWidget = QtGui.QStackedWidget(Dialog)
        self.StackedWidget.setObjectName("StackedWidget")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.gridlayout1 = QtGui.QGridLayout(self.page)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label = QtGui.QLabel(self.page)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.page)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line, 1, 0, 1, 2)
        self.TitleLabel = QtGui.QLabel(self.page)
        self.TitleLabel.setWordWrap(True)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridlayout1.addWidget(self.TitleLabel, 2, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        spacerItem2 = QtGui.QSpacerItem(278, 51, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem2, 5, 1, 1, 1)
        self.StackedWidget.addWidget(self.page)
        self.gridlayout.addWidget(self.StackedWidget, 0, 0, 1, 5)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2, 1, 0, 1, 4)
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton, 2, 2, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 2, 3, 1, 1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Plug-in Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Driver Plug-in Required", None, QtGui.QApplication.UnicodeUTF8))
        if self.upgradePlugin is False:
            self.TitleLabel.setText(QtGui.QApplication.translate("Dialog", "HP Device proprietary plug-in is missing. Click 'Next' to continue plug-in installation.", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.TitleLabel.setText(QtGui.QApplication.translate("Dialog", "HP Device plug-in version mismatch or some files are corrupted.\nClick 'Next' to install required plug-in.", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

