# -*- coding: utf-8 -*-
#
# (c) Copyright 2011-2014 Hewlett-Packard Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Authors: Amarnath Chitumalla
#

#global
import os
import os.path
import sys
import signal

# Local
from base.g import *
from base import utils
from prnt import cups
from base.codes import *
from ui_utils import *


# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtGui import QMessageBox
from PyQt4 import QtCore, QtGui

HPLIP_INFO_SITE ="http://hplip.sourceforge.net/hplip_web.conf"

class Ui_Dialog(object):
    def setupUi(self, Dialog, printerName, device_uri,Error_msg):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 180)
        self.printerName=printerName
        self.device_uri=device_uri
        self.Error_msg=Error_msg
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
        spacerItem2 = QtGui.QSpacerItem(200, 51, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
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
        self.gridlayout.addWidget(self.NextButton, 2, 3, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 2, 4, 1, 1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        if self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP SmartInstall/Mass storage Disabler", None, QtGui.QApplication.UnicodeUTF8))
        else:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Queues diagnose", None, QtGui.QApplication.UnicodeUTF8))
        if self.Error_msg == QUEUES_PAUSED:
            self.label.setText(QtGui.QApplication.translate("Dialog", "Print/Fax Queue is Paused", None, QtGui.QApplication.UnicodeUTF8))
        elif self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
            self.label.setText(QtGui.QApplication.translate("Dialog", "Smart Install Device(s) Detected", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.label.setText(QtGui.QApplication.translate("Dialog", "Queue needs to be reconfigured", None, QtGui.QApplication.UnicodeUTF8))
            
        if self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
            text= "Smart Install is enabled in "+ self.printerName + " device(s). \nDo you want to download and disable smart install to perform device functionalities?"
        elif self.Error_msg == QUEUES_INCORRECT_PPD:
            text= "'"+ self.printerName + "' is using incorrect PPD file. Do you want to remove and reconfigure queue?"
        elif self.Error_msg == QUEUES_PAUSED:
            text="'"+ self.printerName + "' is paused. Do you want to enable queue?"
        elif self.Error_msg == QUEUES_CONFIG_ERROR:
            text="'"+ self.printerName + "' is not configured using hp-setup utility. Click 'Remove and Setup' to remove and reconfigure queue."

        if self.Error_msg != QUEUES_MSG_SENDING:
            self.TitleLabel.setText(QtGui.QApplication.translate("Dialog", text, None, QtGui.QApplication.UnicodeUTF8))
#            if self.Error_msg == QUEUES_PAUSED or self.Error_msg == QUEUES_INCORRECT_PPD or self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
            if self.Error_msg == QUEUES_PAUSED or self.Error_msg == QUEUES_INCORRECT_PPD:
                self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Yes", None, QtGui.QApplication.UnicodeUTF8))
                self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "No", None, QtGui.QApplication.UnicodeUTF8))

            elif self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
                self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Download and Disable", None, QtGui.QApplication.UnicodeUTF8))
                self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

            else:
                self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Remove and Setup", None, QtGui.QApplication.UnicodeUTF8))
                self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


# Ui

class QueuesDiagnose(QDialog, Ui_Dialog):
    def __init__(self, parent, printerName, device_uri, Error_msg,passwordObj=None):
        QDialog.__init__(self, parent)
        self.result = False
        self.printerName = printerName
        self.device_uri = device_uri
        self.Error_msg = Error_msg
        self.passwordObj = passwordObj
        self.setupUi(self, self.printerName, self.device_uri,self.Error_msg)
        self.user_settings = UserSettings()
        self.user_settings.load()
        self.user_settings.debug()

        self.initUi()

    def init(self, printerName, device_uri, Error_msg):
        QDialog.__init__(self,None)
        self.printerName = printerName
        self.device_uri = device_uri
        self.Error_msg = Error_msg
        self.setupUi(self, printerName, device_uri,Error_msg)
        self.user_settings = UserSettings()
        self.user_settings.load()
        self.user_settings.debug()

        self.initUi()


    def initUi(self):
        # connect signals/slots
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButton_clicked)
        self.connect(self.NextButton, SIGNAL("clicked()"), self.NextButton_clicked)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Application icon
        self.setWindowIcon(QIcon(load_pixmap('hp_logo', '128x128')))


    #
    # Misc
    #
    def displayPage(self, page):
        self.updateStepText(page)
        self.StackedWidget.setCurrentIndex(page)

    def CancelButton_clicked(self):
        self.close()


    def NextButton_clicked(self):
        beginWaitCursor()
        try:
            if self.Error_msg ==  QUEUES_SMART_INSTALL_ENABLED:
                self.disable_smart_install()

            elif  self.Error_msg == QUEUES_PAUSED:
                cups.enablePrinter(self.printerName)
                msg ="'"+self.printerName+"' is enabled successfully"
                SuccessUI(self, self.__tr(msg))

            else:
                status, status_str = cups.cups_operation(cups.delPrinter, GUI_MODE, 'qt4', self, self.printerName)

                if status != cups.IPP_OK:
                    msg="Failed to remove ' "+self.printerName+" ' queue.\nRemove using hp-toolbox..."
                    FailureUI(self, self.__tr(msg))
                else:
                    msg="' "+self.printerName+" ' removed successfully.\nRe-configuring this printer by hp-setup..."
                    log.debug(msg)
                    path = utils.which('hp-setup')
                    if path:
                        log.debug("Starting hp-setup")
                        utils.run('hp-setup --gui')

        finally:
            endWaitCursor()
        self.result = True
        self.close()

    def showMessage(self,msg):
        FailureUI(self, self.__tr(msg))

    def showSuccessMessage(self,msg):
        SuccessUI(self, self.__tr(msg))

    def __tr(self,s,c = None):
        return qApp.translate("PluginDialog",s,c)


    def disable_smart_install(self):
        if not utils.check_network_connection():
            FailureUI(self, self.__tr("Internet connection not found."))
        else:
            sts, HPLIP_file = utils.download_from_network(HPLIP_INFO_SITE)
            if sts is True:
                hplip_si_conf = ConfigBase(HPLIP_file)
                source = hplip_si_conf.get("SMART_INSTALL","url","")
                if not source :
                    FailureUI(self, self.__tr("Failed to download %s"%HPLIP_INFO_SITE))
                    return 

            response_file, smart_install_run = utils.download_from_network(source)
            response_asc, smart_install_asc = utils.download_from_network(source+'.asc')
            
            if response_file  and response_asc :
                if self.passwordObj == None:
                    try:
                        from base.password import Password
                    except ImportError:
                        return SIH_FAILED_TO_VERIFY_DIG_SIGN, smart_install_run , ""
                    self.passwordObj = Password(GUI_MODE)

                if utils.ERROR_NONE == utils.validateDownloadFile(smart_install_run, smart_install_asc, "", self.passwordObj):
                    sts, out = utils.run("sh %s"%smart_install_run)
                else:
                
                    if QMessageBox.question(self, self.__tr("Digital signature download failed"),
                        self.__tr("<b>The download of the digital signature file failed.</b><p>Without this file, it is not possible to authenticate and validate this tool prior to installation.</p>Do you still want to run Smart Install disabler?"),
                        QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                        # Disabling without verification.
                        sts, out = utils.run("sh %s"%smart_install_run)

            else:
                if not response_asc:
                    FailureUI(self, self.__tr("Failed to download %s file."%(source+'.asc')))
                else:
                    FailureUI(self, self.__tr("Failed to download %s file."%source))


