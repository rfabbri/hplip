# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2009 Hewlett-Packard Development Company, L.P.
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
# Authors: Don Welch

# Std Lib
import operator

# Local
from base.g import *
from prnt import cups
from base import device, utils, pml
from copier import copier
from ui_utils import load_pixmap

# Qt
from qt import *
from scrollcopy import ScrollCopyView

class MakeCopiesForm(QMainWindow):
    def __init__(self, bus='cups', device_uri=None, printer_name=None,
                num_copies=None, contrast=None, quality=None,
                reduction=None, fit_to_page=None,
                parent=None, name=None, modal=0, fl=0):

        QMainWindow.__init__(self,parent,name,fl)

        self.setIcon(load_pixmap('hp_logo', '128x128'))

        self.cur_device_uri = device_uri
        self.printer_name = printer_name
        self.init_failed = False
        self.num_copies = num_copies
        self.contrast = contrast
        self.quality = quality
        self.reduction = reduction
        self.fit_to_page = fit_to_page

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        self.FormLayout = QGridLayout(self.centralWidget(),1,1,11,6,"FormLayout")
        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.languageChange()

        if self.cur_device_uri and self.printer_name:
            log.error("You may not specify both a printer (-p) and a device (-d).")
            self.FailureUI(self.__tr("<p><b>You may not specify both a printer (-p) and a device (-d)."))
            self.cur_device_uri, self.printer_name = None, None
            self.init_failed = True

        self.cups_printers = cups.getPrinters()
        log.debug(self.cups_printers)

        if not self.cur_device_uri and not self.printer_name:
            t = device.probeDevices(bus=bus, filter={'copy-type': (operator.gt, 0)})
            probed_devices = []

            for d in t:
                if d.startswith('hp:'):
                    probed_devices.append(d)

            log.debug(probed_devices)

            max_deviceid_size, x, devices = 0, 0, {}

            for d in probed_devices:
                printers = []
                for p in self.cups_printers:
                    if p.device_uri == d:
                        printers.append(p.name)
                devices[x] = (d, printers)
                x += 1
                max_deviceid_size = max(len(d), max_deviceid_size)

            if x == 0:
                from nodevicesform import NoDevicesForm
                self.FailureUI(self.__tr("<p><b>No devices found.</b><p>Please make sure your device is properly installed and try again."))
                self.init_failed = True

            elif x == 1:
                log.info(log.bold("Using device: %s" % devices[0][0]))
                self.cur_device_uri = devices[0][0]


            else:
                from choosedevicedlg import ChooseDeviceDlg
                dlg = ChooseDeviceDlg(devices) #, ['hp'])

                if dlg.exec_loop() == QDialog.Accepted:
                    self.cur_device_uri = dlg.device_uri
                else:
                    self.init_failed = True


        self.CopyView = ScrollCopyView(None, num_copies=num_copies,
                                        contrast=contrast, quality=quality,
                                        reduction=reduction, fit_to_page=fit_to_page,
                                        parent=self.centralWidget(), form=self)

        self.FormLayout.addWidget(self.CopyView,0,0)

        self.cur_device = self.cur_device_uri

        if not self.init_failed:
            try:
                self.cur_device = copier.PMLCopyDevice(device_uri=self.cur_device_uri,
                                            printer_name=self.printer_name)
            except Error:
                log.error("Invalid device URI or printer name.")
                self.FailureUI("<b>Invalid device URI or printer name.</b><p>Please check the parameters to hp-print and try again.")
                self.init_failed = True

            else:

                if self.cur_device.copy_type == COPY_TYPE_NONE:
                    self.FailureUI(self.__tr("<b>Sorry, make copies functionality is not implemented for this device.</b>"))
                    self.close()
                    return

                self.cur_device_uri = self.cur_device.device_uri
                user_conf.set('last_used', 'device_uri',  self.cur_device_uri)

                log.debug(self.cur_device_uri)

                self.statusBar().message(self.cur_device.device_uri)


        QTimer.singleShot(0, self.InitialUpdate)

    def InitialUpdate(self):
        if self.init_failed:
            self.close()
            return

        self.CopyView.onDeviceChange(self.cur_device)

    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Make Copies"))

    def FailureUI(self, error_text):
        QMessageBox.critical(self,
                             self.caption(),
                             error_text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def WarningUI(self, msg):
        QMessageBox.warning(self,
                             self.caption(),
                             msg,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)


    def __tr(self,s,c = None):
        return qApp.translate("MakeCopiesForm",s,c)
