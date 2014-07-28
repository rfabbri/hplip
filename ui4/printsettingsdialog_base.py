# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/printsettingsdialog_base.ui'
#
# Created: Mon May  4 14:30:36 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(700, 500)
        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
        self.TitleLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridlayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line, 1, 0, 1, 2)
        self.PrinterName = PrinterNameComboBox(Dialog)
        self.PrinterName.setObjectName("PrinterName")
        self.gridlayout.addWidget(self.PrinterName, 2, 0, 1, 2)
        self.OptionsToolBox = PrintSettingsToolbox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionsToolBox.sizePolicy().hasHeightForWidth())
        self.OptionsToolBox.setSizePolicy(sizePolicy)
        self.OptionsToolBox.setObjectName("OptionsToolBox")
        self.gridlayout.addWidget(self.OptionsToolBox, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(461, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.CloseButton = QtGui.QPushButton(Dialog)
        self.CloseButton.setObjectName("CloseButton")
        self.gridlayout.addWidget(self.CloseButton, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.OptionsToolBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Print Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.TitleLabel.setText(QtGui.QApplication.translate("Dialog", "Print Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.CloseButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from printsettingstoolbox import PrintSettingsToolbox
from printernamecombobox import PrinterNameComboBox
