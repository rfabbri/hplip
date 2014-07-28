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
# Author: Don Welch
#

# Local
from base.g import *
from base import utils, magic, pml, os_utils
from prnt import cups
from ui_utils import load_pixmap

# Qt
from qt import *
from scrollview import ScrollView, PixmapLabelButton
from allowabletypesdlg import AllowableTypesDlg
from waitform import WaitForm

# Std Lib
import os.path, os
import struct, Queue, time


fax_enabled = prop.fax_build

if fax_enabled:
    try:
        from fax import fax
    except ImportError:
        # This can fail on Python < 2.3 due to the datetime module
        # or if fax was diabled during the build
        log.warn("Fax send disabled - Python 2.3+ required.")
        fax_enabled = False


coverpages_enabled = False
if fax_enabled:
    try:
        import reportlab
        ver = reportlab.Version
        try:
            ver_f = float(ver)
        except ValueError:
            ver_f = 0.0

        if ver_f >= 2.0:
            coverpages_enabled = True
        else:
            log.warn("Pre-2.0 version of Reportlab installed. Fax coverpages disabled.")

    except ImportError:
        log.warn("Reportlab not installed. Fax coverpages disabled.")


if not coverpages_enabled:
    log.warn("Please install version 2.0+ of Reportlab for coverpage support.")

if fax_enabled and coverpages_enabled:
    from fax import coverpages
    from coverpageform import CoverpageForm


# Used to store MIME types for files
# added directly in interface.
job_types = {} # { job_id : "mime_type", ...}

class FileListViewItem(QListViewItem):
    def __init__(self, parent, order, title, mime_type_desc, str_pages, path):
        QListViewItem.__init__(self, parent, order, title, mime_type_desc, str_pages, path)
        self.path = path


class RecipientListViewItem(QListViewItem):
    def __init__(self, parent, order, name, fax, notes):
        QListViewItem.__init__(self, parent, order, name, fax, notes)
        self.name = name
        #self.entry = entry


class PhoneNumValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)
        if not input:
            return QValidator.Acceptable, pos
        elif input[pos-1] not in u'0123456789-(+) *#':
            return QValidator.Invalid, pos
        elif len(input) > 50:
            return QValidator.Invalid, pos
        else:
            return QValidator.Acceptable, pos



class ScrollFaxView(ScrollView):
    def __init__(self, service, parent = None, form=None, name = None,fl = 0):
        ScrollView.__init__(self, service, parent, name, fl)

        global fax_enabled
        if service is None:
            fax_enabled = False

        self.form = form
        self.file_list = []
        self.pages_button_group = 0
        self.recipient_list = []
        self.username = prop.username
        self.busy = False
        self.allowable_mime_types = cups.getAllowableMIMETypes()
        self.cover_page_func, cover_page_png = None, None
        self.cover_page_message = ''
        self.cover_page_re = ''
        self.cover_page_name = ''
        self.update_queue = Queue.Queue() # UI updates from send thread
        self.event_queue = Queue.Queue() # UI events (cancel) to send thread
        self.prev_selected_file_path = ''
        self.prev_selected_recipient = ''
        self.preserve_formatting = False
        self.waitdlg = None
        log.debug(self.allowable_mime_types)
        self.last_job_id = 0
        self.dev = None
        self.lock_file = None


        self.db =  fax.FaxAddressBook()
        self.last_db_modification = self.db.last_modification_time()

        self.MIME_TYPES_DESC = \
        {
            "application/pdf" : (self.__tr("PDF Document"), '.pdf'),
            "application/postscript" : (self.__tr("Postscript Document"), '.ps'),
            "application/vnd.hp-HPGL" : (self.__tr("HP Graphics Language File"), '.hgl, .hpg, .plt, .prn'),
            "application/x-cshell" : (self.__tr("C Shell Script"), '.csh, .sh'),
            "application/x-csource" : (self.__tr("C Source Code"), '.c'),
            "text/cpp": (self.__tr("C++ Source Code"), '.cpp, .cxx'),
            "application/x-perl" : (self.__tr("Perl Script"), '.pl'),
            "application/x-python" : (self.__tr("Python Program"), '.py'),
            "application/x-shell" : (self.__tr("Shell Script"), '.sh'),
            "application/x-sh" : (self.__tr("Shell Script"), '.sh'),
            "text/plain" : (self.__tr("Plain Text"), '.txt, .log, etc'),
            "text/html" : (self.__tr("HTML Dcoument"), '.htm, .html'),
            "image/gif" : (self.__tr("GIF Image"), '.gif'),
            "image/png" : (self.__tr("PNG Image"), '.png'),
            "image/jpeg" : (self.__tr("JPEG Image"), '.jpg, .jpeg'),
            "image/tiff" : (self.__tr("TIFF Image"), '.tif, .tiff'),
            "image/x-bitmap" : (self.__tr("Bitmap (BMP) Image"), '.bmp'),
            "image/x-bmp" : (self.__tr("Bitmap (BMP) Image"), '.bmp'),
            "image/x-photocd" : (self.__tr("Photo CD Image"), '.pcd'),
            "image/x-portable-anymap" : (self.__tr("Portable Image (PNM)"), '.pnm'),
            "image/x-portable-bitmap" : (self.__tr("Portable B&W Image (PBM)"), '.pbm'),
            "image/x-portable-graymap" : (self.__tr("Portable Grayscale Image (PGM)"), '.pgm'),
            "image/x-portable-pixmap" : (self.__tr("Portable Color Image (PPM)"), '.ppm'),
            "image/x-sgi-rgb" : (self.__tr("SGI RGB"), '.rgb'),
            "image/x-xbitmap" : (self.__tr("X11 Bitmap (XBM)"), '.xbm'),
            "image/x-xpixmap" : (self.__tr("X11 Pixmap (XPM)"), '.xpm'),
            "image/x-sun-raster" : (self.__tr("Sun Raster Format"), '.ras'),
        }


        user_settings = utils.UserSettings()
        self.cmd_fab = user_settings.cmd_fab
        log.debug("FAB command: %s" % self.cmd_fab)

        if fax_enabled:
            self.check_timer = QTimer(self, "CheckTimer")
            self.connect(self.check_timer, SIGNAL('timeout()'), self.PeriodicCheck)
            self.check_timer.start(3000)


    def fillControls(self):
        ScrollView.fillControls(self)

        if fax_enabled:
            if self.addPrinterFaxList(): #faxes=True, printers=False):

                self.addGroupHeading("files_to_fax", self.__tr("File(s) to Fax"))
                self.addFileList()

                if coverpages_enabled:
                    self.addGroupHeading("coverpage", self.__tr("Add/Edit Fax Coverpage"))
                    self.addCoverpage()

                self.addGroupHeading("recipients", self.__tr("Recipient(s)"))

                self.addRecipientList()

                self.addGroupHeading("recipient_add_from_fab", self.__tr("Add Recipients from the Fax Address Book"))

                self.addRecipientAddFromFAB()

                self.addGroupHeading("recipient_quick_add", self.__tr("<i>Quick Add</i> an Individual Recipient"))

                self.addRecipientQuickAdd()

                self.addGroupHeading("space1", "")

                self.faxButton = self.addActionButton("bottom_nav", self.__tr("Send Fax Now"),
                                        self.faxButton_clicked, 'fax.png', 'fax.png',
                                        self.__tr("Close"), self.funcButton_clicked)

                self.faxButton.setEnabled(False)

                self.updateRecipientCombos()

                self.maximizeControl()

            else:
                QApplication.restoreOverrideCursor()
                self.form.FailureUI("<b>Fax is disabled.</b><p>No CUPS fax queue found for this device.")
                self.funcButton_clicked()

        else:
            QApplication.restoreOverrideCursor()
            self.form.FailureUI("<b>Fax is disabled.</b><p>Python version 2.3 or greater required or fax was disabled during build.")
            self.funcButton_clicked()



    def onUpdate(self, cur_device=None):
        log.debug("ScrollPrintView.onUpdate()")
        self.updateFileList()
        self.updateRecipientList()


    def PeriodicCheck(self): # called by check_timer every 3 sec
        #print self
        if not self.busy:
            log.debug("Checking for incoming faxes...")

            result = list(self.service.CheckForWaitingFax(self.cur_device.device_uri,
                          prop.username, self.last_job_id))

            fax_file = str(result[7])

            if fax_file:
                self.last_job_id = 0
                log.debug("A new fax has arrived: %s" % fax_file)
                job_id = int(result[4])
                title = str(result[5])

                if self.form.isMinimized():
                    self.form.showNormal()

                self.check_timer.stop()
                self.addFileFromJob(0, title, prop.username, job_id, fax_file)
                self.check_timer.start(3000)
                return

            log.debug("Not found.")

            # Check for updated FAB
            last_db_modification = self.db.last_modification_time()

            if last_db_modification > self.last_db_modification:
                QApplication.setOverrideCursor(QApplication.waitCursor)
                log.debug("FAB has been modified. Re-reading...")
                self.last_db_modification = last_db_modification
                self.updateRecipientCombos()
                QApplication.restoreOverrideCursor()


    def onPrinterChange(self, printer_name):
        if printer_name != self.cur_printer:
            self.unlock()
            self.lock(printer_name)
            #utils.unlock(self.lock_file)
            #ok, self.lock_file = utils.lock_app('hp-sendfax-%s' % printer_name, True)

        ScrollView.onPrinterChange(self, printer_name)

    def unlock(self):
        utils.unlock(self.lock_file)

    def lock(self, printer_name=None):
        if printer_name is None:
            printer_name = self.cur_printer

        ok, self.lock_file = utils.lock_app('hp-sendfax-%s' % printer_name, True)



    # Event handler for adding files from a external print job (not during fax send thread)
    def addFileFromJob(self, event, title, username, job_id, fax_file):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        self.busy = True

        try:
            f = file(fax_file, 'r')
            header = f.read(fax.FILE_HEADER_SIZE)

            if len(header) != fax.FILE_HEADER_SIZE:
                log.error("Invalid fax file! (truncated header or no data)")
                sys.exit(1)

            mg, version, total_pages, hort_dpi, vert_dpi, page_size, \
                resolution, encoding, reserved1, reserved2 = \
                struct.unpack(">8sBIHHBBBII", header[:fax.FILE_HEADER_SIZE])

            log.debug("Magic=%s Ver=%d Pages=%d hDPI=%d vDPI=%d Size=%d Res=%d Enc=%d" %
                      (mg, version, total_pages, hort_dpi, vert_dpi, page_size, resolution, encoding))

            if total_pages > 0:
                mime_type = job_types.get(job_id, "application/hplip-fax")
                mime_type_desc = self.MIME_TYPES_DESC.get(mime_type, ('Unknown', 'n/a'))[0]
                log.debug("%s (%s)" % (mime_type, mime_type_desc))
                self.file_list.append((fax_file, mime_type, mime_type_desc, title, total_pages))
                self.prev_selected_file_path = fax_file
            else:
                self.form.FailureUI("<b>Render Failure:</b><p>Rendered document contains no data.")

            self.updateFileList()

        finally:
            self.busy = False

            if self.waitdlg is not None:
                self.waitdlg.hide()
                self.waitdlg.close()
                self.waitdlg = None

            QApplication.restoreOverrideCursor()


    def add_fax_canceled(self):
            pass

    #
    # FILE LIST
    #

    def addFileList(self):
        widget = self.getWidget()

        layout37 = QGridLayout(widget,1,1,5,10,"layout37")

        self.addFilePushButton = PixmapLabelButton(widget, "list_add.png",
            "list_add.png", name='addFilePushButton')

        layout37.addWidget(self.addFilePushButton,2,0)

        self.removeFilePushButton = PixmapLabelButton(widget,
            "list_remove.png", "list_remove.png", name='removeFilePushButton')

        layout37.addWidget(self.removeFilePushButton,2,1)

        self.moveFileUpPushButton = PixmapLabelButton(widget, "up.png",
            "up.png", name='moveFileUpPushButton')

        layout37.addWidget(self.moveFileUpPushButton,2,2)

        self.moveFileDownPushButton = PixmapLabelButton(widget, "down.png",
            "down.png", name='moveFileDownPushButton')

        layout37.addWidget(self.moveFileDownPushButton,2,3)

        self.showTypesPushButton = PixmapLabelButton(widget, "mimetypes.png",
            None, name='showTypesPushButton')

        layout37.addWidget(self.showTypesPushButton,2,5)


        self.fileListView = QListView(widget,"fileListView")
        self.fileListView.addColumn(self.__tr("Order"))
        self.fileListView.addColumn(self.__tr("Name"))
        self.fileListView.addColumn(self.__tr("Type"))
        self.fileListView.addColumn(self.__tr("Pages"))
        self.fileListView.addColumn(self.__tr("Path"))
        self.fileListView.setAllColumnsShowFocus(1)
        self.fileListView.setShowSortIndicator(1)
        self.fileListView.setColumnWidth(0, 100) # Order
        self.fileListView.setColumnWidth(1, 150) # Name
        self.fileListView.setColumnWidth(2, 100) # Type
        self.fileListView.setColumnWidth(3, 100) # Pages
        self.fileListView.setColumnWidth(4, 300) # Path
        self.fileListView.setItemMargin(2)
        self.fileListView.setSorting(-1)

        layout37.addMultiCellWidget(self.fileListView,1,1,0,5)

        spacer26 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout37.addItem(spacer26,2,4)

        self.addFilePushButton.setText(self.__tr("Add File..."))
        self.showTypesPushButton.setText(self.__tr("Show Types..."))
        self.removeFilePushButton.setText(self.__tr("Remove File"))
        self.moveFileDownPushButton.setText(self.__tr("Move Down"))
        self.moveFileUpPushButton.setText(self.__tr("Move Up"))

        self.removeFilePushButton.setEnabled(False)
        self.moveFileDownPushButton.setEnabled(False)
        self.moveFileUpPushButton.setEnabled(False)
        self.connect(self.addFilePushButton, SIGNAL("clicked()"), self.addFile_clicked)
        self.connect(self.removeFilePushButton, SIGNAL("clicked()"), self.removeFile_clicked)
        self.connect(self.showTypesPushButton, SIGNAL("clicked()"), self.showFileTypes_clicked)

        self.connect(self.moveFileUpPushButton, SIGNAL("clicked()"), self.moveFileUp_clicked)
        self.connect(self.moveFileDownPushButton, SIGNAL("clicked()"), self.moveFileDown_clicked)

        self.connect(self.fileListView,SIGNAL("rightButtonClicked(QListViewItem*,const QPoint&, int)"),self.fileListView_rightButtonClicked)

        self.connect(self.fileListView, SIGNAL("selectionChanged(QListViewItem*)"), self.fileListView_selectionChanged)

        self.addWidget(widget, "file_list", maximize=True)

    def fileListView_selectionChanged(self, i):
        try:
            self.prev_selected_file_path = i.path
        except AttributeError:
            pass
        else:
            flv = self.fileListView
            selected_item = flv.selectedItem()
            file_count = flv.childCount()
            last_item = flv.firstChild()
            while last_item.nextSibling():
                last_item = last_item.nextSibling()

            self.moveFileDownPushButton.setEnabled(file_count > 1 and selected_item is not last_item)
            self.moveFileUpPushButton.setEnabled(file_count > 1 and selected_item is not flv.firstChild())


    def moveFileUp_clicked(self):
        try:
            path = self.fileListView.selectedItem().path
        except AttributeError:
            return
        else:
            for i in range(1, len(self.file_list)):
                if self.file_list[i][0] == path:
                    self.file_list[i-1],self.file_list[i] = self.file_list[i], self.file_list[i-1]

            self.updateFileList()

    def moveFileDown_clicked(self):
        try:
            path = self.fileListView.selectedItem().path
        except AttributeError:
            return
        else:
            for i in range(len(self.file_list) - 2, -1, -1):
                if self.file_list[i][0] == path:
                    self.file_list[i], self.file_list[i+1] = self.file_list[i+1], self.file_list[i]

            self.updateFileList()


    def fileListView_rightButtonClicked(self, item, pos, col):
        popup = QPopupMenu(self)

        popup.insertItem(QIconSet(load_pixmap('list_add', '16x16')),
            self.__tr("Add File..."), self.addFile_clicked)

        if item is not None:
            popup.insertItem(QIconSet(load_pixmap('list_remove', '16x16')),
                self.__tr("Remove File"), self.removeFile_clicked)

            if self.fileListView.childCount() > 1:
                last_item = self.fileListView.firstChild()
                while last_item is not None and last_item.nextSibling():
                    last_item = last_item.nextSibling()

                if item is not self.fileListView.firstChild():
                    popup.insertItem(QIconSet(load_pixmap('up', '16x16')),
                        self.__tr("Move Up"), self.moveFileUp_clicked)

                if item is not last_item:
                    popup.insertItem(QIconSet(load_pixmap('down', '16x16')),
                        self.__tr("Move Down"), self.moveFileDown_clicked)


        popup.insertSeparator(-1)
        popup.insertItem(QIconSet(load_pixmap('mimetypes', '16x16')),
            self.__tr("Show File Types..."), self.showFileTypes_clicked)

        popup.popup(pos)


    def addFile(self, path, title, mime_type, mime_type_desc, pages):
        self.file_list.append((path, mime_type, mime_type_desc, title, pages))
        self.prev_selected_file_path = path

        self.updateFileList()

    def processFile(self, path, title=''): # Process an arbitrary file ("Add file...")
        path = os.path.realpath(path)
        if not title:
            title = os.path.basename(path)

        if os.path.exists(path) and os.access(path, os.R_OK):
            mime_type = magic.mime_type(path)
            mime_type_desc = mime_type

            if mime_type == 'application/hplip-fax':
                mime_type_desc = self.MIME_TYPES_DESC[mime_type][0]

                fax_file_fd = file(path, 'r')
                header = fax_file_fd.read(fax.FILE_HEADER_SIZE)

                mg, version, pages, hort_dpi, vert_dpi, page_size, \
                    resolution, encoding, reserved1, reserved2 = self.decode_fax_header(header)

                if mg != 'hplip_g3':
                    log.error("Invalid file header. Bad magic.")
                    self.form.WarningUI(self.__tr("<b>Invalid HPLIP Fax file.</b><p>Bad magic!"))
                    return

                self.addFile(path, title, mime_type, mime_type_desc, pages)

            else:
                log.debug(repr(mime_type))
                try:
                    mime_type_desc = self.MIME_TYPES_DESC[mime_type][0]
                except KeyError:
                    self.form.WarningUI(self.__tr("<b>You are trying to add a file that cannot be directly faxed with this utility.</b><p>To print this file, use the print command in the application that created it."))
                    return
                else:
                    log.debug("Adding file: title='%s' file=%s mime_type=%s mime_desc=%s)" % (title, path, mime_type, mime_type_desc))

                    all_pages = True
                    page_range = ''
                    page_set = 0
                    #nup = 1

                    cups.resetOptions()

                    self.cups_printers = cups.getPrinters()

                    printer_state = cups.IPP_PRINTER_STATE_STOPPED
                    for p in self.cups_printers:
                        if p.name == self.cur_printer:
                            printer_state = p.state

                    log.debug("Printer state = %d" % printer_state)

                    if printer_state == cups.IPP_PRINTER_STATE_IDLE:
                        log.debug("Printing: %s on %s" % (path, self.cur_printer))
                        sent_job_id = cups.printFile(self.cur_printer, path, os.path.basename(path))
                        self.last_job_id = sent_job_id
                        job_types[sent_job_id] = mime_type # save for later
                        log.debug("Job ID=%d" % sent_job_id)

                        QApplication.setOverrideCursor(QApplication.waitCursor)

                        self.waitdlg = WaitForm(0, self.__tr("Processing fax file..."), None, self, modal=1) # self.add_fax_canceled
                        self.waitdlg.show()

                    else:
                        self.form.FailureUI(self.__tr("<b>Printer '%1' is in a stopped or error state.</b><p>Check the printer queue in CUPS and try again.").arg(self.cur_printer))
                        cups.resetOptions()
                        return

                    cups.resetOptions()
                    QApplication.restoreOverrideCursor()

        else:
            self.form.FailureUI(self.__tr("<b>Unable to add file '%1' to file list (file not found or insufficient permissions).</b><p>Check the file name and try again.").arg(path))



    def updateFileList(self):
        self.fileListView.clear()
        temp = self.file_list[:]
        temp.reverse()
        order = len(temp)
        last_item = None
        selected_item = None

        for path, mime_type, mime_type_desc, title, pages in temp:
            i = FileListViewItem(self.fileListView, str(order), title, mime_type_desc, str(pages), path)

            if not self.prev_selected_file_path or self.prev_selected_file_path == path:
                self.fileListView.setSelected(i, True)
                selected_item = i
                self.prev_selected_file_path = path

            order -= 1

        last_item = self.fileListView.firstChild()
        while last_item is not None and last_item.nextSibling():
            last_item = last_item.nextSibling()

        file_count = self.fileListView.childCount()
        self.moveFileDownPushButton.setEnabled(file_count > 1 and selected_item is not last_item)
        self.moveFileUpPushButton.setEnabled(file_count > 1 and selected_item is not self.fileListView.firstChild())
        self.checkSendFaxButton()
        self.removeFilePushButton.setEnabled(file_count > 0)



    def addFile_clicked(self):
        dlg = QFileDialog(user_conf.workingDirectory(), QString.null, None, None, True)

        dlg.setCaption("openfile")
        dlg.setMode(QFileDialog.ExistingFile)
        dlg.show()

        if dlg.exec_loop() == QDialog.Accepted:
                results = dlg.selectedFile()
                working_directory = unicode(dlg.dir().absPath())
                log.debug("results: %s" % results)
                user_conf.setWorkingDirectory(working_directory)

                if results:
                    path = unicode(results)
                    self.processFile(path)


    def removeFile_clicked(self):
        try:
            path = self.fileListView.selectedItem().path
        except AttributeError:
            return
        else:
            temp = self.file_list[:]
            index = 0
            for p, t, d, x, g in temp:
                if p == path:
                    del self.file_list[index]

                    if t == 'application/hplip-fax-coverpage':
                        self.addCoverpagePushButton.setEnabled(coverpages_enabled)
                        self.editCoverpagePushButton.setEnabled(False)

                    self.prev_selected_file_path = ''
                    self.updateFileList()
                    break

                index += 1


    def showFileTypes_clicked(self):
        x = {}
        for a in self.allowable_mime_types:
            x[a] = self.MIME_TYPES_DESC.get(a, ('Unknown', 'n/a'))

        log.debug(x)
        dlg = AllowableTypesDlg(x, self)
        dlg.exec_loop()


    #
    # COVERPAGE
    #

    def addCoverpage(self):
        widget = self.getWidget()

        layout14 = QGridLayout(widget,1,1,5,10,"layout14")

        self.editCoverpagePushButton = PixmapLabelButton(widget,
            "edit.png", "edit.png", name='')

        layout14.addWidget(self.editCoverpagePushButton,0,1)

        self.addCoverpagePushButton = PixmapLabelButton(widget,
            "list_add.png", "list_add.png", name='')

        layout14.addWidget(self.addCoverpagePushButton,0,2)
        spacer12_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout14.addItem(spacer12_2,0,0)

        self.editCoverpagePushButton.setText(self.__tr("Edit..."))
        self.editCoverpagePushButton.setEnabled(False)

        self.addCoverpagePushButton.setText(self.__tr("Add..."))

        self.connect(self.editCoverpagePushButton,SIGNAL("clicked()"),self.editCoverpagePushButton_clicked)
        self.connect(self.addCoverpagePushButton,SIGNAL("clicked()"),self.addCoverpagePushButton_clicked)

        self.addWidget(widget, "coverpage")

    def editCoverpagePushButton_clicked(self):
        self.showCoverPageDlg()

    def addCoverpagePushButton_clicked(self):
        if self.showCoverPageDlg():
            self.file_list.insert(0, ('n/a', "application/hplip-fax-coverpage",
                self.__tr("HP Fax Coverpage"), self.__tr("Cover Page"), 1))

            self.updateFileList()
            self.addCoverpagePushButton.setEnabled(False)
            self.editCoverpagePushButton.setEnabled(True)

    def showCoverPageDlg(self):
        dlg = CoverpageForm(self.cover_page_name, self.preserve_formatting, parent=self)
        dlg.messageTextEdit.setText(self.cover_page_message)
        dlg.regardingTextEdit.setText(self.cover_page_re)

        if dlg.exec_loop() == QDialog.Accepted:

            self.cover_page_func, cover_page_png = dlg.data
            self.cover_page_message = unicode(dlg.messageTextEdit.text())
            self.cover_page_re = unicode(dlg.regardingTextEdit.text())
            self.cover_page_name = dlg.coverpage_name
            self.preserve_formatting = dlg.preserve_formatting
            return True

        return False



    #
    # RECIPIENT LIST
    #

    def addRecipientList(self):
        widget = self.getWidget()

        layout9 = QGridLayout(widget,1,1,5,10,"layout9")

        self.moveDownPushButton = PixmapLabelButton(widget,
            "down_user.png", "down_user.png", name='')

        layout9.addWidget(self.moveDownPushButton,1,2)

        self.recipientListView = QListView(widget,"recipientListView")
        self.recipientListView.addColumn(self.__tr("Order"))
        self.recipientListView.addColumn(self.__tr("Name"))
        self.recipientListView.addColumn(self.__tr("Fax Number"))
        self.recipientListView.addColumn(self.__tr("Notes"))

        self.recipientListView.setAllColumnsShowFocus(1)
        self.recipientListView.setShowSortIndicator(1)
        self.recipientListView.setColumnWidth(0, 100) # Order
        self.recipientListView.setColumnWidth(1, 150) # Name
        self.recipientListView.setColumnWidth(2, 200) # Fax Number
        self.recipientListView.setColumnWidth(3, 250) # Notes
        self.recipientListView.setItemMargin(2)
        self.recipientListView.setSorting(-1)

        widget.setMaximumHeight(250)

        layout9.addMultiCellWidget(self.recipientListView,0,0,0,4)

        self.fabPushButton = PixmapLabelButton(widget,
                    "fab", None, name='')

        layout9.addWidget(self.fabPushButton,1,4)

        self.removeRecipientPushButton = PixmapLabelButton(widget,
            "remove_user.png", "remove_user.png", name='')

        self.removeRecipientPushButton.setEnabled(1)

        layout9.addWidget(self.removeRecipientPushButton,1,0)
        spacer10 = QSpacerItem(20,20,QSizePolicy.MinimumExpanding,QSizePolicy.Minimum)
        layout9.addItem(spacer10,1,3)

        self.moveUpPushButton = PixmapLabelButton(widget,
            "up_user.png", "up_user.png", name='')

        layout9.addWidget(self.moveUpPushButton,1,1)

        self.moveDownPushButton.setEnabled(False)
        self.moveUpPushButton.setEnabled(False)
        self.removeRecipientPushButton.setEnabled(False)

        self.moveDownPushButton.setText(self.__tr("Move Down"))
        self.fabPushButton.setText(self.__tr("Fax Address Book..."))
        self.removeRecipientPushButton.setText(self.__tr("Remove"))
        self.moveUpPushButton.setText(self.__tr("Move Up"))


        self.connect(self.recipientListView,SIGNAL("rightButtonClicked(QListViewItem*,const QPoint&,int)"),self.recipientListView_rightButtonClicked)

        self.connect(self.removeRecipientPushButton,SIGNAL("clicked()"),self.removeRecipientPushButton_clicked)
        self.connect(self.moveUpPushButton,SIGNAL("clicked()"),self.moveUpPushButton_clicked)
        self.connect(self.moveDownPushButton,SIGNAL("clicked()"),self.moveDownPushButton_clicked)
        self.connect(self.fabPushButton,SIGNAL("clicked()"),self.fabPushButton_clicked)

        self.connect(self.recipientListView, SIGNAL("selectionChanged(QListViewItem*)"), self.recipientListView_selectionChanged)

        self.addWidget(widget, "recipient_list", maximize=False)


    def recipientListView_selectionChanged(self, i):
        try:
            self.prev_selected_recipient = i.name
        except AttributeError:
            pass
        else:
            rlv = self.recipientListView
            selected_item = rlv.selectedItem()
            recipient_count = rlv.childCount()
            last_item = rlv.firstChild()
            while last_item.nextSibling():
                last_item = last_item.nextSibling()

            self.moveDownPushButton.setEnabled(recipient_count > 1 and selected_item is not last_item)
            self.moveUpPushButton.setEnabled(recipient_count > 1 and selected_item is not rlv.firstChild())



    def updateRecipientList(self):
        self.recipientListView.clear()
        temp = self.recipient_list[:]
        temp.reverse()
        last_item = None
        selected_item = None
        order = len(temp)

        for name in temp:
            entry = self.db.get(name)
            # TODO: If entry was in list prior to name change in hp-fab,
            # this code will remove it instead of following the name change
            # Ref: CDP-1675
            if entry is not None:
                i = RecipientListViewItem(self.recipientListView, str(order), name, entry['fax'], entry['notes'])

                if not self.prev_selected_recipient or self.prev_selected_recipient == name:
                    self.recipientListView.setSelected(i, True)
                    selected_item = i
                    self.prev_selected_recipient = name

                order -= 1

        last_item = self.recipientListView.firstChild()
        while last_item is not None and last_item.nextSibling():
            last_item = last_item.nextSibling()

        child_count = self.recipientListView.childCount()
        self.removeRecipientPushButton.setEnabled(child_count > 0)
        self.moveDownPushButton.setEnabled(child_count > 1 and selected_item is not last_item)
        self.moveUpPushButton.setEnabled(child_count > 1 and selected_item is not self.recipientListView.firstChild())

        self.checkSendFaxButton()



    def recipientListView_rightButtonClicked(self, item, pos, col):
        self.ind_map = {}
        self.grp_map = {}
        popup = QPopupMenu(self)
        ind = QPopupMenu(popup)
        grp = QPopupMenu(popup)

        all_entries = self.db.get_all_records()
        if all_entries:
            popup.insertItem(QIconSet(load_pixmap('add_user', '16x16')),
                self.__tr("Add Individual"), ind)

            for e, v in all_entries.items():
                if not e.startswith('__'):
                    self.ind_map[ind.insertItem(QIconSet(load_pixmap('add_user', '16x16')), e, None)] = e

        all_groups = self.db.get_all_groups()
        if all_groups:
            popup.insertItem(QIconSet(load_pixmap('add_users', '16x16')),
                self.__tr("Add Group"), grp)

            for g in all_groups:
                self.grp_map[grp.insertItem(QIconSet(load_pixmap('add_users', '16x16')),
                    g, None)] = g

        if item is not None:
            popup.insertSeparator(-1)

            popup.insertItem(QIconSet(load_pixmap('remove_user', '16x16')),
                self.__tr("Remove"), self.removeRecipientPushButton_clicked)

            if self.recipientListView.childCount() > 1:
                last_item = self.recipientListView.firstChild()
                while last_item is not None and last_item.nextSibling():
                    last_item = last_item.nextSibling()

                if item is not self.recipientListView.firstChild():
                    popup.insertItem(QIconSet(load_pixmap('up_user', '16x16')),
                        self.__tr("Move Up"), self.moveUpPushButton_clicked)

                if item is not last_item:
                    popup.insertItem(QIconSet(load_pixmap('down_user', '16x16')),
                        self.__tr("Move Down"), self.moveDownPushButton_clicked)

        popup.insertSeparator(-1)
        popup.insertItem(QIconSet(load_pixmap('fab', '16x16')),
            self.__tr("Fax Address Book..."), self.fabPushButton_clicked)

        self.connect(ind, SIGNAL("activated(int)"), self.ind_popup_activated)
        self.connect(grp, SIGNAL("activated(int)"), self.grp_popup_activated)

        popup.popup(pos)


    def ind_popup_activated(self, i):
        self.addRecipient(self.ind_map[i])

    def grp_popup_activated(self, i):
        self.addRecipient(self.grp_map[i], True)

    def moveUpPushButton_clicked(self):
        try:
            name = self.recipientListView.selectedItem().name
        except AttributeError:
            return
        else:
            utils.list_move_up(self.recipient_list, name)
            self.updateRecipientList()

    def moveDownPushButton_clicked(self):
        try:
            name = self.recipientListView.selectedItem().name
        except AttributeError:
            return
        else:
            utils.list_move_down(self.recipient_list, name)
            self.updateRecipientList()


    def fabPushButton_clicked(self):
        log.debug(self.cmd_fab)
        #print self.cmd_fab
        cmd = ''.join([self.cur_device.device_vars.get(x, x) \
                         for x in self.cmd_fab.split('%')])
        log.debug(cmd)

        path = cmd.split()[0]
        args = cmd.split()

        self.CleanupChildren()
        os_utils.execute(cmd)

        self.db.load()
        self.updateRecipientList()
        self.updateRecipientCombos()


    def CleanupChildren(self):
        log.debug("Cleaning up child processes.")
        try:
            os.waitpid(-1, os.WNOHANG)
        except OSError:
            pass


    def removeRecipientPushButton_clicked(self):
        try:
            name = self.recipientListView.selectedItem().name
        except AttributeError:
            return
        else:
            temp = self.recipient_list[:]
            index = 0
            for n in temp:
                if name == n:
                    del self.recipient_list[index]

                    self.prev_selected_recipient = ''
                    self.updateRecipientList()
                    break

                index += 1



    #
    # ADD FROM ADDRESS BOOK
    #

    def addRecipientAddFromFAB(self):
        widget = self.getWidget()

        layout13 = QGridLayout(widget,1,1,5,10,"layout13")

        self.groupComboBox = QComboBox(0,widget,"groupComboBox")
        self.groupComboBox.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed,0,0,self.groupComboBox.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.groupComboBox,1,2)
        spacer12 = QSpacerItem(20,20,QSizePolicy.Preferred,QSizePolicy.Minimum)
        layout13.addItem(spacer12,1,1)

        self.textLabel1 = QLabel(widget,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.textLabel1,0,0)

        self.individualComboBox = QComboBox(0,widget,"individualComboBox")
        self.individualComboBox.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed,0,0,self.individualComboBox.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.individualComboBox,0,2)

        self.textLabel2 = QLabel(widget,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        layout13.addWidget(self.textLabel2,1,0)
        spacer11 = QSpacerItem(30,20,QSizePolicy.Preferred,QSizePolicy.Minimum)
        layout13.addItem(spacer11,0,1)

        self.addGroupPushButton = PixmapLabelButton(widget,
                    "add_users.png", "add_users.png", name='addGroupPushButton')

        layout13.addWidget(self.addGroupPushButton,1,3)

        self.addIndividualPushButton = PixmapLabelButton(widget,
                    "add_user.png", "add_user.png", name='addIndividualPushButton')


        layout13.addWidget(self.addIndividualPushButton,0,3)

        self.textLabel1.setText(self.__tr("Add an <b>individual </b>from the fax address book:"))
        self.textLabel2.setText(self.__tr("Add a <b>group</b> from the fax address book:"))
        self.addGroupPushButton.setText(self.__tr("Add"))
        self.addIndividualPushButton.setText(self.__tr("Add"))

        self.connect(self.addIndividualPushButton,SIGNAL("clicked()"),self.addIndividualPushButton_clicked)
        self.connect(self.addGroupPushButton,SIGNAL("clicked()"),self.addGroupPushButton_clicked)


        self.addWidget(widget, "recipient_add_from_fab")

    def addIndividualPushButton_clicked(self):
        self.addRecipient(unicode(self.individualComboBox.currentText()))

    def addGroupPushButton_clicked(self):
        self.addRecipient(unicode(self.groupComboBox.currentText()), True)

    def addRecipient(self, name, is_group=False):
        if is_group:
            for i in self.db.group_members(name):
            #for i in self.db.GroupEntries(name):
                if not i.startswith('__'):
                    self.recipient_list.append(i)
                    self.prev_selected_recipient = self.recipient_list[-1]
        else:
            self.recipient_list.append(name)
            self.prev_selected_recipient = name

        self.updateRecipientList()

    def updateRecipientCombos(self):
        # Individuals
        self.individualComboBox.clear()
        all_entries = self.db.get_all_records()
        self.addIndividualPushButton.setEnabled(len(all_entries))

        for e, v in all_entries.items():
            if not e.startswith('__'):
                self.individualComboBox.insertItem(e)

        # Groups
        self.groupComboBox.clear()
        all_groups = self.db.get_all_groups()
        self.addGroupPushButton.setEnabled(len(all_groups))

        for g in all_groups:
            self.groupComboBox.insertItem(g)


    #
    # QUICK ADD
    #

    def addRecipientQuickAdd(self):
        widget = self.getWidget()

        layout12 = QGridLayout(widget,1,1,5,10,"layout12")
        self.quickAddFaxLineEdit = QLineEdit(widget,"quickAddFaxLineEdit")

        self.quickAddFaxLineEdit.setValidator(PhoneNumValidator(self.quickAddFaxLineEdit))
        layout12.addWidget(self.quickAddFaxLineEdit,0,3)

        self.quickAddNameLineEdit = QLineEdit(widget,"quickAddNameLineEdit")
        layout12.addWidget(self.quickAddNameLineEdit,0,1)

        self.textLabel4 = QLabel(widget,"textLabel4")
        layout12.addWidget(self.textLabel4,0,0)

        self.quickAddPushButton = PixmapLabelButton(widget,
                    "add_user_quick.png", "add_user_quick.png", name='quickAddPushButton')

        layout12.addWidget(self.quickAddPushButton,0,4)

        self.textLabel5 = QLabel(widget,"textLabel5")
        layout12.addWidget(self.textLabel5,0,2)

        self.textLabel4.setText(self.__tr("Name:"))
        self.quickAddPushButton.setText(self.__tr("Add"))
        self.textLabel5.setText(self.__tr("Fax Number:"))

        self.quickAddPushButton.setEnabled(False)

        self.connect(self.quickAddPushButton,SIGNAL("clicked()"),self.quickAddPushButton_clicked)
        self.connect(self.quickAddNameLineEdit,SIGNAL("textChanged(const QString&)"),self.quickAddNameLineEdit_textChanged)
        self.connect(self.quickAddFaxLineEdit,SIGNAL("textChanged(const QString&)"),self.quickAddFaxLineEdit_textChanged)

        self.addWidget(widget, "recipient_quick_add")


    def quickAddPushButton_clicked(self):
        name =  unicode(self.quickAddNameLineEdit.text())
        self.db.set(name, u'', u'', u'', unicode(self.quickAddFaxLineEdit.text()), [], self.__tr('Added with Quick Add'))
        self.db.save()
        self.addRecipient(name)

        self.quickAddNameLineEdit.setText("")
        self.quickAddFaxLineEdit.setText("")


    def enableQuickAddButton(self, name=None, fax=None):
        if name is None:
            name = unicode(self.quickAddNameLineEdit.text())
        if fax is None:
            fax = unicode(self.quickAddFaxLineEdit.text())

        existing_name = False
        if name:
            existing_name = name in self.db.get_all_names()

        if existing_name:
            try:
                self.quickAddNameLineEdit.setPaletteBackgroundColor(QColor("yellow"))
            except AttributeError:
                pass
        else:
            try:
                self.quickAddNameLineEdit.setPaletteBackgroundColor(QColor("white"))
            except AttributeError:
                pass

        if name and not existing_name and fax:
            self.quickAddPushButton.setEnabled(True)
        else:
            self.quickAddPushButton.setEnabled(False)


    def quickAddNameLineEdit_textChanged(self, name):
        self.enableQuickAddButton(unicode(name))


    def quickAddFaxLineEdit_textChanged(self, fax):
        self.enableQuickAddButton(None, unicode(fax))


    def checkSendFaxButton(self):
        self.faxButton.setEnabled(len(self.file_list) and len(self.recipient_list))

    def faxButton_clicked(self):
        self.check_timer.stop()
        phone_num_list = []

        log.debug("Current printer=%s" % self.cur_printer)
        ppd_file = cups.getPPD(self.cur_printer)

        if ppd_file is not None and os.path.exists(ppd_file):
            if file(ppd_file, 'r').read().find('HP Fax') == -1:
                self.form.FailureUI(self.__tr("<b>Fax configuration error.</b><p>The CUPS fax queue for '%1' is incorrectly configured.<p>Please make sure that the CUPS fax queue is configured with the 'HPLIP Fax' Model/Driver.").arg(self.cur_printer))
                return

        QApplication.setOverrideCursor(QApplication.waitCursor)

        self.dev = fax.getFaxDevice(self.cur_device.device_uri,
                                   self.cur_printer, None,
                                   self.cur_device.mq['fax-type'])

        try:
            try:
                self.dev.open()
            except Error, e:
                log.warn(e.msg)

            try:
                self.dev.queryDevice(quick=True)
            except Error, e:
                log.error("Query device error (%s)." % e.msg)
                self.dev.error_state = ERROR_STATE_ERROR

        finally:
            self.dev.close()
            QApplication.restoreOverrideCursor()

        if self.dev.error_state > ERROR_STATE_MAX_OK and \
            self.dev.error_state not in (ERROR_STATE_LOW_SUPPLIES, ERROR_STATE_LOW_PAPER):

            self.form.FailureUI(self.__tr("<b>Device is busy or in an error state (code=%1)</b><p>Please wait for the device to become idle or clear the error and try again.").arg(self.cur_device.status_code))
            return

        # Check to make sure queue in CUPS is idle
        self.cups_printers = cups.getPrinters()
        for p in self.cups_printers:
            if p.name == self.cur_printer:
                if p.state == cups.IPP_PRINTER_STATE_STOPPED:
                    self.form.FailureUI(self.__tr("<b>The CUPS queue for '%1' is in a stopped or busy state.</b><p>Please check the queue and try again.").arg(self.cur_printer))
                    return
                break

        log.debug("Recipient list:")

        for p in self.recipient_list:
            entry = self.db.get(p)
            phone_num_list.append(entry)
            log.debug("Name=%s Number=%s" % (entry["name"], entry["fax"]))

        log.debug("File list:")


        for f in self.file_list:
            log.debug(unicode(f))

        self.busy = True

        self.dev.sendEvent(EVENT_START_FAX_JOB, self.cur_printer, 0, '')

        if not self.dev.sendFaxes(phone_num_list, self.file_list, self.cover_page_message,
                                  self.cover_page_re, self.cover_page_func, self.preserve_formatting,
                                  self.cur_printer, self.update_queue, self.event_queue):

            self.form.FailureUI(self.__tr("<b>Send fax is active.</b><p>Please wait for operation to complete."))
            self.dev.sendEvent(EVENT_FAX_JOB_FAIL, self.cur_printer, 0, '')
            self.busy = False
            return


        self.waitdlg = WaitForm(0, self.__tr("Initializing..."), self.send_fax_canceled, self, modal=1)
        self.waitdlg.show()

        self.send_fax_timer = QTimer(self, "SendFaxTimer")
        self.connect(self.send_fax_timer, SIGNAL('timeout()'), self.send_fax_timer_timeout)
        self.send_fax_timer.start(1000) # 1 sec UI updates

    def send_fax_canceled(self):
        self.event_queue.put((fax.EVENT_FAX_SEND_CANCELED, '', '', ''))
        self.dev.sendEvent(EVENT_FAX_JOB_CANCELED, self.cur_printer, 0, '')

    def send_fax_timer_timeout(self):
        while self.update_queue.qsize():
            try:
                status, page_num, arg = self.update_queue.get(0)
            except Queue.Empty:
                break

            if status == fax.STATUS_IDLE:
                self.busy = False
                self.send_fax_timer.stop()

                if self.waitdlg is not None:
                    self.waitdlg.hide()
                    self.waitdlg.close()
                    self.waitdlg = None

            elif status == fax.STATUS_PROCESSING_FILES:
                self.waitdlg.setMessage(self.__tr("Processing page %1...").arg(page_num))

            elif status == fax.STATUS_SENDING_TO_RECIPIENT:
                self.waitdlg.setMessage(self.__tr("Sending fax to %1...").arg(arg))

            elif status == fax.STATUS_DIALING:
                self.waitdlg.setMessage(self.__tr("Dialing %1...").arg(arg))

            elif status == fax.STATUS_CONNECTING:
                self.waitdlg.setMessage(self.__tr("Connecting to %1...").arg(arg))

            elif status == fax.STATUS_SENDING:
                self.waitdlg.setMessage(self.__tr("Sending page %1 to %2...").arg(page_num).arg(arg))

            elif status == fax.STATUS_CLEANUP:
                self.waitdlg.setMessage(self.__tr("Cleaning up..."))

            elif status in (fax.STATUS_ERROR, fax.STATUS_BUSY, fax.STATUS_COMPLETED):
                self.busy = False
                self.send_fax_timer.stop()

                if self.waitdlg is not None:
                    self.waitdlg.hide()
                    self.waitdlg.close()
                    self.waitdlg = None

                if status == fax.STATUS_ERROR:
                    result_code, error_state = self.dev.getPML(pml.OID_FAX_DOWNLOAD_ERROR)
                    if error_state == pml.DN_ERROR_NONE:
                        self.form.FailureUI(self.__tr("<b>Fax send error (Possible cause: No answer or dialtone)"))
                    else:
                        self.form.FailureUI(self.__tr("<b>Fax send error (%s).</b><p>" % pml.DN_ERROR_STR.get(error_state, "Unknown error")))
                    self.dev.sendEvent(EVENT_FAX_JOB_FAIL, self.cur_printer, 0, '')

                elif status == fax.STATUS_BUSY:
                    self.form.FailureUI(self.__tr("<b>Fax device is busy.</b><p>Please try again later."))
                    self.dev.sendEvent(EVENT_FAX_JOB_FAIL, self.cur_printer, 0, '')

                elif status == fax.STATUS_COMPLETED:
                    self.dev.sendEvent(EVENT_END_FAX_JOB, self.cur_printer, 0, '')

                    self.funcButton_clicked()


    def cleanup(self):
        self.unlock()

        if fax_enabled:
            self.check_timer.stop()

    def funcButton_clicked(self):
        self.cleanup()
        self.form.close()

    def __tr(self,s,c = None):
        return qApp.translate("ScrollFaxView",s,c)
