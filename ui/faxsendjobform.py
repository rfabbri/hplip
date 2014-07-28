# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2009 Hewlett-Packard Development Company, L.P.
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
# Author: Don Welch
#

# Std Lib
import operator

# Local
from base.g import *
from base.codes import *
from base import utils, device
from prnt import cups
from ui_utils import load_pixmap

if 1:
#try:
    from fax import fax
#except ImportError:
if 0:
    # This can fail on Python < 2.3 due to the datetime module
    log.error("Fax send disabled - Python 2.3+ required.")
    sys.exit(1)


# Qt/UI
from qt import *
from scrollfax import ScrollFaxView

# dBus
dbus_avail = False
try:
    import dbus
except ImportError:
    dbus_avail = False



class FaxSendJobForm(QMainWindow):

    def __init__(self, device_uri, printer_name, args,
                 parent=None, name=None,
                 modal=0, fl=0):

        QMainWindow.__init__(self,parent,name,fl)

        self.setIcon(load_pixmap('hp_logo', '128x128'))

        self.init_failed = False
        self.device_uri = device_uri
        self.dev = None
        self.printer_name = printer_name
        bus = ['cups']
        self.filename = ''
        self.username = prop.username
        self.args = args
        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        self.FormLayout = QGridLayout(self.centralWidget(),1,1,11,6,"FormLayout")
        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.languageChange()

#        if self.device_uri and self.printer_name:
#            log.error("You may not specify both a printer (-p) and a device (-d).")
#            self.FailureUI(self.__tr("<p><b>You may not specify both a printer (-p) and a device (-d)."))
#            self.device_uri, self.printer_name = None, None
#            self.init_failed = True

        self.cups_printers = cups.getPrinters()
        log.debug(self.cups_printers)

        if self.printer_name:
            found = False
            for p in self.cups_printers:
                if p.name == printer_name:
                    self.device_uri = p.device_uri
                    found = True
                    break

            if not found:
                self.FailureUI(self.__tr("<b>Unknown printer name: %1</b><p>Please check the printer name and try again.").arg(self.printer_name))

            if found and not p.device_uri.startswith('hpfax:/'):
                self.FailureUI(self.__tr("You must specify a printer that has a device URI in the form 'hpfax:/...'"))
                self.init_failed = True

        if not self.device_uri and not self.printer_name:
            t = device.probeDevices(bus=bus, filter={'fax-type':(operator.gt, FAX_TYPE_NONE)})
            #print t
            probed_devices = []

            for d in t:
                probed_devices.append(d.replace('hp:/', 'hpfax:/'))

            #print probed_devices

            probed_devices = utils.uniqueList(probed_devices)
            log.debug(probed_devices)

            max_deviceid_size, x, devices = 0, 0, {}

            for d in probed_devices:
                printers = []
                for p in self.cups_printers:
                    #print p.device_uri, d
                    if p.device_uri == d:
                        #print "OK"
                        printers.append(p.name)

                devices[x] = (d, printers)
                x += 1
                max_deviceid_size = max(len(d), max_deviceid_size)

            x = len(devices)

            #print devices

            if x == 0:
                from nodevicesform import NoDevicesForm
                self.FailureUI(self.__tr("<p><b>No devices found.</b><p>Please make sure your device is properly installed and try again."))
                self.init_failed = True

            elif x == 1:
                log.info(log.bold("Using device: %s" % devices[0][0]))
                self.device_uri = devices[0][0]

            else:
                from chooseprinterdlg import ChoosePrinterDlg
                dlg = ChoosePrinterDlg(self.cups_printers, ['hpfax'])

                if dlg.exec_loop() == QDialog.Accepted:
                    self.device_uri = dlg.device_uri
                else:
                    self.init_failed = True

        self.dbus_avail, self.service, session_bus = device.init_dbus()

        self.FaxView = ScrollFaxView(self.service, self.centralWidget(), self)
        self.FormLayout.addWidget(self.FaxView,0,0)

        if not self.init_failed:
            if not self.device_uri or not self.device_uri.startswith("hpfax:"):
                log.error("Invalid device URI: %s" % repr(device_uri))
                self.FailureUI(self.__tr("<b>Invalid device URI %1.</b><p>Please check the parameters to hp-print and try again.").arg(repr(device_uri)));
                self.init_failed = True

            else:
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

        self.FaxView.onDeviceChange(self.cur_device)

        if self.args is not None:
            for f in self.args:
                self.FaxView.processFile(f)

        if self.printer_name is not None:
            self.FaxView.onPrinterChange(self.printer_name)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Send Fax"))

    def closeEvent(self, event):
        #print "close"
        #print self.FaxView.lock_file
        utils.unlock(self.FaxView.lock_file)
        event.accept()

    def SuccessUI(self):
        QMessageBox.information(self,
                             self.caption(),
                             self.__tr("<p><b>Fax send completed successfully.</b>"),
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def FailureUI(self, error_text):
        log.error(unicode(error_text).replace("<b>", "").replace("</b>", "").replace("<p>", " "))
        QMessageBox.critical(self,
                             self.caption(),
                             error_text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def WarningUI(self, error_text):
        log.warn(unicode(error_text).replace("<b>", "").replace("</b>", "").replace("<p>", " "))
        QMessageBox.warning(self,
                             self.caption(),
                             error_text,
                             QMessageBox.Ok,
                             QMessageBox.NoButton,
                             QMessageBox.NoButton)

    def __tr(self,s,c = None):
        return qApp.translate("FaxSendJobForm", s, c)
