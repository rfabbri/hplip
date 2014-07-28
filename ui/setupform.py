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
# Author: Don Welch, Goutam Korra, Naga Samrat Chowdary Narla,

# Std Lib
import sys
import socket
import re
import gzip
import time
import os.path, os
import operator
import signal

# Local
from base.g import *
from base import device, utils, models, pkit
from prnt import cups
from ui_utils import load_pixmap
from installer import pluginhandler

try:
    from fax import fax
    #from fax import fax
    fax_import_ok = True
except ImportError:
    # This can fail on Python < 2.3 due to the datetime module
    fax_import_ok = False
    log.warning("Fax setup disabled - Python 2.3+ required.")

# Qt
from qt import *
from setupform_base import SetupForm_base
from setupsettings import SetupSettings
from setupmanualfind import SetupManualFind


class DeviceListViewItem(QListViewItem):
    def __init__(self, parent, device_uri, mq, c1='', c2='', c3='', c4=''):
        QListViewItem.__init__(self, parent, c1, c2, c3, c4)
        self.device_uri = device_uri
        self.mq = mq


class PPDListViewItem(QListViewItem):
    def __init__(self, parent, ppd_file, c1=''):
        QListViewItem.__init__(self, parent, ppd_file, c1)
        self.ppd_file = ppd_file


class PrinterNameValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)

        if not input:
            return QValidator.Acceptable, pos

        elif input[pos-1] in u"""~`!@#$%^&*()-=+[]{}()\\/,.<>?'\";:| """:
            return QValidator.Invalid, pos

        # TODO: How to determine if unicode char is "printable" and acceptable
        # to CUPS?
        #elif input != utils.printable(input):
        #    return QValidator.Invalid, pos

        else:
            return QValidator.Acceptable, pos



class PhoneNumValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)

        if not input:
            return QValidator.Acceptable, pos

        elif input[pos-1] not in u'0123456789-(+) ':
            return QValidator.Invalid, pos

        else:
            return QValidator.Acceptable, pos



class SetupForm(SetupForm_base):
    def __init__(self, bus, param, jd_port=1, parent=None, name=None, modal=0, fl=0):
        SetupForm_base.__init__(self, parent, name, modal, fl)

        self.start_page = self.ConnectionPage
        self.first_page = True

        if bus is None:
            self.bus = 'usb'
        else:
            self.bus = bus[0]
            self.start_page = self.ProbedDevicesPage

        if not prop.par_build:
            self.parRadioButton.setEnabled(False)

        if not prop.net_build:
            self.netRadioButton.setEnabled(False)

        if not prop.par_build and not prop.net_build:
            self.bus = 'usb'
            self.start_page = self.ProbedDevicesPage

        self.param = param
        self.jd_port = jd_port

        if self.param:
            # Validate param...
            device_uri, sane_uri, fax_uri = device.makeURI(self.param, self.jd_port)

            if device_uri:
                self.device_uri = device_uri
                self.start_page = self.PPDPage

            else:
                self.FailureUI(self.__tr("<b>Device not found.</b> <p>Please make sure your printer is properly connected and powered-on."))

        self.setIcon(load_pixmap('hp_logo', '128x128'))

        self.connectionTypeButtonGroup.setButton(0)
        self.device_uri = ''
        self.mq = {}
        self.prev_page = None
        self.probe_pat = re.compile(r'(.*?)\s"(.*?)"\s"(.*?)"\s"(.*?)"', re.IGNORECASE)
        self.printer_name = ''
        self.ppd_list = []
        self.location = ''
        self.desc = ''
        self.filter = []
        self.search = ''
        self.ttl = 4
        self.timeout = 5
        self.printer_name_ok = True
        self.fax_name_ok = True
        self.fax_number = ''
        self.fax_name = ''
        self.printer_fax_names_same = False
        self.fax_name_company = ''
        self.fax_location = ''
        self.fax_desc = ''
        self.print_test_page = True
        self.printerNameLineEdit.setValidator(PrinterNameValidator(self.printerNameLineEdit))
        self.faxNameLineEdit.setValidator(PrinterNameValidator(self.faxNameLineEdit))
        self.faxNumberLineEdit.setValidator(PhoneNumValidator(self.faxNumberLineEdit))
        self.setTitleFont(QFont("Helvetica", 16))
        self.setBackEnabled(self.FinishedPage, False)
        self.bg = self.printerNameLineEdit.paletteBackgroundColor()
        self.setHelpEnabled(self.ConnectionPage, False)
        self.setHelpEnabled(self.ProbedDevicesPage, False)
        self.setHelpEnabled(self.PPDPage, False)
        self.setHelpEnabled(self.PrinterNamePage, False)
        self.setHelpEnabled(self.FinishedPage, False)

        self.faxNameLineEdit.setMaxLength(50)
        self.printerNameLineEdit.setMaxLength(50)

        QToolTip.add(self.searchFiltersPushButton2,
            self.__tr('Current: Filter: [%2]  Search: "%3"  TTL: %4  Timeout: %5s').arg(','.join(self.filter)).arg(self.search or '').arg(self.ttl).arg(self.timeout))

        cups.setPasswordCallback(showPasswordUI)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def showPage(self, page):
        orig_page = page

        if self.first_page:
            page = self.start_page
            self.first_page = False

        log.debug("%s %s %s" % ("*"*20, "showPage(%s)" % page.name(), "*"*20))

        try:
            log.debug("%s --> %s" % (self.prev_page.name(), page.name()))
        except AttributeError:
            log.debug("--> %s" % page.name())

        if page is self.ConnectionPage: # start --> ConnectionPage
            pass

        elif page is self.ProbedDevicesPage:
            # ConnectionPage --> ProbedDevicesPage/EnterIPPage/DeviceNotFoundPage
            devices_found = self.updateProbedDevicesPage()


        elif page is self.PPDPage: # ProbedDevicesPage --> PPDPage
            if self.param:
                device_uri, sane_uri, fax_uri = device.makeURI(self.param, self.jd_port)

                if device_uri:
                    self.device_uri = device_uri

            back_end, is_hp, bus, model, serial, dev_file, host, zc, port = \
                device.parseDeviceURI(self.device_uri)

            self.bus = bus
            self.mq = device.queryModelByURI(self.device_uri)

            norm_model = models.normalizeModelName(model).lower()

            pluginObj = pluginhandler.PluginHandle()

            plugin = self.mq.get('plugin', PLUGIN_NONE)
            plugin_reason = self.mq.get('plugin-reason', PLUGIN_REASON_NONE)
            if plugin > PLUGIN_NONE and pluginObj.getStatus() != pluginhandler.PLUGIN_INSTALLED:
                ok, sudo_ok = pkit.run_plugin_command(plugin == PLUGIN_REQUIRED, plugin_reason)
                if not sudo_ok:
                    self.FailureUI(self.__tr("<b>Unable to find an appropriate su/sudo utility to run hp-plugin.</b><p>Install kdesu, gnomesu, or gksu.</p>"))
                    return
                if not ok or pluginObj.getStatus() != pluginhandler.PLUGIN_INSTALLED:
                    if plugin == PLUGIN_REQUIRED:
                        self.FailureUI(self.__tr("<b>The printer you are trying to setup requires a binary driver plug-in and it failed to install.</b><p>Please check your internet connection and try again.</p><p>Visit <u>http://hplipopensource.com</u> for more information.</p>"))
                        return
                    else:
                        self.WarningUI(self.__tr("Either you have chosen to skip the installation of the optional plug-in or that installation has failed.  Your printer may not function at optimal performance."))

            self.updatePPDPage()

        elif page is self.PrinterNamePage:
            self.setDefaultPrinterName()

            if fax_import_ok and prop.fax_build and \
                self.mq.get('fax-type', FAX_TYPE_NONE) not in (FAX_TYPE_NONE, FAX_TYPE_NOT_SUPPORTED):

                self.faxCheckBox.setEnabled(True)
                self.faxCheckBox.setEnabled(True)
                self.faxNameLineEdit.setEnabled(True)
                self.faxNumberLineEdit.setEnabled(True)
                self.faxNameCoLineEdit.setEnabled(True)
                self.faxLocationLineEdit.setEnabled(True)
                self.faxDescriptionLineEdit.setEnabled(True)
                self.faxInfoGroupBox.setEnabled(True)
                self.setup_fax = True
                self.setDefaultFaxName()
                self.readwriteFaxInformation(True)

            else:
                self.setup_fax = False
                self.fax_name_ok = True
                self.defaultFaxNamePushButton.setEnabled(False)
                self.faxCheckBox.setEnabled(False)
                self.faxNameLineEdit.setEnabled(False)
                self.faxNumberLineEdit.setEnabled(False)
                self.faxNameCoLineEdit.setEnabled(False)
                self.faxLocationLineEdit.setEnabled(False)
                self.faxDescriptionLineEdit.setEnabled(False)
                self.faxInfoGroupBox.setEnabled(False)

        elif page is self.FinishedPage:
            self.lineEdit1.setText(self.printer_name)
            self.lineEdit2.setText(self.location)
            self.lineEdit3.setText(self.desc)
            self.lineEdit4.setText(self.ppd_file)

            #log.debug("Restarting CUPS...")
            #status, output = utils.run(restart_cups())
            #log.debug("Restart CUPS returned: exit=%d output=%s" % (status, output))

            print_sts = self.setupPrinter()
            if print_sts == cups.IPP_FORBIDDEN or print_sts == cups.IPP_NOT_AUTHENTICATED or print_sts == cups.IPP_NOT_AUTHORIZED:
                pass
            else:
                if self.setup_fax:
                    if self.setupFax() == cups.IPP_OK:
                        self.readwriteFaxInformation(False)

                        self.lineEdit5.setText(self.fax_number)
                        self.lineEdit6.setText(self.fax_name)
                        self.lineEdit7.setText(self.fax_name_company)
                        self.lineEdit8.setText(self.fax_location)
                        self.lineEdit9.setText(self.fax_desc)

                        self.faxGroupBox.setEnabled(True)

                else:
                    self.faxGroupBox.setEnabled(False)

            if print_sts == cups.IPP_OK:
                self.flashFirmware()

                self.setFinishEnabled(self.FinishedPage, True)
            else:
                self.close()

        if orig_page != page:
            try:
                log.debug("%s --> %s" % (self.prev_page.name(), page.name()))
            except AttributeError:
                log.debug("--> %s" % page.name())

        self.prev_page = page
        QWizard.showPage(self, page)

        if page is self.ProbedDevicesPage: # ConnectionPage --> ProbedDevicesPage/EnterIPPage/DeviceNotFoundPage
            if not devices_found:
                self.FailureUI(self.__tr("<b>No devices found.</b><p>Please make sure your printer is properly connected and powered-on."))


    #
    # CONNECTION TYPE PAGE
    #

    def connectionTypeButtonGroup_clicked(self,a0):
        if a0 == 0:
            self.bus = 'usb'

        elif a0 == 1:
            self.bus = 'net'

        elif a0 == 2:
            self.bus = 'par'

        log.debug(self.bus)


    def searchFiltersPushButton2_clicked(self):
        self.settingsDlg()

    #
    # FILTERS SEARCH SETTINGS
    #

    def settingsDlg(self):
        dlg = SetupSettings(self.bus, self.filter, self.search, self.ttl, self.timeout, self)
        if dlg.exec_loop() == QDialog.Accepted:
            #self.filter = [x.lower().strip() for x in dlg.filter.split(',')]
            self.filter = dlg.filter
            self.search = dlg.search
            self.ttl = dlg.ttl
            self.timeout = dlg.timeout

            t = self.__tr('Current Settings: Filter: [%2]  Search: "%3"  TTL: %4  Timeout: %5s').arg(','.join(self.filter)).arg(self.search or '').arg(self.ttl).arg(self.timeout)

            QToolTip.add(self.searchFiltersPushButton2, t)
            QToolTip.add(self.searchFiltersPushButton, t)
            return True

        return False

    #
    # PROBED DEVICES PAGE
    #

    def updateProbedDevicesPage(self, devices=None, param=''):
        QApplication.setOverrideCursor(QApplication.waitCursor)

        if self.bus == 'net':
            io_str = self.__tr("network")

        elif self.bus == 'usb':
            io_str = self.__tr("USB bus")

        elif self.bus == 'par':
            io_str = self.__tr("parallel port")

        QToolTip.add(self.searchFiltersPushButton, self.__tr('Current Settings: Filter: [%2]  Search: "%3"  TTL: %4  Timeout: %5s').arg(','.join(self.filter)).arg(self.search or '').arg(self.ttl).arg(self.timeout))

        log.debug("Updating probed devices list...")
        log.debug(self.bus)

        self.probedDevicesListView.clear()

        while self.probedDevicesListView.columns():
            self.probedDevicesListView.removeColumn(0)

        self.probedDevicesListView.addColumn(self.__tr("Model"))

        if self.bus == 'usb':
            self.probedDevicesListView.addColumn(self.__tr("Serial No."))

        elif self.bus == 'net':
            self.probedDevicesListView.addColumn(self.__tr("IP Address"))
            self.probedDevicesListView.addColumn(self.__tr("Host Name"))

        elif self.bus == 'par':
            self.probedDevicesListView.addColumn(self.__tr("Device"))

        self.probedDevicesListView.addColumn(self.__tr("Device URI"))

        if devices is None:
            FILTER_MAP = {'print' : None,
                          'none' : None,
                          'scan': 'scan-type',
                          'copy': 'copy-type',
                          'pcard': 'pcard-type',
                          'fax': 'fax-type',
                          }

            filter_dict = {}

            if prop.fax_build and prop.scan_build:
                for f in self.filter:
                    if f in FILTER_MAP:
                        filter_dict[FILTER_MAP[f]] = (operator.gt, 0)
                    else:
                        filter_dict[f] = (operator.gt, 0)
            else:
                filter_dict['scan-type'] = (operator.ge, SCAN_TYPE_NONE)

            if self.bus == 'usb':
                try:
                    from base import smart_install
                except ImportError:
                    log.error("Failed to Import smart_install.py")
                else:   # check if any SmartInstall devices and disables (if not, ignores)
                    smart_install.disable(GUI_MODE, 'qt3')

            devices = device.probeDevices([self.bus], self.timeout, self.ttl, filter_dict, self.search, net_search='slp')

            self.probeHeadingTextLabel.setText(self.__tr("%1 device(s) found on the %1:").arg(len(devices)).arg(io_str))

        else:
            if self.bus == 'net':
                self.probeHeadingTextLabel.setText(self.__tr("%1 device(s) found on the %1 at address %2:").arg(len(devices)).arg(io_str).arg(param))

            elif self.bus == 'usb':
                self.probeHeadingTextLabel.setText(self.__tr("%1 device(s) found on the %1 at ID %2:").arg(len(devices)).arg(io_str).arg(param))

            elif self.bus == 'par':
                self.probeHeadingTextLabel.setText(self.__tr("%1 device(s) found on the %1 device node ID %2:").arg(len(devices)).arg(io_str).arg(param))

        log.debug(devices)

        if devices:
            row = 0
            for d in devices:
                back_end, is_hp, bus, model, serial, dev_file, host, zc, port = device.parseDeviceURI(d)

                mq = {}
                model_ui = models.normalizeModelUIName(model)

                if self.bus == 'usb':
                    i = DeviceListViewItem(self.probedDevicesListView, d, mq, model_ui, serial, d)

                elif self.bus == 'net':
                    i = DeviceListViewItem(self.probedDevicesListView, d, mq, model_ui, host, devices[d][2], d)

                elif self.bus == 'par':
                    i = DeviceListViewItem(self.probedDevicesListView, d, mq, model_ui, dev_file, d)

                row += 1

            i = self.probedDevicesListView.firstChild()
            self.probedDevicesListView.setCurrentItem(i)
            self.probedDevicesListView.setSelected(i, True)
            item = self.probedDevicesListView.currentItem()
            self.device_uri = item.device_uri
            self.updateModelQuery(item)
            self.setNextEnabled(self.ProbedDevicesPage, True)
            log.debug(self.device_uri)

        else:
            self.setNextEnabled(self.ProbedDevicesPage, False)
            QApplication.restoreOverrideCursor()
            return False

        QApplication.restoreOverrideCursor()
        return True

    def updateModelQuery(self, item):
        if not item.mq:
            item.mq = device.queryModelByURI(self.device_uri)
            self.mq = item.mq
        else:
            self.mq = item.mq

        log.debug(self.mq)

    def probedDevicesListView_currentChanged(self, item):
        self.device_uri = item.device_uri
        self.updateModelQuery(item)
        log.debug(self.device_uri)

    def probeUpdatePushButton_clicked(self):
        self.updateProbedDevicesPage()

    def searchFiltersPushButton_clicked(self):
        if self.settingsDlg():
            self.updateProbedDevicesPage()

    def manualFindPushButton_clicked(self):
        dlg = SetupManualFind(self.bus, self)
        if dlg.exec_loop() == QDialog.Accepted:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            cups_uri, sane_uri, fax_uri = device.makeURI(dlg.param)

            if cups_uri:
                back_end, is_hp, bus, model, serial, dev_file, host, zc, port = device.parseDeviceURI(cups_uri)
                name = ''
                if self.bus == 'net':
                    try:
                        name = socket.gethostbyaddr(host)[0]
                    except socket.herror:
                        name = ''

                QApplication.restoreOverrideCursor()
                self.updateProbedDevicesPage({cups_uri: (model, model, name)}, dlg.param)
            else:
                QApplication.restoreOverrideCursor()
                self.updateProbedDevicesPage([], dlg.param)

    #
    # PPD
    #

    def updatePPDPage(self, ppds=None):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            back_end, is_hp, bus, model, serial, dev_file, host, zc, port = device.parseDeviceURI(self.device_uri)
        except Error:
            self.FailureUI(self.__tr("<b>Device not found or invalid HPLIP device.</b><p>If you specified a USB ID, IP address, or other parameter, please re-check it and try again."))
            self.close()
            sys.exit()

        if ppds is None or not ppds:
            ppds = cups.getSystemPPDs()

        self.ppd = cups.getPPDFile2(self.mq,  model , ppds)
        log.debug(self.ppd)
        self.ppdListView.clear()

        if self.ppd is not None:
            PPDListViewItem(self.ppdListView, self.ppd[0], self.ppd[1])

            self.ppd_file = self.ppd[0]
            log.debug(self.ppd_file)

        else:
            self.FailureUI(self.__tr('<b>PPD not file found.</b><p>An appropriate PPD file could not be found. Please check your HPLIP install, use <i>Select Other...</i>, or download one from linuxprinting.org.'))

        QApplication.restoreOverrideCursor()


    def ppdListView_currentChanged(self,a0):
        self.ppd_file = a0.ppd_file
        log.debug(self.ppd_file)


    def otherPPDPushButton_clicked(self):
        ppd_dir = sys_conf.get('dirs', 'ppd')
        ppd_file = unicode(QFileDialog.getOpenFileName(ppd_dir, "PPD Files (*.ppd *.ppd.gz);;All Files (*)", self, "open file dialog", "Choose a PPD file"))

        if ppd_file and os.path.exists(ppd_file):
            self.updatePPDPage({ppd_file: cups.getPPDDescription(ppd_file)})
        else:
            self.updatePPDPage()

    def ppdDefaultsPushButton_clicked(self):
        self.updatePPDPage()


    #
    # PRINTER/FAX INFORMATION PAGE
    #

    def setDefaultPrinterName(self):
        self.installed_print_devices = device.getSupportedCUPSDevices(['hp'])
        #self.installed_print_devices = device.getSupportedCUPSDevices('*')
        log.debug(self.installed_print_devices)

        self.installed_queues = [p.name for p in cups.getPrinters()]

        back_end, is_hp, bus, model, serial, dev_file, host, zc, port = device.parseDeviceURI(self.device_uri)
        default_model = utils.xstrip(model.replace('series', '').replace('Series', ''), '_')

        printer_name = default_model

        installed_printer_names = device.getSupportedCUPSPrinterNames(['hp'])
        # Check for duplicate names
        if (self.device_uri in self.installed_print_devices and printer_name in self.installed_print_devices[self.device_uri]) \
           or (printer_name in installed_printer_names):
                i = 2
                while True:
                    t = printer_name + "_%d" % i
                    if (t not in installed_printer_names) and (self.device_uri not in self.installed_print_devices or t not in self.installed_print_devices[self.device_uri]):
                        printer_name += "_%d" % i
                        break
                    i += 1

        self.printer_name_ok = True
        self.printerNameLineEdit.setText(printer_name)
        log.debug(printer_name)
        self.printerNameLineEdit.setPaletteBackgroundColor(self.bg)
        self.defaultPrinterNamePushButton.setEnabled(False)
        self.printer_name = printer_name


    def setEditErrors(self):
        if self.printer_name_ok:
            self.printerNameLineEdit.setPaletteBackgroundColor(self.bg)
            self.printer_name_ok = True

            if self.fax_name_ok:
                self.setNextEnabled(self.PrinterNamePage, True)

            QToolTip.remove(self.printerNameLineEdit)

        else:
            self.printerNameLineEdit.setPaletteBackgroundColor(QColor(0xff, 0x99, 0x99))
            self.setNextEnabled(self.PrinterNamePage, False)

        if self.fax_name_ok:
            self.fax_name_ok = True
            self.faxNameLineEdit.setPaletteBackgroundColor(self.bg)

            if self.printer_name_ok:
                self.setNextEnabled(self.PrinterNamePage, True)

            QToolTip.remove(self.faxNameLineEdit)

        else:
            self.faxNameLineEdit.setPaletteBackgroundColor(QColor(0xff, 0x99, 0x99))
            self.setNextEnabled(self.PrinterNamePage, False)


    def printerNameLineEdit_textChanged(self,a0):
        self.printer_name = unicode(a0)
        self.defaultPrinterNamePushButton.setEnabled(True)

        self.printer_name_ok = True

        if not self.printer_name:
            QToolTip.add(self.printerNameLineEdit, self.__tr('You must enter a name for the printer.'))
            self.printer_name_ok = False

        elif self.fax_name == self.printer_name:
            s = self.__tr('The printer name and fax name must be different. Please choose different names.')
            QToolTip.add(self.faxNameLineEdit, s)
            QToolTip.add(self.printerNameLineEdit, s)
            self.fax_name_ok = False
            self.printer_name_ok = False
            self.printer_fax_names_same = True

        elif self.printer_name in self.installed_queues:
            QToolTip.add(self.printerNameLineEdit,
                self.__tr('A printer already exists with this name. Please choose a different name.'))
            self.printer_name_ok = False

        elif self.printer_fax_names_same:
            if self.fax_name != self.printer_name:
                self.printer_fax_names_same = False
                self.printer_name_ok = True

                self.faxNameLineEdit.emit(SIGNAL("textChanged(const QString&)"),
                            (self.faxNameLineEdit.text(),))

        self.setEditErrors()


    def printerLocationLineEdit_textChanged(self, a0):
        self.location = unicode(a0)

    def printerDescriptionLineEdit_textChanged(self,a0):
        self.desc = unicode(a0)

    def faxLocationLineEdit_textChanged(self,a0):
        self.fax_location = unicode(a0)

    def faxDescriptionLineEdit_textChanged(self,a0):
        self.fax_desc = unicode(a0)

    def defaultPrinterNamePushButton_clicked(self):
        self.setDefaultPrinterName()
        self.defaultPrinterNamePushButton.setEnabled(False)

    def setDefaultFaxName(self):
        self.installed_fax_devices = device.getSupportedCUPSDevices(['hpfax'])
        log.debug(self.installed_fax_devices)

        self.fax_uri = self.device_uri.replace('hp:', 'hpfax:')

        back_end, is_hp, bus, model, serial, dev_file, host, zc, port = device.parseDeviceURI(self.fax_uri)
        default_model = utils.xstrip(model.replace('series', '').replace('Series', ''), '_')

        fax_name = default_model + "_fax"
        installed_fax_names = device.getSupportedCUPSPrinterNames(['hpfax'])

        # Check for duplicate names
        if (self.fax_uri in self.installed_fax_devices and fax_name in self.installed_fax_devices[self.fax_uri]) \
           or (fax_name in installed_fax_names):
        #if fax_name in self.installed_queues or fax_name == self.printer_name:
                i = 2
                while True:
                    t = fax_name + "_%d" % i
                    if (t not in installed_fax_names) and (self.fax_uri not in self.installed_fax_devices or t not in self.installed_fax_devices[self.fax_uri]):
                        fax_name += "_%d" % i
                        break
                    i += 1

        self.fax_name_ok = True
        self.faxNameLineEdit.setText(fax_name)
        self.faxNameLineEdit.setPaletteBackgroundColor(self.bg)
        self.defaultFaxNamePushButton.setEnabled(False)
        self.fax_name = fax_name
        #self.fax_name_error = False

    def faxNameLineEdit_textChanged(self, a0):
        self.fax_name = unicode(a0)
        self.defaultFaxNamePushButton.setEnabled(True)

        self.fax_name_ok = True

        if not self.fax_name:
            QToolTip.add(self.faxNameLineEdit, self.__tr('You must enter a fax name.'))
            self.fax_name_ok = False

        elif self.fax_name == self.printer_name:
            s = self.__tr('The printer name and fax name must be different. Please choose different names.')
            QToolTip.add(self.faxNameLineEdit, s)
            QToolTip.add(self.printerNameLineEdit, s)
            self.printer_name_ok = False
            self.fax_name_ok = False
            self.printer_fax_names_same = True

        elif self.fax_name in self.installed_queues:
            QToolTip.add(self.faxNameLineEdit,
                self.__tr('A fax already exists with this name. Please choose a different name.'))
            self.fax_name_ok = False

        elif self.printer_fax_names_same:
            if self.fax_name != self.printer_name:
                self.printer_fax_names_same = False
                self.fax_name_ok = True

                self.printerNameLineEdit.emit(SIGNAL("textChanged(const QString&)"),
                            (self.printerNameLineEdit.text(),))

        self.setEditErrors()


    def faxNumberLineEdit_textChanged(self, a0):
        self.fax_number = unicode(a0)

    def faxNameCoLineEdit_textChanged(self, a0):
        self.fax_name_company = unicode(a0)

    def faxCheckBox_clicked(self):
        pass

    def faxCheckBox_toggled(self, a0):
        self.setup_fax = bool(a0)

        if not self.setup_fax and not self.fax_name_ok:
            self.setDefaultFaxName()

    def printTestPageCheckBox_toggled(self, a0):
        self.print_test_page = bool(a0)

    def defaultFaxNamePushButton_clicked(self):
        self.setDefaultFaxName()
        self.defaultFaxNamePushButton.setEnabled(False)

    def readwriteFaxInformation(self, read=True):
        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            d = fax.getFaxDevice(self.fax_uri, disable_dbus=True)

            while True:
                try:
                    d.open()
                except Error:
                    error_text = self.__tr("Unable to communicate with the device. Please check the device and try again.")
                    log.error(unicode(error_text))
                    if QMessageBox.critical(self,
                                           self.caption(),
                                           error_text,
                                           QMessageBox.Retry | QMessageBox.Default,
                                           QMessageBox.Cancel | QMessageBox.Escape,
                                           QMessageBox.NoButton) == QMessageBox.Cancel:
                        break

                else:
                    try:
                        tries = 0
                        ok = True

                        while True:
                            tries += 1

                            try:
                                if read:
                                    self.fax_number = unicode(d.getPhoneNum())
                                    self.fax_name_company = unicode(d.getStationName())
                                else:
                                    d.setStationName(self.fax_name_company)
                                    d.setPhoneNum(self.fax_number)

                            except Error:
                                error_text = self.__tr("<b>Device I/O Error</b><p>Could not communicate with device. Device may be busy.")
                                log.error(unicode(error_text))

                                if QMessageBox.critical(self,
                                                       self.caption(),
                                                       error_text,
                                                       QMessageBox.Retry | QMessageBox.Default,
                                                       QMessageBox.Cancel | QMessageBox.Escape,
                                                       QMessageBox.NoButton) == QMessageBox.Cancel:
                                    break


                                time.sleep(5)
                                ok = False

                                if tries > 12:
                                    break

                            else:
                                ok = True
                                break

                    finally:
                        d.close()

                    if ok and read:
                        self.faxNumberLineEdit.setText(self.fax_number)
                        self.faxNameCoLineEdit.setText(self.fax_name_company)

                    break

        finally:
            QApplication.restoreOverrideCursor()


    #
    # Updating firmware download for supported devices.
    #
    def flashFirmware(self):
        if self.mq.get('fw-download', False):
            try:
                d = device.Device(self.device_uri)
            except Error , e:
                self.FailureUI(self.__tr("<b>Error opening device. Firmware download is Failed.</b><p>%s (%s)." % (e.msg, e.opt)))
            else:
                if d.downloadFirmware():
                    log.info("Firmware download successful.\n")
                else:
                    self.FailureUI(self.__tr("<b>Firmware download is Failed.</b>"))
                d.close()


    #
    # SETUP PRINTER/FAX
    #

    def setupPrinter(self):
        status = cups.IPP_BAD_REQUEST
        QApplication.setOverrideCursor(QApplication.waitCursor)

        #if self.ppd_file.startswith("foomatic:"):
        if not os.path.exists(self.ppd_file): # assume foomatic: or some such
            add_prnt_args = (self.printer_name.encode('utf8'), self.device_uri,self.location, '', self.ppd_file, self.desc)
        else:
            add_prnt_args = (self.printer_name.encode('utf8'), self.device_uri, self.location, self.ppd_file, '', self.desc)

        status, status_str = cups.cups_operation(cups.addPrinter, GUI_MODE, 'qt3', self, *add_prnt_args)

        log.debug("addPrinter() returned (%d, %s)" % (status, status_str))
        log.debug(device.getSupportedCUPSDevices(['hp']))

        if status != cups.IPP_OK:
            self.FailureUI(self.__tr("<b>Printer queue setup failed.</b><p>Error : %s "%status_str))
        else:
            # sending Event to add this device in hp-systray
            utils.sendEvent(EVENT_CUPS_QUEUES_ADDED,self.device_uri, self.printer_name)

        QApplication.restoreOverrideCursor()
        return status


    def setupFax(self):
        status = cups.IPP_BAD_REQUEST
        QApplication.setOverrideCursor(QApplication.waitCursor)
        back_end, is_hp, bus, model, serial, dev_file, host, zc, port = \
                device.parseDeviceURI(self.device_uri)
        norm_model = models.normalizeModelName(model).lower()
        fax_ppd,fax_ppd_name, nick = cups.getFaxPPDFile(self.mq, norm_model)
        # Fax ppd not found
        if not fax_ppd:
            QApplication.restoreOverrideCursor()
            log.error("Fax PPD file not found.")

            if QMessageBox.warning(self, self.__tr("Unable to find HP fax PPD file."),
                self.__tr("The PPD file (%1.ppd) needed to setup the fax queue was not found.").arg(fax_ppd_name),
                self.__tr("Browse to file..."), # button 0
                self.__tr("Quit") # button 1
                ) == 0: # Browse

                while True:
                    ppd_dir = sys_conf.get('dirs', 'ppd')
                    fax_ppd = unicode(QFileDialog.getOpenFileName(ppd_dir,
                        "HP Fax PPD Files (*.ppd *.ppd.gz);;All Files (*)", self,
                        "open file dialog", "Choose the fax PPD file"))

                    if not fax_ppd: # user hit cancel
                        return

                    if os.path.exists(fax_ppd):
                        n = cups.getPPDDescription(fax_ppd)
                        if n == nick:
                            break
                        else:
                            self.FailureUI(self.__tr("<b>Incorrect fax PPD file.</b><p>The fax PPD file must have a nickname of '%1', not '%1'.").arg(nick).arg(n))
                    else:
                        self.FailureUI(self.__tr("<b>File not found.</b><p>hp-setup cannot find the file %1").arg(fax_ppd))

            else: # Quit
                return

        if not os.path.exists(fax_ppd):
            status, status_str = cups.addPrinter(self.fax_name.encode('utf8'),
                self.fax_uri, self.fax_location, '', fax_ppd,  self.fax_desc)
        else:
            status, status_str = cups.addPrinter(self.fax_name.encode('utf8'),
                self.fax_uri, self.fax_location, fax_ppd, '', self.fax_desc)

        log.debug("addPrinter() returned (%d, %s)" % (status, status_str))
        log.debug(device.getSupportedCUPSDevices(['hpfax']))

        if status != cups.IPP_OK:
            self.FailureUI(self.__tr("<b>Fax queue setup failed.</b><p>Error : %s "%status_str))
        else:
            # sending Event to add this device in hp-systray
            utils.sendEvent(EVENT_CUPS_QUEUES_ADDED,self.fax_uri, self.fax_name)

        QApplication.restoreOverrideCursor()
        return status

    def accept(self):
        if self.print_test_page:
            try:
                d = device.Device(self.device_uri)
            except Error, e:
                self.FailureUI(self.__tr("<b>Device error:</b><p>%s (%s)." % (e.msg, e.opt)))

            else:
                try:
                    d.open()
                except Error:
                    self.FailureUI(self.__tr("<b>Unable to print to printer.</b><p>Please check device and try again."))
                else:
                    if d.isIdleAndNoError():
                        d.close()

                        try:
                            d.printTestPage(self.printer_name)
                        except Error, e:
                            if e.opt == ERROR_NO_CUPS_QUEUE_FOUND_FOR_DEVICE:
                                self.FailureUI(self.__tr("<b>No CUPS queue found for device.</b><p>Please install the printer in CUPS and try again."))
                            else:
                                self.FailureUI(self.__tr("<b>Printer Error</b><p>An error occured: %s (code=%d)." % (e.msg, e.opt)))
                    else:
                        self.FailureUI(self.__tr("<b>Printer Error.</b><p>Printer is busy, offline, or in an error state. Please check the device and try again."))
                        d.close()


        QWizard.accept(self)


    def reject(self):
        QWizard.reject(self)

    def FailureUI(self, error_text):
        log.error(unicode(error_text).replace("<b>", "").replace("</b>", "").replace("<p>", " "))
        QMessageBox.critical(self,
                             self.caption(),
                             error_text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def WarningUI(self, error_text):
        QMessageBox.warning(self,
                             self.caption(),
                             error_text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def __tr(self, s, c=None):
        return qApp.translate("SetupForm", s, c)



class PasswordDialog(QDialog):
    def __init__(self,prompt, parent=None, name=None, modal=0, fl=0):
        QDialog.__init__(self,parent,name,modal,fl)
        self.prompt = prompt

        if not name:
            self.setName("PasswordDialog")

        passwordDlg_baseLayout = QGridLayout(self,1,1,11,6,"passwordDlg_baseLayout")

        self.promptTextLabel = QLabel(self,"promptTextLabel")
        passwordDlg_baseLayout.addMultiCellWidget(self.promptTextLabel,0,0,0,1)

        self.usernameTextLabel = QLabel(self,"usernameTextLabel")
        passwordDlg_baseLayout.addMultiCellWidget(self.usernameTextLabel,1,1,0,1)

        self.usernameLineEdit = QLineEdit(self,"usernameLineEdit")
        self.usernameLineEdit.setEchoMode(QLineEdit.Normal)
        passwordDlg_baseLayout.addMultiCellWidget(self.usernameLineEdit,1,1,1,2)

        self.passwordTextLabel = QLabel(self,"passwordTextLabel")
        passwordDlg_baseLayout.addMultiCellWidget(self.passwordTextLabel,2,2,0,1)

        self.passwordLineEdit = QLineEdit(self,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        passwordDlg_baseLayout.addMultiCellWidget(self.passwordLineEdit,2,2,1,2)

        self.okPushButton = QPushButton(self,"okPushButton")
        passwordDlg_baseLayout.addWidget(self.okPushButton,3,2)

        self.languageChange()

        self.resize(QSize(420,163).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okPushButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.passwordLineEdit,SIGNAL("returnPressed()"),self.accept)

    def setDefaultUsername(self, defUser, allowUsernameEdit = True):
        self.usernameLineEdit.setText(defUser)
        if not allowUsernameEdit:
            self.usernameLineEdit.setReadOnly(True)
            self.usernameLineEdit.setPaletteBackgroundColor(QColor("lightgray"))

    def getUsername(self):
        return unicode(self.usernameLineEdit.text())

    def getPassword(self):
        return unicode(self.passwordLineEdit.text())

    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Enter Username/Password"))
        self.promptTextLabel.setText(self.__tr(self.prompt))
        self.usernameTextLabel.setText(self.__tr("Username"))
        self.passwordTextLabel.setText(self.__tr("Password"))
        self.okPushButton.setText(self.__tr("OK"))

    def __tr(self,s,c = None):
        return qApp.translate("PasswordDialog",s,c)


def showPasswordUI(prompt, userName=None, allowUsernameEdit=True):
    try:
        dlg = PasswordDialog(prompt, None)

        if userName != None:
            dlg.setDefaultUsername(userName, allowUsernameEdit)

        if dlg.exec_loop() == QDialog.Accepted:
            return (dlg.getUsername(), dlg.getPassword())

    finally:
        pass

    return ("", "")


def FailureMessageUI(prompt):
    try:
        dlg = SetupForm("usb", "")
#        dlg = PasswordDialog(prompt, None)
        dlg.FailureUI( prompt)

    finally:
        pass


