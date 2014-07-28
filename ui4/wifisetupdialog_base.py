# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/wifisetupdialog_base.ui'
#
# Created: Thu May 28 11:00:20 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,700,500).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.StackedWidget = QtGui.QStackedWidget(Dialog)
        self.StackedWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.StackedWidget.setObjectName("StackedWidget")

        self.DiscoveryPage = QtGui.QWidget()
        self.DiscoveryPage.setObjectName("DiscoveryPage")

        self.gridlayout1 = QtGui.QGridLayout(self.DiscoveryPage)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.DiscoveryPage)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,3)

        self.line = QtGui.QFrame(self.DiscoveryPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,3)

        self.MainTitleLabel = QtGui.QLabel(self.DiscoveryPage)
        self.MainTitleLabel.setTextFormat(QtCore.Qt.RichText)
        self.MainTitleLabel.setWordWrap(True)
        self.MainTitleLabel.setObjectName("MainTitleLabel")
        self.gridlayout1.addWidget(self.MainTitleLabel,2,0,1,3)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,3,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1,4,0,1,1)

        self.Picture = QtGui.QLabel(self.DiscoveryPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Picture.sizePolicy().hasHeightForWidth())
        self.Picture.setSizePolicy(sizePolicy)
        self.Picture.setMinimumSize(QtCore.QSize(396,128))
        self.Picture.setMaximumSize(QtCore.QSize(396,128))
        self.Picture.setObjectName("Picture")
        self.gridlayout1.addWidget(self.Picture,4,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,4,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(664,61,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem3,5,0,1,3)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.InfoIcon = QtGui.QLabel(self.DiscoveryPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.InfoIcon.sizePolicy().hasHeightForWidth())
        self.InfoIcon.setSizePolicy(sizePolicy)
        self.InfoIcon.setMinimumSize(QtCore.QSize(16,16))
        self.InfoIcon.setMaximumSize(QtCore.QSize(16,16))
        self.InfoIcon.setObjectName("InfoIcon")
        self.hboxlayout.addWidget(self.InfoIcon)

        self.label_14 = QtGui.QLabel(self.DiscoveryPage)
        self.label_14.setWordWrap(True)
        self.label_14.setObjectName("label_14")
        self.hboxlayout.addWidget(self.label_14)
        self.gridlayout1.addLayout(self.hboxlayout,6,0,1,3)
        self.StackedWidget.addWidget(self.DiscoveryPage)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout2 = QtGui.QGridLayout(self.page_2)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_4 = QtGui.QLabel(self.page_2)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4,0,0,1,2)

        self.line_2 = QtGui.QFrame(self.page_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout2.addWidget(self.line_2,1,0,1,3)

        self.DevicesTableWidget = QtGui.QTableWidget(self.page_2)
        self.DevicesTableWidget.setAlternatingRowColors(True)
        self.DevicesTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.DevicesTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.DevicesTableWidget.setSortingEnabled(False)
        self.DevicesTableWidget.setObjectName("DevicesTableWidget")
        self.gridlayout2.addWidget(self.DevicesTableWidget,2,0,1,3)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.DevicesFoundIcon = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DevicesFoundIcon.sizePolicy().hasHeightForWidth())
        self.DevicesFoundIcon.setSizePolicy(sizePolicy)
        self.DevicesFoundIcon.setMinimumSize(QtCore.QSize(16,16))
        self.DevicesFoundIcon.setMaximumSize(QtCore.QSize(16,16))
        self.DevicesFoundIcon.setFrameShape(QtGui.QFrame.NoFrame)
        self.DevicesFoundIcon.setObjectName("DevicesFoundIcon")
        self.hboxlayout1.addWidget(self.DevicesFoundIcon)

        self.DevicesFoundLabel = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DevicesFoundLabel.sizePolicy().hasHeightForWidth())
        self.DevicesFoundLabel.setSizePolicy(sizePolicy)
        self.DevicesFoundLabel.setWordWrap(True)
        self.DevicesFoundLabel.setObjectName("DevicesFoundLabel")
        self.hboxlayout1.addWidget(self.DevicesFoundLabel)
        self.gridlayout2.addLayout(self.hboxlayout1,3,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(21,28,QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem4,3,1,1,1)

        self.RefreshButton = QtGui.QPushButton(self.page_2)
        self.RefreshButton.setObjectName("RefreshButton")
        self.gridlayout2.addWidget(self.RefreshButton,3,2,1,1)
        self.StackedWidget.addWidget(self.page_2)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout3 = QtGui.QGridLayout(self.page_3)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_5 = QtGui.QLabel(self.page_3)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridlayout3.addWidget(self.label_5,0,0,1,1)

        self.line_3 = QtGui.QFrame(self.page_3)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout3.addWidget(self.line_3,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.page_3)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout4.setObjectName("gridlayout4")

        self.UndirectedRadioButton = QtGui.QRadioButton(self.groupBox_3)
        self.UndirectedRadioButton.setChecked(True)
        self.UndirectedRadioButton.setObjectName("UndirectedRadioButton")
        self.gridlayout4.addWidget(self.UndirectedRadioButton,0,0,1,3)

        self.DirectedRadioButton = QtGui.QRadioButton(self.groupBox_3)
        self.DirectedRadioButton.setObjectName("DirectedRadioButton")
        self.gridlayout4.addWidget(self.DirectedRadioButton,1,0,1,2)

        self.SSIDLineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.SSIDLineEdit.setEnabled(False)
        self.SSIDLineEdit.setObjectName("SSIDLineEdit")
        self.gridlayout4.addWidget(self.SSIDLineEdit,1,2,1,1)

        self.SearchPushButton = QtGui.QPushButton(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchPushButton.sizePolicy().hasHeightForWidth())
        self.SearchPushButton.setSizePolicy(sizePolicy)
        self.SearchPushButton.setObjectName("SearchPushButton")
        self.gridlayout4.addWidget(self.SearchPushButton,2,0,1,1)

        spacerItem5 = QtGui.QSpacerItem(521,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem5,2,1,1,2)
        self.gridlayout3.addWidget(self.groupBox_3,2,0,1,1)

        self.SelectSSIDGroupBox = QtGui.QGroupBox(self.page_3)
        self.SelectSSIDGroupBox.setCheckable(False)
        self.SelectSSIDGroupBox.setObjectName("SelectSSIDGroupBox")

        self.gridlayout5 = QtGui.QGridLayout(self.SelectSSIDGroupBox)
        self.gridlayout5.setObjectName("gridlayout5")

        spacerItem6 = QtGui.QSpacerItem(421,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem6,0,0,1,2)

        self.ShowExtendedCheckBox = QtGui.QCheckBox(self.SelectSSIDGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ShowExtendedCheckBox.sizePolicy().hasHeightForWidth())
        self.ShowExtendedCheckBox.setSizePolicy(sizePolicy)
        self.ShowExtendedCheckBox.setObjectName("ShowExtendedCheckBox")
        self.gridlayout5.addWidget(self.ShowExtendedCheckBox,0,2,1,1)

        self.NetworksTableWidget = QtGui.QTableWidget(self.SelectSSIDGroupBox)
        self.NetworksTableWidget.setAlternatingRowColors(True)
        self.NetworksTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.NetworksTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.NetworksTableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.NetworksTableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.NetworksTableWidget.setObjectName("NetworksTableWidget")
        self.gridlayout5.addWidget(self.NetworksTableWidget,1,0,1,3)

        self.NetworksFoundIcon = QtGui.QLabel(self.SelectSSIDGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NetworksFoundIcon.sizePolicy().hasHeightForWidth())
        self.NetworksFoundIcon.setSizePolicy(sizePolicy)
        self.NetworksFoundIcon.setMinimumSize(QtCore.QSize(16,16))
        self.NetworksFoundIcon.setMaximumSize(QtCore.QSize(16,16))
        self.NetworksFoundIcon.setFrameShape(QtGui.QFrame.NoFrame)
        self.NetworksFoundIcon.setObjectName("NetworksFoundIcon")
        self.gridlayout5.addWidget(self.NetworksFoundIcon,2,0,1,1)

        self.NetworksFoundLabel = QtGui.QLabel(self.SelectSSIDGroupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NetworksFoundLabel.sizePolicy().hasHeightForWidth())
        self.NetworksFoundLabel.setSizePolicy(sizePolicy)
        self.NetworksFoundLabel.setWordWrap(True)
        self.NetworksFoundLabel.setObjectName("NetworksFoundLabel")
        self.gridlayout5.addWidget(self.NetworksFoundLabel,2,1,1,2)
        self.gridlayout3.addWidget(self.SelectSSIDGroupBox,3,0,1,1)
        self.StackedWidget.addWidget(self.page_3)

        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")

        self.gridlayout6 = QtGui.QGridLayout(self.page_5)
        self.gridlayout6.setObjectName("gridlayout6")

        self.label_15 = QtGui.QLabel(self.page_5)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridlayout6.addWidget(self.label_15,0,0,1,2)

        self.line_4 = QtGui.QFrame(self.page_5)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridlayout6.addWidget(self.line_4,1,0,1,2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_3 = QtGui.QLabel(self.page_5)
        self.label_3.setObjectName("label_3")
        self.hboxlayout2.addWidget(self.label_3)

        self.SSIDLabel = QtGui.QLabel(self.page_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SSIDLabel.sizePolicy().hasHeightForWidth())
        self.SSIDLabel.setSizePolicy(sizePolicy)
        self.SSIDLabel.setObjectName("SSIDLabel")
        self.hboxlayout2.addWidget(self.SSIDLabel)

        self.StrengthIcon = QtGui.QLabel(self.page_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StrengthIcon.sizePolicy().hasHeightForWidth())
        self.StrengthIcon.setSizePolicy(sizePolicy)
        self.StrengthIcon.setMinimumSize(QtCore.QSize(34,20))
        self.StrengthIcon.setMaximumSize(QtCore.QSize(34,20))
        self.StrengthIcon.setObjectName("StrengthIcon")
        self.hboxlayout2.addWidget(self.StrengthIcon)
        self.gridlayout6.addLayout(self.hboxlayout2,2,0,1,2)

        spacerItem7 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout6.addItem(spacerItem7,3,1,1,1)

        self.groupBox = QtGui.QGroupBox(self.page_5)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout7 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout7.setObjectName("gridlayout7")

        self.WEPRadioButton = ReadOnlyRadioButton(self.groupBox)
        self.WEPRadioButton.setObjectName("WEPRadioButton")
        self.gridlayout7.addWidget(self.WEPRadioButton,0,0,1,1)

        self.WPARadioButton = ReadOnlyRadioButton(self.groupBox)
        self.WPARadioButton.setObjectName("WPARadioButton")
        self.gridlayout7.addWidget(self.WPARadioButton,1,0,1,1)
        self.gridlayout6.addWidget(self.groupBox,4,0,1,2)

        self.groupBox_2 = QtGui.QGroupBox(self.page_5)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout8.setObjectName("gridlayout8")

        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout8.addWidget(self.label_6,0,0,1,1)

        self.KeyLineEdit = QtGui.QLineEdit(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.KeyLineEdit.sizePolicy().hasHeightForWidth())
        self.KeyLineEdit.setSizePolicy(sizePolicy)
        self.KeyLineEdit.setObjectName("KeyLineEdit")
        self.gridlayout8.addWidget(self.KeyLineEdit,0,1,1,1)

        self.KeysIcon = QtGui.QLabel(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.KeysIcon.sizePolicy().hasHeightForWidth())
        self.KeysIcon.setSizePolicy(sizePolicy)
        self.KeysIcon.setMinimumSize(QtCore.QSize(32,32))
        self.KeysIcon.setMaximumSize(QtCore.QSize(32,32))
        self.KeysIcon.setFrameShape(QtGui.QFrame.NoFrame)
        self.KeysIcon.setObjectName("KeysIcon")
        self.gridlayout8.addWidget(self.KeysIcon,0,2,1,1)

        self.ShowKeyCheckBox = QtGui.QCheckBox(self.groupBox_2)
        self.ShowKeyCheckBox.setObjectName("ShowKeyCheckBox")
        self.gridlayout8.addWidget(self.ShowKeyCheckBox,1,1,1,2)
        self.gridlayout6.addWidget(self.groupBox_2,5,0,1,2)

        spacerItem8 = QtGui.QSpacerItem(638,81,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout6.addItem(spacerItem8,6,1,1,1)

        self.ConfigureIcon = QtGui.QLabel(self.page_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConfigureIcon.sizePolicy().hasHeightForWidth())
        self.ConfigureIcon.setSizePolicy(sizePolicy)
        self.ConfigureIcon.setMinimumSize(QtCore.QSize(16,16))
        self.ConfigureIcon.setMaximumSize(QtCore.QSize(16,16))
        self.ConfigureIcon.setObjectName("ConfigureIcon")
        self.gridlayout6.addWidget(self.ConfigureIcon,7,0,1,1)

        self.label_7 = QtGui.QLabel(self.page_5)
        self.label_7.setObjectName("label_7")
        self.gridlayout6.addWidget(self.label_7,7,1,1,1)
        self.StackedWidget.addWidget(self.page_5)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout9 = QtGui.QGridLayout(self.page)
        self.gridlayout9.setObjectName("gridlayout9")

        self.label_16 = QtGui.QLabel(self.page)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridlayout9.addWidget(self.label_16,0,0,1,1)

        self.line_5 = QtGui.QFrame(self.page)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout9.addWidget(self.line_5,1,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.page)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout10 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout10.setObjectName("gridlayout10")

        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.gridlayout10.addWidget(self.label_8,0,0,1,1)

        self.SSIDLabel_2 = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SSIDLabel_2.sizePolicy().hasHeightForWidth())
        self.SSIDLabel_2.setSizePolicy(sizePolicy)
        self.SSIDLabel_2.setObjectName("SSIDLabel_2")
        self.gridlayout10.addWidget(self.SSIDLabel_2,0,1,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.SignalStrengthIcon = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SignalStrengthIcon.sizePolicy().hasHeightForWidth())
        self.SignalStrengthIcon.setSizePolicy(sizePolicy)
        self.SignalStrengthIcon.setMinimumSize(QtCore.QSize(34,20))
        self.SignalStrengthIcon.setMaximumSize(QtCore.QSize(34,20))
        self.SignalStrengthIcon.setObjectName("SignalStrengthIcon")
        self.hboxlayout3.addWidget(self.SignalStrengthIcon)

        self.SignalStrengthLabel = QtGui.QLabel(self.groupBox_4)
        self.SignalStrengthLabel.setObjectName("SignalStrengthLabel")
        self.hboxlayout3.addWidget(self.SignalStrengthLabel)
        self.gridlayout10.addLayout(self.hboxlayout3,0,2,1,1)

        self.label_9 = QtGui.QLabel(self.groupBox_4)
        self.label_9.setObjectName("label_9")
        self.gridlayout10.addWidget(self.label_9,1,0,1,1)

        self.AddressModeLabel = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddressModeLabel.sizePolicy().hasHeightForWidth())
        self.AddressModeLabel.setSizePolicy(sizePolicy)
        self.AddressModeLabel.setObjectName("AddressModeLabel")
        self.gridlayout10.addWidget(self.AddressModeLabel,1,1,1,1)

        self.label_12 = QtGui.QLabel(self.groupBox_4)
        self.label_12.setObjectName("label_12")
        self.gridlayout10.addWidget(self.label_12,2,0,1,1)

        self.HostnameLabel = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HostnameLabel.sizePolicy().hasHeightForWidth())
        self.HostnameLabel.setSizePolicy(sizePolicy)
        self.HostnameLabel.setObjectName("HostnameLabel")
        self.gridlayout10.addWidget(self.HostnameLabel,2,1,1,1)

        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setObjectName("label_10")
        self.gridlayout10.addWidget(self.label_10,3,0,1,1)

        self.IPAddressLabel = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPAddressLabel.sizePolicy().hasHeightForWidth())
        self.IPAddressLabel.setSizePolicy(sizePolicy)
        self.IPAddressLabel.setObjectName("IPAddressLabel")
        self.gridlayout10.addWidget(self.IPAddressLabel,3,1,1,1)

        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        self.gridlayout10.addWidget(self.label_11,4,0,1,1)

        self.GatewayLabel = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GatewayLabel.sizePolicy().hasHeightForWidth())
        self.GatewayLabel.setSizePolicy(sizePolicy)
        self.GatewayLabel.setObjectName("GatewayLabel")
        self.gridlayout10.addWidget(self.GatewayLabel,4,1,1,1)

        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setObjectName("label_13")
        self.gridlayout10.addWidget(self.label_13,5,0,1,1)

        self.DNSLabel = QtGui.QLabel(self.groupBox_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DNSLabel.sizePolicy().hasHeightForWidth())
        self.DNSLabel.setSizePolicy(sizePolicy)
        self.DNSLabel.setObjectName("DNSLabel")
        self.gridlayout10.addWidget(self.DNSLabel,5,1,1,1)
        self.gridlayout9.addWidget(self.groupBox_4,2,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName("groupBox_5")

        self.gridlayout11 = QtGui.QGridLayout(self.groupBox_5)
        self.gridlayout11.setObjectName("gridlayout11")

        self.ExitIcon = QtGui.QLabel(self.groupBox_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExitIcon.sizePolicy().hasHeightForWidth())
        self.ExitIcon.setSizePolicy(sizePolicy)
        self.ExitIcon.setMinimumSize(QtCore.QSize(16,16))
        self.ExitIcon.setMaximumSize(QtCore.QSize(16,16))
        self.ExitIcon.setFrameShape(QtGui.QFrame.NoFrame)
        self.ExitIcon.setObjectName("ExitIcon")
        self.gridlayout11.addWidget(self.ExitIcon,0,0,1,1)

        self.ExitLabel = QtGui.QLabel(self.groupBox_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExitLabel.sizePolicy().hasHeightForWidth())
        self.ExitLabel.setSizePolicy(sizePolicy)
        self.ExitLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.ExitLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ExitLabel.setWordWrap(True)
        self.ExitLabel.setObjectName("ExitLabel")
        self.gridlayout11.addWidget(self.ExitLabel,0,1,2,2)

        spacerItem9 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout11.addItem(spacerItem9,1,0,1,1)

        spacerItem10 = QtGui.QSpacerItem(501,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout11.addItem(spacerItem10,2,0,1,2)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.PageLabel2 = QtGui.QLabel(self.groupBox_5)
        self.PageLabel2.setObjectName("PageLabel2")
        self.hboxlayout4.addWidget(self.PageLabel2)

        self.PageSpinBox = QtGui.QSpinBox(self.groupBox_5)
        self.PageSpinBox.setMinimum(1)
        self.PageSpinBox.setObjectName("PageSpinBox")
        self.hboxlayout4.addWidget(self.PageSpinBox)

        self.PageLabel = QtGui.QLabel(self.groupBox_5)
        self.PageLabel.setObjectName("PageLabel")
        self.hboxlayout4.addWidget(self.PageLabel)
        self.gridlayout11.addLayout(self.hboxlayout4,2,2,1,1)
        self.gridlayout9.addWidget(self.groupBox_5,3,0,1,1)

        spacerItem11 = QtGui.QSpacerItem(664,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout9.addItem(spacerItem11,4,0,1,1)
        self.StackedWidget.addWidget(self.page)
        self.gridlayout.addWidget(self.StackedWidget,0,0,1,5)

        self.StepText = QtGui.QLabel(Dialog)
        self.StepText.setObjectName("StepText")
        self.gridlayout.addWidget(self.StepText,1,0,1,1)

        spacerItem12 = QtGui.QSpacerItem(181,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem12,1,1,1,1)

        self.BackButton = QtGui.QPushButton(Dialog)
        self.BackButton.setObjectName("BackButton")
        self.gridlayout.addWidget(self.BackButton,1,2,1,1)

        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton,1,3,1,1)

        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton,1,4,1,1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Wifi Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Wireless (Wifi/802.11) Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.MainTitleLabel.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This utility allows you configure your wireless capable printer using a temporary USB connection. You will be prompted to disconnect the USB cable once wireless network setup is complete. </p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Note: This configuration utility does not setup (install) your printer on this computer. Use hp-setup to setup your printer once it has been configured on the network by this utility.</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Note: Only select wireless capable printers are supported by this utility.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please plug-in your wireless capable printer at this time (using a USB cable) and click<span style=\" font-style:italic;\"> Next &gt;</span> to continue.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Select From Discovered Wireless Capable Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.DevicesTableWidget.clear()
        self.DevicesTableWidget.setColumnCount(0)
        self.DevicesTableWidget.setRowCount(0)
        self.DevicesFoundLabel.setText(QtGui.QApplication.translate("Dialog", "Found 0 wireless capable devices on the USB bus.", None, QtGui.QApplication.UnicodeUTF8))
        self.RefreshButton.setText(QtGui.QApplication.translate("Dialog", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Find and Select a Wireless Network", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Find Wireless Network", None, QtGui.QApplication.UnicodeUTF8))
        self.UndirectedRadioButton.setText(QtGui.QApplication.translate("Dialog", "Search for wireless networks automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.DirectedRadioButton.setText(QtGui.QApplication.translate("Dialog", "Enter the name (SSID) of a known wireless network:", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchPushButton.setText(QtGui.QApplication.translate("Dialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.SelectSSIDGroupBox.setTitle(QtGui.QApplication.translate("Dialog", "Wireless Networks", None, QtGui.QApplication.UnicodeUTF8))
        self.ShowExtendedCheckBox.setText(QtGui.QApplication.translate("Dialog", "Show extended information", None, QtGui.QApplication.UnicodeUTF8))
        self.NetworksTableWidget.clear()
        self.NetworksTableWidget.setColumnCount(0)
        self.NetworksTableWidget.setRowCount(0)
        self.NetworksFoundLabel.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Found %1 wireless networks. Click <span style=\" font-style:italic;\">Search</span> to perform another search.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "Configure Wireless", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\';\">Wireless Network Name (SSID):</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.SSIDLabel.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\';\">(unknown)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Wireless Security Type", None, QtGui.QApplication.UnicodeUTF8))
        self.WEPRadioButton.setText(QtGui.QApplication.translate("Dialog", "WEP (Wired Equivalent Privacy)", None, QtGui.QApplication.UnicodeUTF8))
        self.WPARadioButton.setText(QtGui.QApplication.translate("Dialog", "WPA (Wi-Fi Protected Access)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Wireless Security Key", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Key:", None, QtGui.QApplication.UnicodeUTF8))
        self.ShowKeyCheckBox.setText(QtGui.QApplication.translate("Dialog", "Show key", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Enter the security key for the network, and click </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-style:italic;\">Connect</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"> to continue.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Dialog", "Wireless Configuration Results", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Dialog", "Wireless Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Network:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.SSIDLabel_2.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.SignalStrengthIcon.setText(QtGui.QApplication.translate("Dialog", "(icon)", None, QtGui.QApplication.UnicodeUTF8))
        self.SignalStrengthLabel.setText(QtGui.QApplication.translate("Dialog", "0/5 (0dBm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Address Mode:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AddressModeLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Hostname:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.HostnameLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">IP Address:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.IPAddressLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">Gateway Address:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.GatewayLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">DNS Address:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.DNSLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("Dialog", "Messages", None, QtGui.QApplication.UnicodeUTF8))
        self.ExitLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.PageLabel2.setText(QtGui.QApplication.translate("Dialog", "Message:", None, QtGui.QApplication.UnicodeUTF8))
        self.PageLabel.setText(QtGui.QApplication.translate("Dialog", "of XXX", None, QtGui.QApplication.UnicodeUTF8))
        self.BackButton.setText(QtGui.QApplication.translate("Dialog", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from readonlyradiobutton import ReadOnlyRadioButton
