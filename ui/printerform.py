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
import signal

# Local
from base.g import *
from base.codes import *
from base import utils, device
from prnt import cups
from ui_utils import load_pixmap

# Qt
from qt import *
from scrollprint import ScrollPrintView



class PrinterForm(QMainWindow):
    def __init__(self, printer_name=None, args=None,
                 parent=None,name=None,modal=0,fl=0):

        QMainWindow.__init__(self,parent,name,fl)

        self.printer_name = printer_name
        self.file_list = []
        self.args = args
        self.init_failed = False

        self.statusBar()

        self.setIcon(load_pixmap('hp_logo', '128x128'))
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        if not name:
            self.setName("PrinterForm")

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        self.FormLayout = QGridLayout(self.centralWidget(),1,1,11,6,"FormLayout")
        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.languageChange()

        self.cups_printers = device.getSupportedCUPSPrinters()
        log.debug(self.cups_printers)

        if  not self.printer_name: # no -p provided
            t = device.probeDevices(['cups'])
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
                self.device_uri = devices[0][0]

            else:
                from chooseprinterdlg import ChoosePrinterDlg
                dlg = ChoosePrinterDlg(self.cups_printers)
                if dlg.exec_loop() == QDialog.Accepted:
                    self.printer_name = dlg.printer_name
                    self.device_uri = dlg.device_uri
                else:
                    self.init_failed = True

        else: # -p provided
            for p in self.cups_printers:
                if p.name == self.printer_name:
                    self.device_uri = p.device_uri
                    break
            else:
                self.FailureUI("<b>Invalid printer name.</b><p>Please check the parameters to hp-print and try again.")
                self.init_failed = True


        if not self.init_failed:
            self.PrintView = ScrollPrintView(None, self.centralWidget(), self, "PrintView")
            self.FormLayout.addWidget(self.PrintView,0,0)

            try:
                self.cur_device = device.Device(device_uri=self.device_uri,
                                                 printer_name=self.printer_name)
            except Error, e:
                log.error("Invalid device URI or printer name.")
                self.FailureUI("<b>Invalid device URI or printer name.</b><p>Please check the parameters to hp-print and try again.")
                self.init_failed = True

            else:
                self.device_uri = self.cur_device.device_uri
                user_conf.set('last_used', 'device_uri', self.device_uri)

                log.debug(self.device_uri)

                self.statusBar().message(self.device_uri)

        QTimer.singleShot(0, self.InitialUpdate)
        

    def InitialUpdate(self):
        if self.init_failed:
            self.close()
            return

        self.PrintView.onDeviceChange(self.cur_device)

        if self.args is not None:
            for f in self.args:
                self.PrintView.addFile(f)

        if self.printer_name is not None:
            self.PrintView.onPrinterChange(self.printer_name)


    def FailureUI(self, error_text):
        log.error(unicode(error_text).replace("<b>", "").replace("</b>", "").replace("<p>", " "))
        QMessageBox.critical(self,
                             self.caption(),
                             error_text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Print"))


    def __tr(self,s,c = None):
        return qApp.translate("PrinterForm",s,c)
