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
from base import utils, magic, os_utils
from prnt import cups
from ui_utils import load_pixmap

# Qt
from qt import *
from scrollview import ScrollView, PixmapLabelButton
from allowabletypesdlg import AllowableTypesDlg
from jobstoragemixin import JobStorageMixin

# Std Lib
import os.path
import os
import time

class RangeValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        for x in unicode(input)[pos-1:]:
            if x not in u'0123456789,- ':
                return QValidator.Invalid, pos

        return QValidator.Acceptable, pos



class FileListViewItem(QListViewItem):
    def __init__(self, parent, index, filename, mime_type_desc, path):
        QListViewItem.__init__(self, parent, str(index+1), filename, mime_type_desc, path)
        self.path = path
        self.index = index


class ScrollPrintView(ScrollView):
    utils.mixin(JobStorageMixin)

    def __init__(self, service, parent=None, form=None, name=None, fl=0):
        ScrollView.__init__(self, service, parent, name, fl)

        self.initJobStorage()

        self.form = form
        self.file_list = []
        self.pages_button_group = 0
        self.prev_selected_file_index = 0

        self.allowable_mime_types = cups.getAllowableMIMETypes()
        log.debug(self.allowable_mime_types)

        self.MIME_TYPES_DESC = \
        {
            "application/pdf" : (self.__tr("PDF Document"), '.pdf'),
            "application/postscript" : (self.__tr("Postscript Document"), '.ps'),
            "application/vnd.hp-HPGL" : (self.__tr("HP Graphics Language File"), '.hgl, .hpg, .plt, .prn'),
            "application/x-cshell" : (self.__tr("C Shell Script"), '.csh, .sh'),
            "application/x-csource" : (self.__tr("C Source Code"), '.c'),
            "text/cpp": (self.__tr("C/C++ Source Code"), '.c, .cpp, .cxx'),
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


    def fillControls(self):
        ScrollView.fillControls(self)

        if self.addPrinterFaxList():
            self.addGroupHeading("files_to_print", self.__tr("File(s) to Print"))
            self.addFileList()
            self.addGroupHeading("options", self.__tr("Print Options"))
            self.addCopies()
            self.addPageRange()
            self.addPageSet()

            self.job_storage_avail = self.cur_device.mq['job-storage'] == JOB_STORAGE_ENABLE

            if self.job_storage_avail:
                self.addGroupHeading("jobstorage", self.__tr("Job Storage and Secure Printing"))
                self.addJobStorage()

            self.addGroupHeading("space1", "")

            self.printButton = self.addActionButton("bottom_nav", self.__tr("Print File(s)"),
                                    self.printButton_clicked, 'print.png', 'print.png',
                                    self.__tr("Close"), self.funcButton_clicked)

            self.printButton.setEnabled(False)
            self.maximizeControl()

        else:
            QApplication.restoreOverrideCursor()
            self.form.FailureUI("<b>Print is disabled.</b><p>No CUPS print queue found for this device.")
            self.funcButton_clicked()


    def onUpdate(self, cur_device=None):
        log.debug("ScrollPrintView.onUpdate()")
        self.updateFileList()

    def onDeviceChange(self, cur_device=None):
        self.file_list = []
        ScrollView.onDeviceChange(self, cur_device)

    def addFileList(self):
        widget = self.getWidget()
        layout37 = QGridLayout(widget,1,1,5,10,"layout37")

        self.addFilePushButton = PixmapLabelButton(widget,
            "list_add.png", "list_add.png")

        layout37.addWidget(self.addFilePushButton,2,0)

        self.removeFilePushButton = PixmapLabelButton(widget,
            "list_remove.png", "list_remove.png")

        layout37.addWidget(self.removeFilePushButton,2,1)

        self.moveFileUpPushButton = PixmapLabelButton(widget, "up.png",
            "up.png", name='moveFileUpPushButton')

        layout37.addWidget(self.moveFileUpPushButton,2,2)

        self.moveFileDownPushButton = PixmapLabelButton(widget, "down.png",
            "down.png", name='moveFileDownPushButton')

        layout37.addWidget(self.moveFileDownPushButton,2,3)

        self.showTypesPushButton = PixmapLabelButton(widget, "mimetypes.png",
            None, name='addFilePushButton')

        layout37.addWidget(self.showTypesPushButton,2,5)
        self.fileListView = QListView(widget,"fileListView")
        self.fileListView.addColumn(self.__tr("Order"))
        self.fileListView.addColumn(self.__tr("Name"))
        self.fileListView.addColumn(self.__tr("Type"))
        self.fileListView.addColumn(self.__tr("Path"))
        self.fileListView.setAllColumnsShowFocus(1)
        self.fileListView.setShowSortIndicator(1)
        self.fileListView.setColumnWidth(0, 100)
        self.fileListView.setColumnWidth(1, 150)
        self.fileListView.setColumnWidth(2, 75)
        self.fileListView.setColumnWidth(3, 300)
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
        self.connect(self.fileListView,SIGNAL("rightButtonClicked(QListViewItem*,const QPoint&, int)"),self.fileListView_rightButtonClicked)

        self.connect(self.moveFileUpPushButton, SIGNAL("clicked()"), self.moveFileUp_clicked)
        self.connect(self.moveFileDownPushButton, SIGNAL("clicked()"), self.moveFileDown_clicked)
        self.connect(self.fileListView, SIGNAL("selectionChanged(QListViewItem*)"),
            self.fileListView_selectionChanged)

        self.addWidget(widget, "file_list", maximize=True)

    def fileListView_selectionChanged(self, i):
        try:
            self.prev_selected_file_index = i.index
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

    def moveFileUp_clicked(self):
        log.debug("Move file up")
        try:
            item = self.fileListView.selectedItem()
            path, index = item.path, item.index
        except AttributeError:
            return
        else:
            new_pos = index-1
            self.file_list[new_pos], self.file_list[index] = self.file_list[index], self.file_list[new_pos]
            item.index = new_pos
            self.prev_selected_file_index = new_pos
            self.updateFileList()

    def moveFileDown_clicked(self):
        log.debug("Move file down")
        try:
            item = self.fileListView.selectedItem()
            path, index = item.path, item.index
        except AttributeError:
            return
        else:
            new_pos = index+1
            self.file_list[index], self.file_list[new_pos] = self.file_list[new_pos], self.file_list[index]
            item.index = new_pos
            self.prev_selected_file_index = new_pos
            self.updateFileList()

    def addFile(self, path):
        path = os.path.realpath(path)
        if os.path.exists(path) and os.access(path, os.R_OK):
            mime_type = magic.mime_type(path)
            mime_type_desc = mime_type
            log.debug(mime_type)

            try:
                mime_type_desc = self.MIME_TYPES_DESC[mime_type][0]
            except KeyError:
                self.form.FailureUI(self.__tr("<b>You are trying to add a file that cannot be directly printed with this utility.</b><p>To print this file, use the print command in the application that created it."))
            else:
                log.debug("Adding file %s (%s,%s)" % (path, mime_type, mime_type_desc))
                self.file_list.append((path, mime_type, mime_type_desc))
        else:
            self.form.FailureUI(self.__tr("<b>Unable to add file '%1' to file list (file not found or insufficient permissions).</b><p>Check the file name and try again.").arg(path))

        self.updateFileList()

    def updateFileList(self):
        self.fileListView.clear()
        temp = self.file_list[:]
        temp.reverse()
        last_item = None
        selected_item = None
        index = len(temp)-1

        for path, mime_type, desc in temp:
            log.debug("path=%s, mime_type=%s, desc=%s, index=%d" % (path, mime_type, desc, index))
            i = FileListViewItem(self.fileListView, index, os.path.basename(path), desc, path)

            if self.prev_selected_file_index == index:
                self.fileListView.setSelected(i, True)
                self.prev_selected_file_index = index
                selected_item = i

            index -= 1

        last_item = self.fileListView.firstChild()
        while last_item is not None and last_item.nextSibling():
            last_item = last_item.nextSibling()

        file_count = self.fileListView.childCount()
        self.moveFileDownPushButton.setEnabled(file_count > 1 and selected_item is not last_item)
        self.moveFileUpPushButton.setEnabled(file_count > 1 and selected_item is not self.fileListView.firstChild())
        self.removeFilePushButton.setEnabled(file_count > 0)
        self.printButton.setEnabled(file_count > 0)

    def addFile_clicked(self):
        dlg = QFileDialog(user_conf.workingDirectory(), QString.null, None, None, True)

        dlg.setCaption("openfile")
        dlg.setMode(QFileDialog.ExistingFile)
        dlg.show()

        if dlg.exec_loop() == QDialog.Accepted:
                results = dlg.selectedFile()
                working_directory = unicode(dlg.dir().absPath())
                #log.debug("results: %s" % unicode(results))
                user_conf.setWorkingDirectory(working_directory)

                if results:
                    self.addFile(unicode(results))

    def removeFile_clicked(self):
        try:
            path = self.fileListView.selectedItem().path
        except AttributeError:
            return
        else:
            temp = self.file_list[:]
            index = 0
            for p, t, d in temp:
                if p == path:
                    del self.file_list[index]
                    if index == self.prev_selected_file_index:
                        self.prev_selected_file_index = 0
                    break
                index += 1

            self.updateFileList()

    def showFileTypes_clicked(self):
        x = {}
        for a in self.allowable_mime_types:
            x[a] = self.MIME_TYPES_DESC.get(a, ('Unknown', 'n/a'))

        log.debug(x)
        dlg = AllowableTypesDlg(x, self)
        dlg.exec_loop()


    def addCopies(self):
        widget = self.getWidget()

        layout12 = QHBoxLayout(widget,5,10,"layout12")

        self.textLabel5 = QLabel(widget,"textLabel5")
        layout12.addWidget(self.textLabel5)
        spacer20 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout12.addItem(spacer20)

        self.copiesSpinBox = QSpinBox(widget,"copiesSpinBox")
        layout12.addWidget(self.copiesSpinBox)

        self.copiesDefaultPushButton = QPushButton(widget,"copiesDefaultPushButton")
        layout12.addWidget(self.copiesDefaultPushButton)

        self.textLabel5.setText(self.__tr("Number of copies:"))
        self.copiesDefaultPushButton.setText(self.__tr("Default"))

        self.copiesSpinBox.setMaxValue(99)
        self.copiesSpinBox.setMinValue(1)
        self.copiesSpinBox.setValue(1)

        self.copiesDefaultPushButton.setEnabled(False)

        self.connect(self.copiesDefaultPushButton, SIGNAL("clicked()"), self.copiesDefaultPushButton_clicked)
        self.connect(self.copiesSpinBox, SIGNAL("valueChanged(int)"), self.copiesSpinBox_valueChanged)

        self.addWidget(widget, "copies")

    def copiesDefaultPushButton_clicked(self):
        self.copiesSpinBox.setValue(1)
        self.copiesDefaultPushButton.setEnabled(False)

    def copiesSpinBox_valueChanged(self, i):
        self.copiesDefaultPushButton.setEnabled(i != 1)

    def addPageRange(self):
        widget = self.getWidget()

        layout39 = QGridLayout(widget,1,1,5,10,"layout39")

        self.pageRangeEdit = QLineEdit(widget,"self.pageRangeEdit")
        self.pageRangeEdit.setEnabled(0)
        layout39.addWidget(self.pageRangeEdit,0,3)

        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout39.addItem(spacer20_2,0,1)

        textLabel5_2 = QLabel(widget,"textLabel5_2")
        layout39.addWidget(textLabel5_2,0,0)

        self.pagerangeDefaultPushButton = QPushButton(widget,"pagerangeDefaultPushButton")
        layout39.addWidget(self.pagerangeDefaultPushButton,0,4)

        self.rangeButtonGroup = QButtonGroup(widget,"self.rangeButtonGroup")
        self.rangeButtonGroup.setLineWidth(0)
        self.rangeButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.rangeButtonGroup.layout().setSpacing(0)
        self.rangeButtonGroup.layout().setMargin(0)
        self.rangeButtonGroupLayout = QGridLayout(self.rangeButtonGroup.layout())
        self.rangeButtonGroupLayout.setAlignment(Qt.AlignTop)

        radioButton3_2 = QRadioButton(self.rangeButtonGroup,"radioButton3_2")
        radioButton3_2.setChecked(1)
        self.rangeButtonGroup.insert( radioButton3_2,0)
        self.rangeButtonGroupLayout.addWidget(radioButton3_2,0,0)

        radioButton4_2 = QRadioButton(self.rangeButtonGroup,"radioButton4_2")
        self.rangeButtonGroup.insert( radioButton4_2,1)
        self.rangeButtonGroupLayout.addWidget(radioButton4_2,0,1)

        layout39.addWidget(self.rangeButtonGroup,0,2)

        self.bg = self.pageRangeEdit.paletteBackgroundColor()
        self.invalid_page_range = False

        self.pageRangeEdit.setValidator(RangeValidator(self.pageRangeEdit))

        textLabel5_2.setText(self.__tr("Page Range:"))
        radioButton3_2.setText(self.__tr("All pages"))
        radioButton4_2.setText(self.__tr("Page range:"))

        self.pagerangeDefaultPushButton.setText(self.__tr("Default"))

        self.pagerangeDefaultPushButton.setEnabled(False)

        self.connect(self.rangeButtonGroup, SIGNAL("clicked(int)"), self.rangeButtonGroup_clicked)
        self.connect(self.pageRangeEdit,SIGNAL("lostFocus()"),self.pageRangeEdit_lostFocus)
        self.connect(self.pageRangeEdit,SIGNAL("textChanged(const QString&)"),self.pageRangeEdit_textChanged)
        self.connect(self.pagerangeDefaultPushButton, SIGNAL("clicked()"), self.pagerangeDefaultPushButton_clicked)

        self.addWidget(widget, "range")

    def pagerangeDefaultPushButton_clicked(self):
        self.rangeButtonGroup.setButton(0)
        self.pagerangeDefaultPushButton.setEnabled(False)
        self.pageRangeEdit.setEnabled(False)

    def rangeButtonGroup_clicked(self, a0):
        self.pages_button_group = a0
        self.pageRangeEdit.setEnabled(a0 == 1)
        self.pagerangeDefaultPushButton.setEnabled(a0 == 1)

    def pageRangeEdit_lostFocus(self):
        x = []
        try:
            x = utils.expand_range(unicode(self.pageRangeEdit.text()))
        except ValueError:
            log.error("Invalid page range entered.")
            self.invalid_page_range = True
            self.pageRangeEdit.setPaletteBackgroundColor(QColor(0xff, 0x99, 0x99))

        else:
            self.pageRangeEdit.setText(QString(utils.collapse_range(x)))
            self.pageRangeEdit.setPaletteBackgroundColor(self.bg)
            self.invalid_page_range = False

    def pageRangeEdit_textChanged(self,a0):
        x = []
        try:
            x = utils.expand_range(str(self.pageRangeEdit.text()))
        except ValueError:
            self.invalid_page_range = True
            self.pageRangeEdit.setPaletteBackgroundColor(QColor(0xff, 0x99, 0x99))

        else:
            self.pageRangeEdit.setPaletteBackgroundColor(self.bg)
            self.invalid_page_range = False

    def addPageSet(self):
        widget = self.getWidget()

        layout34 = QHBoxLayout(widget,5,10,"layout34")

        self.textLabel5_4 = QLabel(widget,"textLabel5_4")
        layout34.addWidget(self.textLabel5_4)
        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout34.addItem(spacer20_4)

        self.pageSetComboBox = QComboBox(0,widget,"pageSetComboBox")
        layout34.addWidget(self.pageSetComboBox)

        self.pagesetDefaultPushButton = QPushButton(widget,"pagesetDefaultPushButton")
        layout34.addWidget(self.pagesetDefaultPushButton)

        self.textLabel5_4.setText(self.__tr("Page set:"))
        self.pageSetComboBox.clear()
        self.pageSetComboBox.insertItem(self.__tr("All pages"))
        self.pageSetComboBox.insertItem(self.__tr("Even pages"))
        self.pageSetComboBox.insertItem(self.__tr("Odd pages"))
        self.pagesetDefaultPushButton.setText(self.__tr("Default"))

        self.pagesetDefaultPushButton.setEnabled(False)

        self.connect(self.pageSetComboBox, SIGNAL("activated(int)"), self.pageSetComboBox_activated)
        self.connect(self.pagesetDefaultPushButton, SIGNAL("clicked()"), self.pagesetDefaultPushButton_clicked)

        self.addWidget(widget, "set")

    def pagesetDefaultPushButton_clicked(self):
        self.pagesetDefaultPushButton.setEnabled(False)
        self.pageSetComboBox.setCurrentItem(0)

    def pageSetComboBox_activated(self, i):
        self.pagesetDefaultPushButton.setEnabled(i != 0)

##    #
##    # JOB STORAGE
##    #
##
##    def addJobStorage(self):
##        self.addJobStorageMode()
##        self.addJobStoragePIN()
##        self.addJobStorageUsername()
##        self.addJobStorageID()
##        self.addJobStorageIDExists()
##        self.jobStorageDisable()
##
##
##    def addJobStorageMode(self):
##        widget = self.getWidget()
##
##        layout34 = QHBoxLayout(widget,5,10,"layout34")
##
##        self.jobStorageModeLabel = QLabel(widget,"jobStorageModeLabel")
##        layout34.addWidget(self.jobStorageModeLabel)
##        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
##        layout34.addItem(spacer20_4)
##
##        self.jobStorageModeComboBox = QComboBox(0,widget,"jobStorageModeComboBox")
##        layout34.addWidget(self.jobStorageModeComboBox)
##
##        self.jobStorageModeDefaultPushButton = QPushButton(widget,"pagesetDefaultPushButton")
##        layout34.addWidget(self.jobStorageModeDefaultPushButton)
##
##        self.jobStorageModeLabel.setText(self.__tr("Job Storage Mode:"))
##        self.jobStorageModeComboBox.clear()
##        self.jobStorageModeComboBox.insertItem(self.__tr("Off"))
##        self.jobStorageModeComboBox.insertItem(self.__tr("Proof and Hold"))
##        self.jobStorageModeComboBox.insertItem(self.__tr("Personal/Private Job"))
##        self.jobStorageModeComboBox.insertItem(self.__tr("Quick Copy"))
##        self.jobStorageModeComboBox.insertItem(self.__tr("Stored Job"))
##
##        self.jobStorageModeDefaultPushButton.setText(self.__tr("Default"))
##        self.jobStorageModeDefaultPushButton.setEnabled(False)
##
##        self.connect(self.jobStorageModeComboBox, SIGNAL("activated(int)"), self.jobStorageModeComboBox_activated)
##        self.connect(self.jobStorageModeDefaultPushButton, SIGNAL("clicked()"), self.jobStorageModeDefaultPushButton_clicked)
##
##        self.addWidget(widget, "job_storage_mode")
##
##    def jobStorageModeComboBox_activated(self, a):
##        self.job_storage_mode = a
##
##        if a == 0: # Off
##            self.jobStorageDisable()
##
##        elif a == 1: # Proof and Hold
##            self.jobStorageModeDefaultPushButton.setEnabled(True)
##            self.jobStorageUserJobEnable(True)
##            self.jobStoragePINEnable(False)
##
##        elif a == 2: # Private Job
##            self.jobStorageModeDefaultPushButton.setEnabled(True)
##            self.jobStoragePINEnable(True)
##            self.jobStorageUserJobEnable(True)
##
##        elif a == 3: # Quick Copy
##            self.jobStorageModeDefaultPushButton.setEnabled(True)
##            self.jobStoragePINEnable(False)
##            self.jobStorageUserJobEnable(True)
##
##        elif a == 4: # Stored Job
##            self.jobStorageModeDefaultPushButton.setEnabled(True)
##            self.jobStoragePINEnable(True) # ???
##            self.jobStorageUserJobEnable(True)
##
##    def jobStorageModeDefaultPushButton_clicked(self):
##        self.jobStorageModeComboBox.setCurrentItem(0)
##        self.job_storage_mode = 0
##
##    def jobStorageDisable(self): # Turn all Off
##        self.jobStorageModeDefaultPushButton.setEnabled(False)
##        self.jobStoragePINEnable(False)
##        self.jobStorageUserJobEnable(False)
##
##    def jobStoragePINEnable(self, e=True): # PIN On/Off
##        t = e and self.jobStoragePINButtonGroup.selectedId() == 1
##        self.jobStoragePINButtonGroup.setEnabled(e)
##        self.jobStoragePINEdit.setEnabled(t)
##        self.jobStoragePINDefaultPushButton.setEnabled(t)
##
##    def jobStorageUserJobEnable(self, e=True): # Username/Job ID/Job ID Exists On/Off
##        t = e and self.jobStorageUsernameButtonGroup.selectedId() == 1
##        self.jobStorageUsernameButtonGroup.setEnabled(e)
##        self.jobStorageUsernameDefaultPushButton.setEnabled(t)
##        self.jobStorageUsernameEdit.setEnabled(t)
##
##        t = e and self.jobStorageIDButtonGroup.selectedId() == 1
##        self.jobStorageIDButtonGroup.setEnabled(e)
##        self.jobStorageIDDefaultPushButton.setEnabled(t)
##        self.jobStorageIDEdit.setEnabled(t)
##
##        t = e and self.jobStorageIDExistsComboBox.currentItem() == 1
##        self.jobStorageIDExistsComboBox.setEnabled(e)
##        self.jobStorageIDExistsDefaultPushButton.setEnabled(t)
##
##
##
##    # PIN
##
##
##    def addJobStoragePIN(self):
##        widget = self.getWidget()
##
##        layout39 = QGridLayout(widget,1,1,5,10,"layout39")
##
##        self.jobStoragePINEdit = QLineEdit(widget,"self.jobStoragePINEdit")
##        self.jobStoragePINEdit.setMaxLength(4)
##        self.jobStoragePINEdit.setText(self.job_storage_pin)
##        layout39.addWidget(self.jobStoragePINEdit,0,3)
##
##        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
##        layout39.addItem(spacer20_2,0,1)
##
##        textLabel5_2 = QLabel(widget,"textLabel5_2")
##        layout39.addWidget(textLabel5_2,0,0)
##
##        self.jobStoragePINDefaultPushButton = QPushButton(widget,"jobStoragePINDefaultPushButton")
##        layout39.addWidget(self.jobStoragePINDefaultPushButton,0,4)
##
##        self.jobStoragePINButtonGroup = QButtonGroup(widget,"self.jobStoragePINButtonGroup")
##        self.jobStoragePINButtonGroup.setLineWidth(0)
##        self.jobStoragePINButtonGroup.setColumnLayout(0,Qt.Vertical)
##        self.jobStoragePINButtonGroup.layout().setSpacing(0)
##        self.jobStoragePINButtonGroup.layout().setMargin(0)
##        self.jobStoragePINButtonGroupLayout = QGridLayout(self.jobStoragePINButtonGroup.layout())
##        self.jobStoragePINButtonGroupLayout.setAlignment(Qt.AlignTop)
##
##        radioButton3_2 = QRadioButton(self.jobStoragePINButtonGroup,"radioButton3_2")
##        radioButton3_2.setChecked(1)
##        self.jobStoragePINButtonGroup.insert( radioButton3_2,0)
##        self.jobStoragePINButtonGroupLayout.addWidget(radioButton3_2,0,0)
##
##        radioButton4_2 = QRadioButton(self.jobStoragePINButtonGroup,"radioButton4_2")
##        self.jobStoragePINButtonGroup.insert( radioButton4_2,1)
##        self.jobStoragePINButtonGroupLayout.addWidget(radioButton4_2,0,1)
##
##        layout39.addWidget(self.jobStoragePINButtonGroup,0,2)
##
##        self.bg = self.jobStoragePINEdit.paletteBackgroundColor()
##        self.invalid_page_range = False
##
##        self.jobStoragePINEdit.setValidator(PINValidator(self.jobStoragePINEdit))
##
##        textLabel5_2.setText(self.__tr("Make Job Private (use PIN to print):"))
##        radioButton3_2.setText(self.__tr("Public/Off"))
##        radioButton4_2.setText(self.__tr("Private/Use PIN to Print:"))
##
##        self.jobStoragePINDefaultPushButton.setText(self.__tr("Default"))
##
##        self.connect(self.jobStoragePINButtonGroup, SIGNAL("clicked(int)"), self.jobStoragePINButtonGroup_clicked)
##        self.connect(self.jobStoragePINEdit,SIGNAL("lostFocus()"),self.jobStoragePINEdit_lostFocus)
##        self.connect(self.jobStoragePINEdit,SIGNAL("textChanged(const QString&)"),self.jobStoragePINEdit_textChanged)
##        self.connect(self.jobStoragePINDefaultPushButton, SIGNAL("clicked()"), self.jobStoragePINDefaultPushButton_clicked)
##
##        self.addWidget(widget, "job_storage_pin")
##
##    def jobStoragePINButtonGroup_clicked(self, a):
##        if a == 0: # Public/Off
##            self.jobStoragePINDefaultPushButton.setEnabled(False)
##            self.jobStoragePINEdit.setEnabled(False)
##            self.job_storage_use_pin = False
##            self.job_storage_pin = u"0000"
##
##        else: # On/Private/Use PIN
##            self.jobStoragePINDefaultPushButton.setEnabled(True)
##            self.jobStoragePINEdit.setEnabled(True)
##            self.job_storage_use_pin = True
##            self.job_storage_pin = unicode(self.jobStoragePINEdit.text())
##
##    def jobStoragePINEdit_lostFocus(self):
##        pafss
##
##    def jobStoragePINEdit_textChanged(self, a):
##        self.job_storage_pin = unicode(a)
##
##    def jobStoragePINDefaultPushButton_clicked(self):
##        self.jobStoragePINButtonGroup.setButton(0)
##        self.jobStoragePINDefaultPushButton.setEnabled(False)
##        self.jobStoragePINEdit.setEnabled(False)
##        self.job_storage_use_pin = False
##
##    # Username
##
##    def addJobStorageUsername(self):
##        widget = self.getWidget()
##
##        layout39 = QGridLayout(widget,1,1,5,10,"layout39")
##
##        self.jobStorageUsernameEdit = QLineEdit(widget,"self.jobStorageUsernameEdit")
##        self.jobStorageUsernameEdit.setMaxLength(16)
##        self.jobStorageUsernameEdit.setText(self.job_storage_username)
##        layout39.addWidget(self.jobStorageUsernameEdit,0,3)
##
##        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
##        layout39.addItem(spacer20_2,0,1)
##
##        textLabel5_2 = QLabel(widget,"textLabel5_2")
##        layout39.addWidget(textLabel5_2,0,0)
##
##        self.jobStorageUsernameDefaultPushButton = QPushButton(widget,"jobStorageUsernameDefaultPushButton")
##        layout39.addWidget(self.jobStorageUsernameDefaultPushButton,0,4)
##
##        self.jobStorageUsernameButtonGroup = QButtonGroup(widget,"self.jobStorageUsernameButtonGroup")
##        self.jobStorageUsernameButtonGroup.setLineWidth(0)
##        self.jobStorageUsernameButtonGroup.setColumnLayout(0,Qt.Vertical)
##        self.jobStorageUsernameButtonGroup.layout().setSpacing(0)
##        self.jobStorageUsernameButtonGroup.layout().setMargin(0)
##        self.jobStorageUsernameButtonGroupLayout = QGridLayout(self.jobStorageUsernameButtonGroup.layout())
##        self.jobStorageUsernameButtonGroupLayout.setAlignment(Qt.AlignTop)
##
##        radioButton3_2 = QRadioButton(self.jobStorageUsernameButtonGroup,"radioButton3_2")
##        radioButton3_2.setChecked(1)
##        self.jobStorageUsernameButtonGroup.insert( radioButton3_2,0)
##        self.jobStorageUsernameButtonGroupLayout.addWidget(radioButton3_2,0,0)
##
##        radioButton4_2 = QRadioButton(self.jobStorageUsernameButtonGroup,"radioButton4_2")
##        self.jobStorageUsernameButtonGroup.insert( radioButton4_2,1)
##        self.jobStorageUsernameButtonGroupLayout.addWidget(radioButton4_2,0,1)
##
##        layout39.addWidget(self.jobStorageUsernameButtonGroup,0,2)
##
##        self.bg = self.jobStorageUsernameEdit.paletteBackgroundColor()
##        self.invalid_page_range = False
##
##        self.jobStorageUsernameEdit.setValidator(TextValidator(self.jobStorageUsernameEdit))
##
##        textLabel5_2.setText(self.__tr("User name (for job identification):"))
##        radioButton3_2.setText(self.__tr("Automatic"))
##        radioButton4_2.setText(self.__tr("Custom:"))
##
##        self.jobStorageUsernameDefaultPushButton.setText(self.__tr("Default"))
##
##        self.connect(self.jobStorageUsernameButtonGroup, SIGNAL("clicked(int)"), self.jobStorageUsernameButtonGroup_clicked)
##        self.connect(self.jobStorageUsernameEdit,SIGNAL("lostFocus()"),self.jobStorageUsernameEdit_lostFocus)
##        self.connect(self.jobStorageUsernameEdit,SIGNAL("textChanged(const QString&)"),self.jobStorageUsernameEdit_textChanged)
##        self.connect(self.jobStorageUsernameDefaultPushButton, SIGNAL("clicked()"), self.jobStorageUsernameDefaultPushButton_clicked)
##
##        self.addWidget(widget, "job_storage_username")
##
##    def jobStorageUsernameButtonGroup_clicked(self, a):
##        if a == 0: # Automatic
##            self.jobStorageUsernameDefaultPushButton.setEnabled(False)
##            self.jobStorageUsernameEdit.setEnabled(False)
##            self.job_storage_auto_username = True
##            self.job_storage_username = unicode(prop.username[:16])
##
##        else: # Custom
##            self.jobStorageUsernameDefaultPushButton.setEnabled(True)
##            self.jobStorageUsernameEdit.setEnabled(True)
##            self.job_storage_auto_username = False
##            self.job_storage_username = unicode(self.jobStorageUsernameEdit.text())
##
##    def jobStorageUsernameEdit_lostFocus(saddJobStorageIDelf):
##        pass
##
##    def jobStorageUsernameEdit_textChanged(self, a):
##        self.job_storage_username = unicode(a)
##
##    def jobStorageUsernameDefaultPushButton_clicked(self):
##        self.jobStorageUsernameButtonGroup.setButton(0)
##        self.jobStorageUsernameDefaultPushButton.setEnabled(False)
##        self.jobStorageUsernameEdit.setEnabled(False)
##        self.job_storage_auto_username = True
##        self.job_storage_username = unicode(prop.username[:16])
##
##    # Job ID
##
##    def addJobStorageID(self):
##        widget = self.getWidget()
##
##        layout39 = QGridLayout(widget,1,1,5,10,"layout39")
##
##        self.jobStorageIDEdit = QLineEdit(widget,"self.jobStorageIDEdit")
##        self.jobStorageIDEdit.setMaxLength(16)
##        self.jobStorageIDEdit.setText(self.job_storage_jobname)
##        layout39.addWidget(self.jobStorageIDEdit,0,3)
##
##        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
##        layout39.addItem(spacer20_2,0,1)
##
##        textLabel5_2 = QLabel(widget,"textLabel5_2")
##        layout39.addWidget(textLabel5_2,0,0)
##
##        self.jobStorageIDDefaultPushButton = QPushButton(widget,"jobStorageIDDefaultPushButton")
##        layout39.addWidget(self.jobStorageIDDefaultPushButton,0,4)
##
##        self.jobStorageIDButtonGroup = QButtonGroup(widget,"self.jobStorageIDButtonGroup")
##        self.jobStorageIDButtonGroup.setLineWidth(0)
##        self.jobStorageIDButtonGroup.setColumnLayout(0,Qt.Vertical)
##        self.jobStorageIDButtonGroup.layout().setSpacing(0)
##        self.jobStorageIDButtonGroup.layout().setMargin(0)
##        self.jobStorageIDButtonGroupLayout = QGridLayout(self.jobStorageIDButtonGroup.layout())
##        self.jobStorageIDButtonGroupLayout.setAlignment(Qt.AlignTop)
##
##        radioButton3_2 = QRadioButton(self.jobStorageIDButtonGroup,"radioButton3_2")
##        radioButton3_2.setChecked(1)
##        self.jobStorageIDButtonGroup.insert( radioButton3_2,0)
##        self.jobStorageIDButtonGroupLayout.addWidget(radioButton3_2,0,0)
##
##        radioButton4_2 = QRadioButton(self.jobStorageIDButtonGroup,"radioButton4_2")
##        self.jobStorageIDButtonGroup.insert( radioButton4_2,1)
##        self.jobStorageIDButtonGroupLayout.addWidget(radioButton4_2,0,1)
##
##        layout39.addWidget(self.jobStorageIDButtonGroup,0,2)
##
##        self.bg = self.jobStorageIDEdit.paletteBackgroundColor()
##        self.invalid_page_range = False
##
##        self.jobStorageIDEdit.setValidator(TextValidator(self.jobStorageIDEdit))
##
##        textLabel5_2.setText(self.__tr("Job name (for job identification):"))
##        radioButton3_2.setText(self.__tr("Automatic"))
##        radioButton4_2.setText(self.__tr("Custom:"))
##
##        self.jobStorageIDDefaultPushButton.setText(self.__tr("Default"))
##
##        self.connect(self.jobStorageIDButtonGroup, SIGNAL("clicked(int)"), self.jobStorageIDButtonGroup_clicked)
##        self.connect(self.jobStorageIDEdit,SIGNAL("lostFocus()"),self.jobStorageIDEdit_lostFocus)
##        self.connect(self.jobStorageIDEdit,SIGNAL("textChanged(const QString&)"),self.jobStorageIDEdit_textChanged)
##        self.connect(self.jobStorageIDDefaultPushButton, SIGNAL("clicked()"), self.jobStorageIDDefaultPushButton_clicked)
##
##        self.addWidget(widget, "job_storage_ID")
##
##    def jobStorageIDButtonGroup_clicked(self, a):
##        if a == 0: # Automatic
##            self.jobStorageIDDefaultPushButton.setEnabled(False)
##            self.jobStorageIDEdit.setEnabled(False)
##            self.job_storage_auto_jobname = True
##            self.job_storage_jobname = unicode(time.strftime("%a, %d %b %Y %H:%M:%S"))
##
##        else: # Custom
##            self.jobStorageIDDefaultPushButton.setEnabled(True)
##            self.jobStorageIDEdit.setEnabled(True)
##            self.job_storage_auto_jobname = False
##            self.job_storage_jobname = unicode(self.jobStorageIDEdit.text())
##
##    def jobStorageIDEdit_lostFocus(self):
##        pass
##
##    def jobStorageIDEdit_textChanged(self, a):
##        self.job_storage_jobname = unicode(a)
##
##    def jobStorageIDDefaultPushButton_clicked(self):
##        self.jobStorageIDButtonGroup.setButton(0)
##        self.jobStorageIDDefaultPushButton.setEnabled(False)
##        self.jobStorageIDEdit.setEnabled(False)
##        self.job_storage_auto_jobname = True
##        self.job_storage_jobname = unicode(time.strftime("%a, %d %b %Y %H:%M:%S"))
##
##    # Job ID Exists
##
##    def addJobStorageIDExists(self):
##        widget = self.getWidget()
##
##        layout34 = QHBoxLayout(widget,5,10,"layout34")
##
##        self.jobStorageIDExistsLabel = QLabel(widget,"jobStorageIDExistsLabel")
##        layout34.addWidget(self.jobStorageIDExistsLabel)
##        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
##        layout34.addItem(spacer20_4)
##
##        self.jobStorageIDExistsComboBox = QComboBox(0,widget,"jobStorageIDExistsComboBox")
##        layout34.addWidget(self.jobStorageIDExistsComboBox)
##
##        self.jobStorageIDExistsDefaultPushButton = QPushButton(widget,"pagesetDefaultPushButton")
##        layout34.addWidget(self.jobStorageIDExistsDefaultPushButton)
##
##        self.jobStorageIDExistsLabel.setText(self.__tr("If Job Name already exists:"))
##        self.jobStorageIDExistsComboBox.clear()
##        self.jobStorageIDExistsComboBox.insertItem(self.__tr("Replace existing job"))
##        self.jobStorageIDExistsComboBox.insertItem(self.__tr("Use Job Name + (1-99)"))
##
##        self.jobStorageIDExistsDefaultPushButton.setText(self.__tr("Default"))
##
##        self.connect(self.jobStorageIDExistsComboBox, SIGNAL("activated(int)"), self.jobStorageIDExistsComboBox_activated)
##        self.connect(self.jobStorageIDExistsDefaultPushButton, SIGNAL("clicked()"), self.jobStorageIDExistsDefaultPushButton_clicked)
##
##        self.addWidget(widget, "job_storage_id_exists")
##
##    def jobStorageIDExistsComboBox_activated(self, a):
##        self.jobStorageIDExistsDefaultPushButton.setEnabled(a==1)
##        self.job_storage_job_exist = a
##
##    def jobStorageIDExistsDefaultPushButton_clicked(self):
##        self.jobStorageIDExistsComboBox.setCurrentItem(0)
##        self.jobStorageIDExistsDefaultPushButton.setEnabled(False)
##        self.job_storage_job_exist = 0
##
##
##    #
##    #
##    #

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
                log.debug("number-up = %d" % nup)

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

                    #code = os_utils.execute(cmd)
                    code, out = utils.run(cmd)
                    if code != 0:
                        log.error("Print command failed.")
                        self.form.FailureUI(self.__tr("Print command failed with error code %1").arg(code))

                self.form.close()

        finally:
            self.cur_device.close()

    def funcButton_clicked(self):
        self.form.close()

    def __tr(self,s,c = None):
        return qApp.translate("ScrollPrintView",s,c)
