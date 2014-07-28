# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/devicesetupdialog_base.ui'
#
# Created: Mon May  4 14:30:32 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
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
        self.TabWidget = QtGui.QTabWidget(Dialog)
        self.TabWidget.setObjectName("TabWidget")
        self.PowerSettingsTab = QtGui.QWidget()
        self.PowerSettingsTab.setObjectName("PowerSettingsTab")
        self.gridlayout1 = QtGui.QGridLayout(self.PowerSettingsTab)
        self.gridlayout1.setObjectName("gridlayout1")
        self.groupBox = QtGui.QGroupBox(self.PowerSettingsTab)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setObjectName("gridlayout2")
        self.OnRadioButton = QtGui.QRadioButton(self.groupBox)
        self.OnRadioButton.setObjectName("OnRadioButton")
        self.gridlayout2.addWidget(self.OnRadioButton, 0, 0, 1, 2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.OffRadioButton = QtGui.QRadioButton(self.groupBox)
        self.OffRadioButton.setEnabled(True)
        self.OffRadioButton.setObjectName("OffRadioButton")
        self.hboxlayout.addWidget(self.OffRadioButton)
        self.DurationComboBox = QtGui.QComboBox(self.groupBox)
        self.DurationComboBox.setEnabled(False)
        self.DurationComboBox.setObjectName("DurationComboBox")
        self.hboxlayout.addWidget(self.DurationComboBox)
        self.gridlayout2.addLayout(self.hboxlayout, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem, 1, 1, 1, 1)
        self.gridlayout1.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(282, 51, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1, 1, 0, 1, 1)
        self.TabWidget.addTab(self.PowerSettingsTab, "")
        self.gridlayout.addWidget(self.TabWidget, 3, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(510, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.gridlayout.addItem(spacerItem2, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(361, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem3, 5, 0, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 5, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.OffRadioButton, QtCore.SIGNAL("toggled(bool)"), self.DurationComboBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Device Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Device Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Automatic Power Off", None, QtGui.QApplication.UnicodeUTF8))
        self.OnRadioButton.setText(QtGui.QApplication.translate("Dialog", "Always leave printer on", None, QtGui.QApplication.UnicodeUTF8))
        self.OffRadioButton.setText(QtGui.QApplication.translate("Dialog", "Automatically turn printer off after:", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.PowerSettingsTab), QtGui.QApplication.translate("Dialog", "Power Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

from deviceuricombobox import DeviceUriComboBox
