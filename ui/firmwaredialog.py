# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2011 Hewlett-Packard Development Company, L.P.
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
# Author: Sarbeswar Meher
#

# Std Lib
import operator
import signal

# Local
from base.g import *
from base import device, utils
from prnt import cups
from base.codes import *
from ui_utils import *

# Qt
from qt import *

# Ui
from firmwaredialog_base import FirmwareDialog_Base

class FirmwareDialog(QDialog, FirmwareDialog_Base):
    def __init__(self, parent, device_uri):
	QDialog.__init__(self, parent)        
	self.setupUi(self)        
	self.device_uri = device_uri
        self.initUi()
        QTimer.singleShot(0, self.updateUi)
	
    def initUi(self):
        self.DeviceComboBox.setFilter({'fw-download' : (operator.gt, 0)})
        self.DeviceComboBox.setParent(self)
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.close)
        self.connect(self.DownloadFirmwareButton, SIGNAL("clicked()"), self.downloadFirmware)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Application icon
	self.setIcon(load_pixmap('hp_logo', '128x128'))

        if self.device_uri:
            self.DeviceComboBox.setInitialDevice(self.device_uri)


    def updateUi(self):
        self.DeviceComboBox.updateUi()


    def DeviceUriComboBox_currentChanged(self, device_uri):
        self.device_uri = device_uri
        # Update


    def DeviceUriComboBox_noDevices(self):
        self.FailureUI(self.__tr("<b>No devices that support firmware download found.</b>"))
        self.close()


    def downloadFirmware(self):
        d = None

        try:
            try:
                d = device.Device(self.device_uri)
            except Error:
                self.CheckDeviceUI()
                return

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    ok = d.downloadFirmware()

                else:
                    self.CheckDeviceUI()

        finally:
            if d is not None:
                d.close()

        self.close()



    def __tr(self,s,c = None):
        return qApp.translate("FirmwareDialog",s,c)

    def FailureUI(self, error_text):
        
        QMessageBox.critical(self,
		self.caption(),
		error_text,
		QMessageBox.Ok,
		QMessageBox.NoButton,
		QMessageBox.NoButton)


    def CheckDeviceUI(self):
         return self.FailureUI(self.__tr("<b>Unable to communicate with device or device is in an error state.</b><p>Please check device setup and try again.</p>"))

