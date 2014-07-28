# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2007 Hewlett-Packard Development Company, L.P.
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
from base import utils, pml
from copier import copier

# Qt
from qt import *
from scrollview import ScrollView, PixmapLabelButton
from waitform import WaitForm

# Std Lib
import os.path, os
import Queue


class ScrollCopyView(ScrollView):
    def __init__(self, service, num_copies=None, contrast=None, quality=None,
                reduction=None, fit_to_page=None, parent=None, form=None, name=None, fl=0):
        ScrollView.__init__(self, service, parent, name, fl)

        self.form = form

        self.num_copies = num_copies
        self.contrast = contrast
        self.quality = quality
        self.reduction = reduction
        self.fit_to_page = fit_to_page

        self.update_queue = Queue.Queue() # UI updates from copy thread
        self.event_queue = Queue.Queue() # UI events to copy thread

    def getDeviceSettings(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            # get sticky settings as defaults (if not spec'd on command line)
            if self.num_copies is None:
                result_code, self.num_copies = self.dev.getPML(pml.OID_COPIER_NUM_COPIES)

            if self.contrast is None:
                result_code, self.contrast = self.dev.getPML(pml.OID_COPIER_CONTRAST)

            if self.reduction is None:
                result_code, self.reduction = self.dev.getPML(pml.OID_COPIER_REDUCTION)

            if self.quality is None:
                result_code, self.quality = self.dev.getPML(pml.OID_COPIER_QUALITY)

            if self.scan_src == SCAN_SRC_FLATBED and self.fit_to_page is None:
                result_code, self.fit_to_page = self.dev.getPML(pml.OID_COPIER_FIT_TO_PAGE)

                if result_code != pml.ERROR_OK:
                    self.fit_to_page = pml.COPIER_FIT_TO_PAGE_DISABLED
                    self.fitToPageCheckBox.setEnabled(False)

            else:
                self.fit_to_page = pml.COPIER_FIT_TO_PAGE_DISABLED

            if self.scan_src != SCAN_SRC_FLATBED:
                self.fitToPageCheckBox.setEnabled(False)

            result_code, self.max_reduction = self.dev.getPML(pml.OID_COPIER_REDUCTION_MAXIMUM)
            result_code, self.max_enlargement = self.dev.getPML(pml.OID_COPIER_ENLARGEMENT_MAXIMUM)

            # contrast
            a = self.contrast/25
            self.contrastSpinBox.setValue(a)

            if a >= 0:
                self.contrastSpinBox.setPrefix("+")
            else:
                self.contrastSpinBox.setPrefix("")

            self.contrastSlider.setValue(a)
            self.contrastSlider.setTickmarks(QSlider.Below)
            self.contrastSlider.setTickInterval(1)

            self.contrastDefaultPushButton.setEnabled(a != 0)

            # reduction/enlargement/fittopage

            self.reductionSlider.setRange(self.max_reduction, self.max_enlargement)
            self.reductionSlider.setTickmarks(QSlider.Below)
            self.reductionSlider.setTickInterval(10)
            self.reductionSlider.setValue(self.reduction)

            self.reductionSpinBox.setMaxValue(self.max_enlargement)
            self.reductionSpinBox.setMinValue(self.max_reduction)
            self.reductionSpinBox.setValue(self.reduction)
            self.reductionSpinBox.setSuffix("%")

            if self.fit_to_page == pml.COPIER_FIT_TO_PAGE_ENABLED:
                self.fitToPageCheckBox.setChecked(True)
                self.reductionSpinBox.setEnabled(False)
                self.reductionSlider.setEnabled(False)
                self.reductionDefaultPushButton.setEnabled(True)
            else:
                self.fitToPageCheckBox.setChecked(False)
                self.reductionSlider.setEnabled(True)
                self.reductionSpinBox.setEnabled(True)
                self.reductionDefaultPushButton.setEnabled(self.reduction != 100)

            # num_copies
            self.copiesSpinBox.setValue(self.num_copies)
            self.copiesDefaultPushButton.setEnabled(self.num_copies != 1)

            # quality
            if self.quality == pml.COPIER_QUALITY_FAST:
                self.qualityComboBox.setCurrentItem(0)
                s = 'Fast'

            elif self.quality == pml.COPIER_QUALITY_DRAFT:
                self.qualityComboBox.setCurrentItem(1)
                s = 'Draft'

            elif self.quality == pml.COPIER_QUALITY_NORMAL:
                self.qualityComboBox.setCurrentItem(2)
                s = 'Normal'

            elif self.quality == pml.COPIER_QUALITY_PRESENTATION:
                self.qualityComboBox.setCurrentItem(3)
                s = 'Presentation'

            elif self.quality == pml.COPIER_QUALITY_BEST:
                self.qualityComboBox.setCurrentItem(4)
                s = 'Best'

            log.debug("Default Quality: %d (%s)" % (self.quality, s))

            self.qualityDefaultPushButton.setEnabled(self.quality != pml.COPIER_QUALITY_NORMAL)

            log.debug("Default Num copies: %d" % self.num_copies)
            log.debug("Default Contrast: %d" % self.contrast)
            log.debug("Default Reduction: %d" % self.reduction)
            log.debug("Maximum Reduction: %d" % self.max_reduction)
            log.debug("Maximum Enlargement: %d" % self.max_enlargement)

            if self.fit_to_page == pml.COPIER_FIT_TO_PAGE_ENABLED:
                s = 'Enabled'  # 2
            else:
                s = 'Disabled' # 1

            log.debug("Default Fit to page: %s (%s)" % (self.fit_to_page, s))
            log.debug("Scan src (models.dat: scan-src): %d" % self.scan_src)

        finally:
            self.dev.closePML()
            QApplication.restoreOverrideCursor()


    def fillControls(self):
        ScrollView.fillControls(self)

        self.addGroupHeading("copies", self.__tr("Number of Copies"))
        self.addCopies()

        self.addGroupHeading("reduction", self.__tr("Enlargement, Reduction and Fit to Page"))
        self.addEnlargementReduction()

        self.addGroupHeading("contrast", self.__tr("Copy Contrast"))
        self.addContrast()

        self.addGroupHeading("quality", self.__tr("Copy Quality"))
        self.addQuality()

        self.addGroupHeading("space1", "")

        self.copyButton = self.addActionButton("bottom_nav", self.__tr("Make Copies(s)"),
                                self.copyButton_clicked, 'print.png', 'print.png',
                                self.__tr("Close"), self.funcButton_clicked)



    def onUpdate(self, cur_device=None):
        log.debug("ScrollPrintView.onUpdate()")

    def onDeviceChange(self, cur_device=None):
        ScrollView.onDeviceChange(self, cur_device)

        self.dev = copier.PMLCopyDevice(device_uri=self.cur_device.device_uri,
                                        printer_name=self.cur_printer)

        self.scan_src = self.dev.mq.get('scan-src', SCAN_SRC_FLATBED)
        self.copy_type = self.dev.mq.get('copy-type', COPY_TYPE_DEVICE)

        if self.scan_src == SCAN_SRC_SCROLLFED:
            self.fitToPageCheckBox.setEnabled(False)
            self.fit_to_page = pml.COPIER_FIT_TO_PAGE_DISABLED

        self.getDeviceSettings()


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
        self.num_copies = i

    def addQuality(self):
        widget = self.getWidget()
        layout34 = QHBoxLayout(widget,5,10,"layout34")

        self.textLabel5_4 = QLabel(widget,"textLabel5_4")
        self.textLabel5_4.setText(self.__tr("Quality:"))
        layout34.addWidget(self.textLabel5_4)

        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout34.addItem(spacer20_4)

        self.qualityComboBox = QComboBox(0,widget,"qualityComboBox")
        layout34.addWidget(self.qualityComboBox)

        self.qualityDefaultPushButton = QPushButton(widget,"qualityDefaultPushButton")
        layout34.addWidget(self.qualityDefaultPushButton)

        self.qualityComboBox.clear()
        self.qualityComboBox.insertItem(self.__tr("Fast")) # 0
        self.qualityComboBox.insertItem(self.__tr("Draft")) # 1
        self.qualityComboBox.insertItem(self.__tr("Normal")) # 2
        self.qualityComboBox.insertItem(self.__tr("Presentation")) # 3
        self.qualityComboBox.insertItem(self.__tr("Best")) # 4
        self.qualityComboBox.setCurrentItem(2) # Normal

        self.qualityDefaultPushButton.setText(self.__tr("Default"))
        self.qualityDefaultPushButton.setEnabled(False)

        self.connect(self.qualityComboBox, SIGNAL("activated(int)"), self.qualityComboBox_activated)
        self.connect(self.qualityDefaultPushButton, SIGNAL("clicked()"), self.qualityDefaultPushButton_clicked)

        self.addWidget(widget, "quality")

    def qualityDefaultPushButton_clicked(self):
        self.qualityDefaultPushButton.setEnabled(False)
        self.qualityComboBox.setCurrentItem(2) # Normal
        self.quality = pml.COPIER_QUALITY_NORMAL

    def qualityComboBox_activated(self, i):
        self.qualityDefaultPushButton.setEnabled(i != 2) # Normal

        if i == 0:
            self.quality = pml.COPIER_QUALITY_FAST
        elif i == 1:
            self.quality = pml.COPIER_QUALITY_DRAFT
        elif i == 2:
            self.quality = pml.COPIER_QUALITY_NORMAL
        elif i == 3:
            self.quality = pml.COPIER_QUALITY_PRESENTATION
        elif i == 4:
            self.quality = pml.COPIER_QUALITY_BEST


    def addEnlargementReduction(self):
        widget = self.getWidget()
        layout43 = QGridLayout(widget,1,1,5,10,"layout43")

        self.reductionSlider = QSlider(widget,"reductionSlider")
        self.reductionSlider.setOrientation(QSlider.Horizontal)

        layout43.addWidget(self.reductionSlider,0,2)

        self.reductionSpinBox = QSpinBox(widget, "reductionSpinBox")
        self.reductionSpinBox.setMaxValue(100)
        self.reductionSpinBox.setMinValue(0)
        self.reductionSpinBox.setValue(100)
        self.reductionSpinBox.setSuffix("%")
        layout43.addWidget(self.reductionSpinBox,0,3)

        spacer42 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout43.addItem(spacer42,0,1)

        self.fitToPageCheckBox = QCheckBox(widget,"fitToPageCheckBox")
        layout43.addWidget(self.fitToPageCheckBox,1,2)

        self.reductionDefaultPushButton = QPushButton(widget,"reductionDefaultPushButton")
        layout43.addWidget(self.reductionDefaultPushButton,0,4)

        self.textLabel1 = QLabel(widget,"textLabel1")
        layout43.addWidget(self.textLabel1,0,0)

        self.textLabel1.setText(self.__tr("Enlargement or reduction (percent):"))
        self.fitToPageCheckBox.setText(self.__tr("Fit to Page"))
        self.reductionDefaultPushButton.setText(self.__tr("Default"))

        self.reductionSlider.setRange(25, 400)

        self.connect(self.reductionSlider,SIGNAL("valueChanged(int)"),self.reductionSlider_valueChanged)
        self.connect(self.fitToPageCheckBox,SIGNAL("clicked()"),self.fitToPageCheckBox_clicked)
        self.connect(self.reductionDefaultPushButton, SIGNAL("clicked()"), self.reductionDefaultPushButton_clicked)
        self.connect(self.reductionSpinBox, SIGNAL("valueChanged(int)"), self.reductionSpinBox_valueChanged)

        self.addWidget(widget, "reduction")

    def reductionSlider_valueChanged(self,a0):
        self.reduction = a0
        self.reductionSpinBox.setValue(a0)
        self.reductionDefaultPushButton.setEnabled(a0 != 100)

    def reductionSpinBox_valueChanged(self, a0):
        self.reduction = a0
        self.reductionSlider.setValue(a0)
        self.reductionDefaultPushButton.setEnabled(a0 != 100)

    def fitToPageCheckBox_clicked(self):
        if self.fitToPageCheckBox.isChecked():
            self.fit_to_page = pml.COPIER_FIT_TO_PAGE_ENABLED
            self.reductionSpinBox.setEnabled(False)
            self.reductionSlider.setEnabled(False)
            self.reductionDefaultPushButton.setEnabled(True)
        else:
            self.fit_to_page = pml.COPIER_FIT_TO_PAGE_DISABLED
            self.reductionSlider.setEnabled(True)
            self.reductionSpinBox.setEnabled(True)
            self.reductionDefaultPushButton.setEnabled(self.reductionSlider.value() != 100)

    def reductionDefaultPushButton_clicked(self):
        self.reduction = 100
        self.reductionSlider.setValue(100)
        self.reductionSlider.setEnabled(True)
        self.reductionSpinBox.setValue(100)
        self.reductionSpinBox.setEnabled(True)
        self.fitToPageCheckBox.setChecked(False)
        self.fit_to_page = False

    def addContrast(self):
        widget = self.getWidget()

        layout41 = QGridLayout(widget,1,1,5,10,"layout41")

        self.textLabel1_2 = QLabel(widget,"textLabel1_2")

        layout41.addWidget(self.textLabel1_2,0,0)

        self.contrastDefaultPushButton = QPushButton(widget,"contrastDefaultPushButton")

        layout41.addWidget(self.contrastDefaultPushButton,0,4)
        spacer41 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout41.addItem(spacer41,0,1)

        self.contrastSlider = QSlider(widget,"contrastSlider")
        self.contrastSlider.setMinValue(-5)
        self.contrastSlider.setMaxValue(5)
        self.contrastSlider.setPageStep(1)
        self.contrastSlider.setOrientation(QSlider.Horizontal)

        layout41.addWidget(self.contrastSlider,0,2)

        self.contrastSpinBox = QSpinBox(widget, "contrastSpinBox")
        self.contrastSpinBox.setMinValue(-5)
        self.contrastSpinBox.setMaxValue(5)

        layout41.addWidget(self.contrastSpinBox,0,3)

        self.textLabel1_2.setText(self.__tr("Contrast (-5 lighter to +5 darker):"))
        self.contrastDefaultPushButton.setText(self.__tr("Default"))

        self.connect(self.contrastSlider,SIGNAL("valueChanged(int)"),self.contrastSlider_valueChanged)
        self.connect(self.contrastSpinBox, SIGNAL("valueChanged(int)"), self.contrastSpinBox_valueChanged)
        self.connect(self.contrastDefaultPushButton, SIGNAL("clicked()"), self.contrastDefaultPushButton_clicked)

        self.addWidget(widget, "contrast")


    def contrastSlider_valueChanged(self, a0):
        self.contrastSpinBox.setValue(a0)
        self.contrast = a0 * 25
        self.contrastDefaultPushButton.setEnabled(a0 != 0)

    def contrastSpinBox_valueChanged(self, a0):
        if a0 >= 0:
            self.contrastSpinBox.setPrefix("+")
        else:
            self.contrastSpinBox.setPrefix("")

        self.contrastSlider.setValue(a0)
        self.contrast = a0 * 25
        self.contrastDefaultPushButton.setEnabled(a0 != 0)

    def contrastDefaultPushButton_clicked(self):
        self.contrastSpinBox.setValue(0)
        self.contrastSpinBox.setPrefix("+")
        self.contrastSlider.setValue(0)
        self.contrast = 0


    def copy_canceled(self):
        self.event_queue.put(copier.COPY_CANCELED)
        self.dev.sendEvent(EVENT_COPY_JOB_CANCELED)

    def copy_timer_timeout(self):
        while self.update_queue.qsize():
            try:
                status = self.update_queue.get(0)
            except Queue.Empty:
                break

            if status == copier.STATUS_IDLE:
                self.copy_timer.stop()

                #self.pb.hide()
                #self.form.statusBar().removeWidget(self.pb)

            elif status in (copier.STATUS_SETTING_UP, copier.STATUS_WARMING_UP):
                #self.pb.setProgress(self.pb.progress()+1)
                pass

            elif status == copier.STATUS_ACTIVE:
                #self.pb.setProgress(self.pb.progress()+1)
                pass

            elif status in (copier.STATUS_ERROR, copier.STATUS_DONE):
                self.copy_timer.stop()
                #self.pb.hide()
                #self.form.statusBar().removeWidget(self.pb)

                # Close the dialog box.
                #
                if self.waitdlg is not None:
                    self.waitdlg.hide()
                    self.waitdlg.close()
                    self.waitdlg = None

                if status == copier.STATUS_ERROR:
                    self.form.FailureUI(self.__tr("<b>Copier error.</b><p>"))
                    self.dev.sendEvent(EVENT_COPY_JOB_FAIL)

                elif status == copier.STATUS_DONE:
                    pass
                    self.dev.sendEvent(EVENT_END_COPY_JOB)

                self.cur_device.close()
                self.copyButton.setEnabled(True)

                self.form.close()


    def copyButton_clicked(self):
        self.copyButton.setEnabled(False)
        try:
            try:
                self.dev.open()
            except Error:
                self.form.FailureUI(self.__tr("<b>Cannot copy: Device is busy or not available.</b><p>Please check device and try again. [1]"))
                return

            self.dev.sendEvent(EVENT_START_COPY_JOB, self.cur_printer, 0, '')
            #self.pb = QProgressBar()
            #self.pb.setTotalSteps(2)
            #self.form.statusBar().addWidget(self.pb)
            #self.pb.show()

            log.debug("Num copies: %d" % self.num_copies)
            log.debug("Contrast: %d" % self.contrast)
            log.debug("Reduction: %d" % self.reduction)

            s = 'Normal'
            if self.quality == pml.COPIER_QUALITY_FAST:
                s = 'Fast'
            elif self.quality == pml.COPIER_QUALITY_DRAFT:
                s = 'Draft'
            elif self.quality == pml.COPIER_QUALITY_NORMAL:
                s = 'Normal'
            elif self.quality == pml.COPIER_QUALITY_PRESENTATION:
                s = 'Presentation'
            elif self.quality == pml.COPIER_QUALITY_BEST:
                s = 'Best'

            log.debug("Quality: %d (%s)" % (self.quality, s))

            if self.fit_to_page == pml.COPIER_FIT_TO_PAGE_ENABLED:
                s = 'Enabled'  # 2
            else:
                s = 'Disabled' # 1

            log.debug("Fit to page: %s (%s)" % (self.fit_to_page, s))
            log.debug("Scan src: %d" % self.scan_src)

            # Open the dialog box.
            #
            self.waitdlg = WaitForm(0, self.__tr("Copying..."), self.copy_canceled, self, modal=1)
            self.waitdlg.show()

            self.copy_timer = QTimer(self, "CopyTimer")
            self.connect(self.copy_timer, SIGNAL('timeout()'), self.copy_timer_timeout)
            self.copy_timer.start(1000) # 1 sec UI updates

            self.dev.copy(self.num_copies, self.contrast, self.reduction,
                          self.quality, self.fit_to_page, self.scan_src,
                          self.update_queue, self.event_queue)

        finally:
            #self.cur_device.close()
            #self.copyButton.setEnabled(True)
            pass

    def funcButton_clicked(self):
        self.dev.close()
        self.form.close()

    def __tr(self,s,c = None):
        return qApp.translate("ScrollCopy",s,c)
