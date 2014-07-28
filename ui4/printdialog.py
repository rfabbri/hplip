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
#


# Local
from base.g import *
from base import device, utils
from prnt import cups
from base.codes import *
from ui_utils import *

# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Ui
from printdialog_base import Ui_Dialog
from filetable import FileTable, FILETABLE_TYPE_PRINT
from printernamecombobox import PRINTERNAMECOMBOBOX_TYPE_PRINTER_ONLY

#signal
import signal

PAGE_FILE = 0
PAGE_OPTIONS = 1
PAGE_MAX = 1


class PrintDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, printer_name, args=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.printer_name = printer_name

        # User settings
        self.user_settings = UserSettings()
        self.user_settings.load()
        self.user_settings.debug()

        self.initUi()

        self.file_list = []
        if args is not None:
            for a in args:
                self.Files.addFileFromUI(os.path.abspath(a))

        self.devices = {}


        QTimer.singleShot(0, self.updateFilePage)


    def initUi(self):
        self.OptionsToolBox.include_job_options = True

        # connect signals/slots
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButton_clicked)
        self.connect(self.BackButton, SIGNAL("clicked()"), self.BackButton_clicked)
        self.connect(self.NextButton, SIGNAL("clicked()"), self.NextButton_clicked)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.initFilePage()
        self.initOptionsPage()

        # Application icon
        self.setWindowIcon(QIcon(load_pixmap('hp_logo', '128x128')))

        if self.printer_name:
            self.PrinterName.setInitialPrinter(self.printer_name)

        self.StackedWidget.setCurrentIndex(0)


    #
    # File Page
    #

    def initFilePage(self):
        self.Files.setType(FILETABLE_TYPE_PRINT)
        #self.Files.setWorkingDir(user_conf.workingDirectory())
        self.Files.setWorkingDir(self.user_settings.working_dir)
        self.connect(self.Files, SIGNAL("isEmpty"), self.Files_isEmpty)
        self.connect(self.Files, SIGNAL("isNotEmpty"), self.Files_isNotEmpty)


    def updateFilePage(self):
        self.NextButton.setText(self.__tr("Next >"))
        self.NextButton.setEnabled(self.Files.isNotEmpty())
        self.BackButton.setEnabled(False)
        self.updateStepText(PAGE_FILE)
        self.Files.updateUi()

    def Files_isEmpty(self):
        self.NextButton.setEnabled(False)


    def Files_isNotEmpty(self):
        self.NextButton.setEnabled(True)


    #
    # Options Page
    #

    def initOptionsPage(self):
        self.BackButton.setEnabled(True)
        self.PrinterName.setType(PRINTERNAMECOMBOBOX_TYPE_PRINTER_ONLY)

        self.connect(self.PrinterName, SIGNAL("PrinterNameComboBox_currentChanged"),
            self.PrinterNameComboBox_currentChanged)

        self.connect(self.PrinterName, SIGNAL("PrinterNameComboBox_noPrinters"),
            self.PrinterNameComboBox_noPrinters)


    def updateOptionsPage(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            self.PrinterName.updateUi()
            self.BackButton.setEnabled(True)
            num_files = len(self.Files.file_list)

            if  num_files > 1:
                self.NextButton.setText(self.__tr("Print %1 Files").arg(num_files))
            else:
                self.NextButton.setText(self.__tr("Print File"))

            self.updateStepText(PAGE_OPTIONS)
            # TODO: Enable print button only if printer is accepting and all options are OK (esp. page range)
        finally:
            QApplication.restoreOverrideCursor()


    def PrinterNameComboBox_currentChanged(self, device_uri, printer_name):
        try:
            self.devices[device_uri]
        except KeyError:
            self.devices[device_uri] = device.Device(device_uri)

        self.OptionsToolBox.updateUi(self.devices[device_uri], printer_name)


    def PrinterNameComboBox_noPrinters(self):
        FailureUI(self, self.__tr("<b>No printers found.</b><p>Please setup a printer and try again."))
        self.close()


    #
    # Print
    #

    def executePrint(self):
        for cmd in self.OptionsToolBox.getPrintCommands(self.Files.file_list):
            log.debug(cmd)
            status, output = utils.run(cmd)
            if status != 0:
                FailureUI(self, self.__tr("<b>Print command failed with status code %1.</b><p>%2</p>").arg(status).arg(cmd))

        self.close()
        #print file('/home/dwelch/.cups/lpoptions', 'r').read()

    #
    # Misc
    #

    def CancelButton_clicked(self):
        self.close()


    def BackButton_clicked(self):
        p = self.StackedWidget.currentIndex()
        if p == PAGE_OPTIONS:
            self.StackedWidget.setCurrentIndex(PAGE_FILE)
            self.updateFilePage()

        else:
            log.error("Invalid page!") # shouldn't happen!


    def NextButton_clicked(self):
        p = self.StackedWidget.currentIndex()
        if p == PAGE_FILE:
            self.StackedWidget.setCurrentIndex(PAGE_OPTIONS)
            self.updateOptionsPage()

        elif p == PAGE_OPTIONS:
            self.executePrint()


    def updateStepText(self, p):
        self.StepText.setText(self.__tr("Step %1 of %2").arg(p+1).arg(PAGE_MAX+1))


    def __tr(self,s,c = None):
        return qApp.translate("PrintDialog",s,c)



"""
   def printButton_clicked(self):
        if self.invalid_page_range:
            self.form.FailureUI(self.__tr("<b>Cannot print: Invalid page range: %1</b><p>A valid page range is a list of pages or ranges of pages separated by commas (e.g., 1-2,4,6-7)").arg(self.pageRangeEdit.text()))
            return

        try:
            try:
                self.cur_device.open()
            except Error:
                self.form.FailureUI(self.__tr("<b>Cannot print: Device is busy or not available.</b><p>Please check device and try again."))
                return

            if 1: # Go ahead and allow - print will be queued in CUPS if not rejecting
                printers = cups.getPrinters()
                for p in printers:
                    if p.name == self.cur_printer:
                        break

                if p.state == cups.IPP_PRINTER_STATE_STOPPED:
                    self.form.FailureUI(self.__tr("<b>Cannot print: Printer is stopped.</b><p>Please START the printer to continue this print. Job will begin printing once printer is started."))

                if not p.accepting:
                    self.form.FailureUI(self.__tr("<b>Cannot print: Printer is not accepting jobs.</b><p>Please set the printer to ACCEPTING JOBS to continue printing."))
                    return

                copies = int(self.copiesSpinBox.value())
                all_pages = self.pages_button_group == 0
                page_range = unicode(self.pageRangeEdit.text())
                page_set = int(self.pageSetComboBox.currentItem())

                cups.resetOptions()
                cups.openPPD(self.cur_printer)
                current_options = dict(cups.getOptions())
                cups.closePPD()

                nup = int(current_options.get("number-up", 1))

                for p, t, d in self.file_list:

                    alt_nup = (nup > 1 and t == 'application/postscript' and utils.which('psnup'))

                    if utils.which('lpr'):
                        if alt_nup:
                            cmd = ' '.join(['psnup', '-%d' % nup, ''.join(['"', p, '"']), '| lpr -P', self.cur_printer])
                        else:
                            cmd = ' '.join(['lpr -P', self.cur_printer])

                        if copies > 1:
                            cmd = ' '.join([cmd, '-#%d' % copies])

                    else:
                        if alt_nup:
                            cmd = ' '.join(['psnup', '-%d' % nup, ''.join(['"', p, '"']), '| lp -c -d', self.cur_printer])
                        else:
                            cmd = ' '.join(['lp -c -d', self.cur_printer])

                        if copies > 1:
                            cmd = ' '.join([cmd, '-n%d' % copies])


                    if not all_pages and len(page_range) > 0:
                        cmd = ' '.join([cmd, '-o page-ranges=%s' % page_range])

                    if page_set > 0:
                        if page_set == 1:
                            cmd = ' '.join([cmd, '-o page-set=even'])
                        else:
                            cmd = ' '.join([cmd, '-o page-set=odd'])


                    # Job Storage
                    # self.job_storage_mode = (0=Off, 1=P&H, 2=PJ, 3=QC, 4=SJ)
                    # self.job_storage_pin = u"" (dddd)
                    # self.job_storage_use_pin = True|False
                    # self.job_storage_username = u""
                    # self.job_storage_auto_username = True|False
                    # self.job_storage_jobname = u""
                    # self.job_storage_auto_jobname = True|False
                    # self.job_storage_job_exist = (0=replace, 1=job name+(1-99))

                    if self.job_storage_avail:
                        if self.job_storage_mode: # On

                            if self.job_storage_mode == 1: # Proof and Hold
                                cmd = ' '.join([cmd, '-o HOLD=PROOF'])

                            elif self.job_storage_mode == 2: # Private Job
                                if self.job_storage_use_pin:
                                    cmd = ' '.join([cmd, '-o HOLD=ON'])
                                    cmd = ' '.join([cmd, '-o HOLDTYPE=PRIVATE'])
                                    cmd = ' '.join([cmd, '-o HOLDKEY=%s' % self.job_storage_pin.encode('ascii')])
                                else:
                                    cmd = ' '.join([cmd, '-o HOLD=PROOF'])
                                    cmd = ' '.join([cmd, '-o HOLDTYPE=PRIVATE'])

                            elif self.job_storage_mode == 3: # Quick Copy
                                cmd = ' '.join([cmd, '-o HOLD=ON'])
                                cmd = ' '.join([cmd, '-o HOLDTYPE=PUBLIC'])

                            elif self.job_storage_mode == 4: # Store Job
                                if self.job_storage_use_pin:
                                    cmd = ' '.join([cmd, '-o HOLD=STORE'])
                                    cmd = ' '.join([cmd, '-o HOLDTYPE=PRIVATE'])
                                    cmd = ' '.join([cmd, '-o HOLDKEY=%s' % self.job_storage_pin.encode('ascii')])
                                else:
                                    cmd = ' '.join([cmd, '-o HOLD=STORE'])

                            cmd = ' '.join([cmd, '-o USERNAME=%s' % self.job_storage_username.encode('ascii')\
                                .replace(" ", "_")])

                            cmd = ' '.join([cmd, '-o JOBNAME=%s' % self.job_storage_jobname.encode('ascii')\
                                .replace(" ", "_")])

                            if self.job_storage_job_exist == 1:
                                cmd = ' '.join([cmd, '-o DUPLICATEJOB=APPEND'])
                            else:
                                cmd = ' '.join([cmd, '-o DUPLICATEJOB=REPLACE'])

                        else: # Off
                            cmd = ' '.join([cmd, '-o HOLD=OFF'])


                    if not alt_nup:
                        cmd = ''.join([cmd, ' "', p, '"'])

                    log.debug("Printing: %s" % cmd)

                    code = os.system(cmd)
                    if code != 0:
                        log.error("Print command failed.")
                        self.form.FailureUI(self.__tr("Print command failed with error code %1").arg(code))

                self.form.close()

        finally:
            self.cur_device.close()

"""
