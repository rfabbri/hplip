# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/firmwaredialog_base.ui'
#
# Created: Mon May  4 14:30:33 2009
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
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line, 1, 0, 1, 3)
        self.DeviceComboBox = DeviceUriComboBox(Dialog)
        self.DeviceComboBox.setObjectName("DeviceComboBox")
        self.gridlayout.addWidget(self.DeviceComboBox, 2, 0, 1, 3)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.frame, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 171, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(301, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.DownloadFirmwareButton = QtGui.QPushButton(Dialog)
        self.DownloadFirmwareButton.setObjectName("DownloadFirmwareButton")
        self.gridlayout.addWidget(self.DownloadFirmwareButton, 5, 1, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 5, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Download Firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Download Firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click<span style=\" font-style:italic;\"> Download Firmware</span> to begin download process.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.DownloadFirmwareButton.setText(QtGui.QApplication.translate("Dialog", "Download Firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from deviceuricombobox import DeviceUriComboBox
