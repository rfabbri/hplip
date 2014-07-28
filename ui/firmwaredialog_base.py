# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firmwaredialog_base.ui'
#
# Created: Tue Feb 1 21:48:57 2011
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!
#
# Author: Sarbeswar Meher
#

from qt import *

from deviceuricombobox import DeviceUriComboBox


class FirmwareDialog_Base(object):
    def setupUi(self,Dialog):
	Dialog.setModal(True)
        Dialog.setName("FirmwareDialog_Base")

        self.Download_Firmwar = QLabel(Dialog,"Download_Firmware")
        self.Download_Firmwar.setGeometry(QRect(9,9,454,25))
        Download_Firmwar_font = QFont(self.Download_Firmwar.font())
        Download_Firmwar_font.setPointSize(16)
        self.Download_Firmwar.setFont(Download_Firmwar_font)

        self.line = QFrame(Dialog,"line")
        self.line.setGeometry(QRect(9,40,682,3))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setFrameShape(QFrame.HLine)

        self.DownloadFirmwareButton = QPushButton(Dialog,"DownloadFirmwareButton")
        self.DownloadFirmwareButton.setGeometry(QRect(460,320,131,27))

        self.CancelButton = QPushButton(Dialog,"CancelButton")
        self.CancelButton.setGeometry(QRect(600,320,85,27))

        self.frame4 = QFrame(Dialog,"frame4")
        self.frame4.setGeometry(QRect(9,86,682,37))
        self.frame4.setFrameShape(QFrame.StyledPanel)
        self.frame4.setFrameShadow(QFrame.Raised)

        self.textLabel2 = QLabel(self.frame4,"textLabel2")
        self.textLabel2.setGeometry(QRect(10,8,662,17))


        self.DeviceComboBox = DeviceUriComboBox(Dialog)
        self.DeviceComboBox.setGeometry(QRect(9,49,682,26))

        self.languageChange(Dialog)

        self.resize(QSize(709,361).expandedTo(self.minimumSizeHint()))
       
    def languageChange(self, Dialog):
        self.setCaption(self.__tr("HP Device Manager - Download Firmware "))
        self.Download_Firmwar.setText(self.__tr("Download Firmware"))
        self.DownloadFirmwareButton.setText(self.__tr("Download Firmware"))
        self.CancelButton.setText(self.__tr("Cancel"))
        self.textLabel2.setText(self.__tr("Click <i>Download Firmware</i> to begin download process."))


    def __tr(self,s,c = None):
        return qApp.translate("FirmwareDialog_Base",s,c)
