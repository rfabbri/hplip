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
# Author: Don Welch, Yashwant Kumar Sahu
#

# Local
from base.g import *
from base import utils
from prnt import cups
from jobstoragemixin import JobStorageMixin

# Qt
from qt import *
from scrollview import ScrollView

# Std Lib
import os.path
import os


class RangeValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        for x in unicode(input)[pos-1:]:
            if x not in u'0123456789,- ':
                return QValidator.Invalid, pos

        return QValidator.Acceptable, pos


class OptionComboBox(QComboBox):
    def __init__(self, rw, parent, name, group, option, choices, default, typ=cups.PPD_UI_PICKONE, other=None):
        QComboBox.__init__(self, rw, parent, name)
        self.group = group
        self.option = option
        self.choices = choices
        self.default = default
        self.typ = typ
        self.other = other

    def setDefaultPushbutton(self, pushbutton):
        self.pushbutton = pushbutton

    def setOther(self, other):
        self.other = other


class OptionSpinBox(QSpinBox):
    def __init__(self,  parent, name, group, option, default):
        QSpinBox.__init__(self, parent, name)
        self.group = group
        self.option = option
        self.default = default

    def setDefaultPushbutton(self, pushbutton):
        self.pushbutton = pushbutton


class OptionButtonGroup(QButtonGroup):
    def __init__(self,  parent, name, group, option, default):
        QButtonGroup.__init__(self, parent, name)
        self.group = group
        self.option = option
        self.default = default

    def setDefaultPushbutton(self, pushbutton):
        self.pushbutton = pushbutton


class DefaultPushButton(QPushButton):
    def __init__(self,  parent, name, group, option, choices, default, control, typ):
        QPushButton.__init__(self, parent, name)
        self.group = group
        self.option = option
        self.default = default
        self.control = control
        self.typ = typ
        self.choices = choices



class ScrollPrintSettingsView(ScrollView):
    utils.mixin(JobStorageMixin)

    def __init__(self, service, parent=None, name=None, fl=0):
        ScrollView.__init__(self, service, parent, name, fl)

        self.initJobStorage(True)



    def fillControls(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)

        ScrollView.fillControls(self)

        self.loading = True
        cups.resetOptions()
        cups.openPPD(self.cur_printer)
        cur_outputmode = ""
                
        #if 1:
        try:
            if 1:
            #try:
                current_options = dict(cups.getOptions())

                if not self.cur_device.device_type == DEVICE_TYPE_FAX:
                    self.addGroupHeading("basic", self.__tr("Basic"))
                    log.debug("Group: Basic")

                    # Basic
                        # PageSize (in PPD section)
                        # orientation-requested
                        # sides
                        # outputorder
                        # Collate


                    current = current_options.get('orientation-requested', '3')

                    self.addItem("basic", "orientation-requested", self.__tr("Page Orientation"),
                        cups.PPD_UI_PICKONE, current,
                        [('3', self.__tr('Portrait')),
                         ('4', self.__tr('Landscape')),
                         ('5', self.__tr('Reverse landscape')),
                         ('6', self.__tr('Reverse portrait'))], '3')

                    log.debug("Option: orientation-requested")
                    log.debug("Current value: %s" % current)

                    duplexer = self.cur_device.dq.get('duplexer', 0)
                    log.debug("Duplexer = %d" % duplexer)

                    if duplexer:
                        current = current_options.get('sides', 'one-sided')
                        self.addItem("basic", "sides",
                            self.__tr("Duplex (Print on both sides of the page)"),
                            cups.PPD_UI_PICKONE, current,
                            [('one-sided',self.__tr('Single sided')),
                             ('two-sided-long-edge', self.__tr('Two sided (long edge)')),
                             ('two-sided-short-edge', self.__tr('Two sided (short edge)'))], 'one-sided')

                        log.debug("Option: sides")
                        log.debug("Current value: %s" % current)

                    current = current_options.get('outputorder', 'normal')

                    self.addItem("basic", "outputorder",
                        self.__tr("Output Order (Print last page first)"),
                        cups.PPD_UI_PICKONE, current,
                        [('normal', self.__tr('Normal (Print first page first)')),
                         ('reverse', self.__tr('Reversed (Print last page first)'))], 'normal')

                    log.debug("Option: outputorder")
                    log.debug("Current value: %s" % current)

                    current = utils.to_bool(current_options.get('Collate', '0'))

                    self.addItem("basic", "Collate",
                        self.__tr("Collate (Group together multiple copies)"),
                        cups.PPD_UI_BOOLEAN, current,
                        [], 0)

                    log.debug("Option: Collate")
                    log.debug("Current value: %s" % current)

                groups = cups.getGroupList()

                for g in groups:
                    log.debug("Group: %s" % repr(g))

                    if 'jobretention' in g.lower():
                        log.debug("HPJobRetention skipped.")
                        continue

                    text, num_subgroups = cups.getGroup(g)
                    read_only = 'install' in g.lower()

                    try:
                        text = text.decode('utf-8')
                    except UnicodeDecodeError:
                        pass

                    if g.lower() == 'printoutmode':
                        text = self.__tr("Quality")

                    self.addGroupHeading(g, text, read_only)

                    log.debug("  Text: %s" % repr(text))
                    log.debug("Num subgroups: %d" % num_subgroups)

                    options = cups.getOptionList(g)

                    for o in options:
                        log.debug("  Option: %s" % repr(o))

                        if 'pageregion' in o.lower():
                            log.debug("Page Region skipped.")
                            continue



                        option_text, defchoice, conflicted, ui  = cups.getOption(g, o)

                        try:
                            option_text = option_text.decode('utf-8')
                        except UnicodeDecodeError:
                            pass

                        if o.lower() == 'quality':
                            option_text = self.__tr("Quality")

                        log.debug("    Text: %s" % repr(option_text))
                        log.debug("    Defchoice: %s" % repr(defchoice))

                        choices = cups.getChoiceList(g, o)

                        value = None
                        choice_data = []
                        for c in choices:
                            log.debug("    Choice: %s" % repr(c))

                            # TODO: Add custom paper size controls
                            if 'pagesize' in o.lower() and 'custom' in c.lower():
                                log.debug("Skipped.")
                                continue

                            choice_text, marked = cups.getChoice(g, o, c)

                            try:
                                choice_text = choice_text.decode('utf-8')
                            except UnicodeDecodeError:
                                pass

                            log.debug("      Text: %s" % repr(choice_text))

                            if marked:
                                value = c

                            choice_data.append((c, choice_text))

                        if o.lower() == 'outputmode':
                            if value is not None:
                                cur_outputmode = value
                            else:
                                cur_outputmode = defchoice                                

                        self.addItem(g, o, option_text, ui, value, choice_data, defchoice, read_only)

##                        if 'pagesize' in o.lower(): # and 'custom' in c.lower():
##                            current = 0.0
##                            width_widget = self.addItem("custom", "custom-width", self.__tr("Custom Paper Width"), cups.UI_UNITS_SPINNER,
##                                current, (0.0, 0.0), 0.0)
##
##                            current = 0.0
##                            height_widget = self.addItem("custom", "custom-height", self.__tr("Custom Paper Height"), cups.UI_UNITS_SPINNER,
##                                current, (0.0, 0.0), 0.0)
##
##                            if value.lower() == 'custom':
##                                pass

                # N-Up
                    # number-up
                    # number-up-layout
                    # page-border

                self.addGroupHeading("nup",
                    self.__tr("N-Up (Multiple document pages per printed page)"))

                log.debug("Group: N-Up")

                current = current_options.get('number-up', '1')

                self.addItem("nup", "number-up", self.__tr("Pages per Sheet"),
                    cups.PPD_UI_PICKONE, current,
                    [('1', self.__tr('1 page per sheet')),
                     ('2', self.__tr('2 pages per sheet')),
                     ('4', self.__tr('4 pages per sheet'))], '1')

                log.debug("  Option: number-up")
                log.debug("  Current value: %s" % current)

                current = current_options.get('number-up-layout', 'lrtb')

                self.addItem("nup", "number-up-layout", self.__tr("Layout"),
                    cups.PPD_UI_PICKONE, current,
                    [('btlr', self.__tr('Bottom to top, left to right')),
                     ('btrl', self.__tr('Bottom to top, right to left')),
                     ('lrbt', self.__tr('Left to right, bottom to top')),
                     ('lrtb', self.__tr('Left to right, top to bottom')),
                     ('rlbt', self.__tr('Right to left, bottom to top')),
                     ('rltb', self.__tr('Right to left, top to bottom')),
                     ('tblr', self.__tr('Top to bottom, left to right')),
                     ('tbrl', self.__tr('Top to bottom, right to left')) ], 'lrtb')

                log.debug("  Option: number-up-layout")
                log.debug("  Current value: %s" % current)

                current = current_options.get('page-border', 'none')

                self.addItem("nup", "page-border",
                    self.__tr("Printed Border Around Each Page"),
                    cups.PPD_UI_PICKONE, current,
                    [('double', self.__tr("Two thin borders")),
                     ("double-thick", self.__tr("Two thick borders")),
                     ("none", self.__tr("No border")),
                     ("single", self.__tr("One thin border")),
                     ("single-thick", self.__tr("One thick border"))], 'none')

                log.debug("  Option: page-border")
                log.debug("  Current value: %s" % current)

                # Adjustment
                    # brightness
                    # gamma

                if not self.cur_device.device_type == DEVICE_TYPE_FAX:
                    self.addGroupHeading("adjustment", self.__tr("Printout Appearance"))

                    current = int(current_options.get('brightness', 100))

                    log.debug("  Option: brightness")
                    log.debug("  Current value: %s" % current)

                    self.addItem("adjustment", "brightness", self.__tr("Brightness"),
                        cups.UI_SPINNER, current, (0, 200), 100, suffix=" %")

                    current = int(current_options.get('gamma', 1000))

                    log.debug("  Option: gamma")
                    log.debug("  Current value: %s" % current)

                    self.addItem("adjustment", "gamma", self.__tr("Gamma"), cups.UI_SPINNER, current,
                        (1, 10000), 1000)

                # Margins (pts)
                    # page-left
                    # page-right
                    # page-top
                    # page-bottom

##                if 0:
##                    # TODO: cupsPPDPageSize() fails on LaserJets. How do we get margins in this case? Defaults?
##                    # PPD file for LJs has a HWMargin entry...
##                    page, page_width, page_len, left, bottom, right, top = cups.getPPDPageSize()
##
##                    right = page_width - right
##                    top = page_len - top
##
##                    self.addGroupHeading("margins", self.__tr("Margins"))
##                    current_top = current_options.get('page-top', 0) # pts
##                    current_bottom = current_options.get('page-bottom', 0) # pts
##                    current_left = current_options.get('page-left', 0) # pts
##                    current_right = current_options.get('page-right', 0) # pts
##
##                    log.debug("  Option: page-top")
##                    log.debug("  Current value: %s" % current_top)
##
##                    self.addItem("margins", "page-top", self.__tr("Top margin"),
##                        cups.UI_UNITS_SPINNER, current_top,
##                        (0, page_len), top)
##
##                    self.addItem("margins", "page-bottom", self.__tr("Bottom margin"),
##                        cups.UI_UNITS_SPINNER, current_bottom,
##                        (0, page_len), bottom)
##
##                    self.addItem("margins", "page-left", self.__tr("Right margin"),
##                        cups.UI_UNITS_SPINNER, current_left,
##                        (0, page_width), left)
##
##                    self.addItem("margins", "page-right", self.__tr("Left margin"),
##                        cups.UI_UNITS_SPINNER, current_right,
##                        (0, page_width), right)

                # Image Printing
                    # position
                    # natural-scaling
                    # saturation
                    # hue

                self.addGroupHeading("image", self.__tr("Image Printing"))

                current = utils.to_bool(current_options.get('fitplot', 'false'))

                self.addItem("image", "fitplot",
                    self.__tr("Fit to Page"),
                    cups.PPD_UI_BOOLEAN, current,
                    [], 0)


                current = current_options.get('position', 'center')

                self.addItem("image", "position", self.__tr("Position on Page"),
                    cups.PPD_UI_PICKONE, current,
                    [('center', self.__tr('Centered')),
                     ('top', self.__tr('Top')),
                     ('left', self.__tr('Left')),
                     ('right', self.__tr('Right')),
                     ('top-left', self.__tr('Top left')),
                     ('top-right', self.__tr('Top right')),
                     ('bottom', self.__tr('Bottom')),
                     ('bottom-left', self.__tr('Bottom left')),
                     ('bottom-right', self.__tr('Bottom right'))], 'center')

                log.debug("  Option: position")
                log.debug("  Current value: %s" % current)

                if not self.cur_device.device_type == DEVICE_TYPE_FAX:
                    current = int(current_options.get('saturation', 100))

                    log.debug("  Option: saturation")
                    log.debug("  Current value: %s" % current)

                    self.addItem("image", "saturation", self.__tr("Saturation"),
                        cups.UI_SPINNER, current, (0, 200), 100, suffix=" %")

                    current = int(current_options.get('hue', 0))

                    log.debug("  Option: hue")
                    log.debug("  Current value: %s" % current)

                    self.addItem("image", "hue", self.__tr("Hue (color shift/rotation)"),
                        cups.UI_SPINNER, current,
                        (-100, 100), 0)

                current = int(current_options.get('natural-scaling', 100))

                log.debug("  Option: natural-scaling")
                log.debug("  Current value: %s" % current)

                self.addItem("image", "natural-scaling",
                    self.__tr('"Natural" Scaling (relative to image)'),
                    cups.UI_SPINNER, current, (1, 800), 100, suffix=" %")

                current = int(current_options.get('scaling', 100))

                log.debug("  Option: scaling")
                log.debug("  Current value: %s" % current)

                self.addItem("image", "scaling", self.__tr("Scaling (relative to page)"),
                    cups.UI_SPINNER, current,
                    (1, 800), 100, suffix=" %")

                # Misc
                    # PrettyPrint
                    # job-sheets
                    # mirror

                self.addGroupHeading("misc", self.__tr("Miscellaneous"))

                log.debug("Group: Misc")

                current = utils.to_bool(current_options.get('prettyprint', '0'))

                self.addItem("misc", "prettyprint",
                    self.__tr('"Pretty Print" Text Documents (Add headers and formatting)'),
                    cups.PPD_UI_BOOLEAN, current, [], 0)

                log.debug("  Option: prettyprint")
                log.debug("  Current value: %s" % current)

                if not self.cur_device.device_type == DEVICE_TYPE_FAX:
                    current = current_options.get('job-sheets', 'none').split(',')

                    try:
                        start = current[0]
                    except IndexError:
                        start = 'none'

                    try:
                        end = current[1]
                    except IndexError:
                        end = 'none'

                    # TODO: Look for locally installed banner pages beyond the default CUPS ones?
                    self.addItem("misc", "job-sheets", self.__tr("Banner Pages"), cups.UI_BANNER_JOB_SHEETS,
                        (start, end),
                        [("none", self.__tr("No banner page")),
                         ('classified', self.__tr("Classified")),
                         ('confidential', self.__tr("Confidential")),
                         ('secret', self.__tr("Secret")),
                         ('standard', self.__tr("Standard")),
                         ('topsecret', self.__tr("Top secret")),
                         ('unclassified', self.__tr("Unclassified"))], ('none', 'none'))

                    log.debug("  Option: job-sheets")
                    log.debug("  Current value: %s,%s" % (start, end))

                current = utils.to_bool(current_options.get('mirror', '0'))

                self.addItem("misc", "mirror", self.__tr('Mirror Printing'),
                    cups.PPD_UI_BOOLEAN, current, [], 0)

                log.debug("  Option: mirror")
                log.debug("  Current value: %s" % current)
                
                #Summary
                    #color input
                    #quality
                quality_attr_name = "OutputModeDPI"
                cur_outputmode_dpi = cups.findPPDAttribute(quality_attr_name, cur_outputmode)
                if cur_outputmode_dpi is not None:
                    log.debug("Adding Group: Summary outputmode is : %s" % cur_outputmode)
                    log.debug("Adding Group: Summary outputmode dpi is : %s" % unicode (cur_outputmode_dpi))                
                    self.addGroupHeading("summry", self.__tr("Summary"))
                    self.addItem("summry", "colorinput", self.__tr('Color Input / Black Render'),
                        cups.UI_INFO, cur_outputmode_dpi, [], 0)
                    self.addItem("summry", "quality", self.__tr('Print Quality'),
                        cups.UI_INFO, cur_outputmode, [], 0)
                
                self.job_storage_avail = 0 #self.cur_device.mq['job-storage'] == JOB_STORAGE_ENABLE

                #print current_options

                if self.job_storage_avail:
                    self.addGroupHeading("jobstorage", self.__tr("Job Storage and Secure Printing"))
                    self.addJobStorage(current_options)


            #except Exception, e:
                #log.exception()
            #    pass

        finally:
            cups.closePPD()
            self.loading = False
            QApplication.restoreOverrideCursor()

    def ComboBox_indexChanged(self, currentItem):
        sender = self.sender()
        currentItem = unicode(currentItem)
        # Checking for summary control
        labelPQValaue = getattr(self, 'PQValueLabel', None)
        labelPQColorInput = getattr(self, 'PQColorInputLabel', None)
        # When output mode combo item is changed, we need to update the summary information      
        if currentItem is not None and sender.option == 'OutputMode' and labelPQValaue is not None and labelPQColorInput is not None:
            # Setting output mode
            self.PQValueLabel.setText(currentItem)
            
            # Getting DPI custom attributefrom the PPD
            # Setting color input
            quality_attr_name = "OutputModeDPI"
            cups.openPPD(self.cur_printer)
            outputmode_dpi = cups.findPPDAttribute(quality_attr_name, currentItem)
            log.debug("Outputmode changed, setting outputmode_dpi: %s" % outputmode_dpi)
            cups.closePPD()            
            self.PQColorInputLabel.setText(outputmode_dpi)
            
            log.debug("Outputmode changed, setting value outputmode: %s" % currentItem)            

    def optionComboBox_activated(self, a):
        a = unicode(a)
        sender = self.sender()
        choice = None

        if sender.typ == cups.UI_BANNER_JOB_SHEETS:
            start, end = None, None
            for c, t in sender.choices:
                if t == a:
                    start = c
                    break

            for c, t in sender.other.choices:
                if t == sender.other.currentText():
                    end = c
                    break

            if sender.option == 'end':
                start, end = end, start

            if start is not None and \
                end is not None and \
                start.lower() == sender.default[0].lower() and \
                end.lower() == sender.default[1].lower():
                    self.removePrinterOption('job-sheets')
                    sender.pushbutton.setEnabled(False)
            else:
                sender.pushbutton.setEnabled(True)

                if start is not None and \
                    end is not None:

                    self.setPrinterOption('job-sheets', ','.join([start, end]))

        else:
            choice = None
            for c, t in sender.choices:
                if t == a:
                    choice = c
                    break

            if choice is not None and choice.lower() == sender.default.lower():
                self.removePrinterOption(sender.option)
                sender.pushbutton.setEnabled(False)
            else:
                sender.pushbutton.setEnabled(True)

                if choice is not None:
                    self.setPrinterOption(sender.option, choice)

            self.linkPrintoutModeAndQuality(sender.option, choice)


    def linkPrintoutModeAndQuality(self, option, choice):
        if option.lower() == 'quality' and \
            choice is not None:

            try:
                c = self.items['o:PrintoutMode'].control
            except KeyError:
                return
            else:
                if c is not None:
                    if choice.lower() == 'fromprintoutmode':
                        # from printoutmode selected
                        # determine printoutmode option combo enable state
                        c.setEnabled(True)
                        QToolTip.remove(c)
                        a = unicode(c.currentText())

                        # determine printoutmode default button state
                        link_choice = None
                        for x, t in c.choices:
                            if t == a:
                                link_choice = x
                                break

                        if link_choice is not None and \
                            link_choice.lower() == c.default.lower():

                            c.pushbutton.setEnabled(False)
                        else:
                            c.pushbutton.setEnabled(True)

                    else: # fromprintoutmode not selected, disable printoutmode
                        c.setEnabled(False)
                        QToolTip.add(c, self.__tr("""Set Quality to "Controlled by 'Printout Mode'" to enable."""))
                        c.pushbutton.setEnabled(False)



    def optionSpinBox_valueChanged(self, i):
        sender = self.sender()

        if i == sender.default:
            self.removePrinterOption(sender.option)
            sender.pushbutton.setEnabled(False)
        else:
            sender.pushbutton.setEnabled(True)
            self.setPrinterOption(sender.option, str(i))


    def optionButtonGroup_clicked(self, b):
        sender = self.sender()
        b = int(b)

        if b == sender.default:
            self.removePrinterOption(sender.option)
            sender.pushbutton.setEnabled(False)
        else:
            sender.pushbutton.setEnabled(True)

            if b:
                self.setPrinterOption(sender.option, "true")
            else:
                self.setPrinterOption(sender.option, "false")



    def defaultPushButton_clicked(self):
        sender = self.sender()
        sender.setEnabled(False)

        if sender.typ == cups.PPD_UI_BOOLEAN:
            if sender.default:
                sender.control.setButton(1)
            else:
                sender.control.setButton(0)

            self.removePrinterOption(sender.option)

        elif sender.typ == cups.PPD_UI_PICKONE:
            choice, text = None, None

            for c, t in sender.choices:
                if c == sender.default:
                    choice = c
                    text = t
                    break

            if choice is not None:
                self.removePrinterOption(sender.option)
                sender.control.setCurrentText(text)

                self.linkPrintoutModeAndQuality(sender.option, choice)

        elif sender.typ == cups.UI_SPINNER:
            sender.control.setValue(sender.default)
            self.removePrinterOption(sender.option)

        elif sender.typ == cups.UI_BANNER_JOB_SHEETS:
            start, end, start_text, end_text = None, None, None, None
            for c, t in sender.choices:
                if c == sender.default[0]:
                    start = c
                    start_text = t

                if c == sender.default[1]:
                    end = c
                    end_text = t

            if start is not None:
                sender.control[0].setCurrentText(start_text)

            if end is not None:
                sender.control[1].setCurrentText(end_text)

            self.removePrinterOption('job-sheets')


    def setPrinterOption(self, option, value):
        cups.openPPD(self.cur_printer)

        try:
            cups.addOption("%s=%s" % (option, value))
            cups.setOptions()
        finally:
            cups.closePPD()

    def removePrinterOption(self, option):
        cups.openPPD(self.cur_printer)

        try:
            cups.removeOption(option)
            cups.setOptions()
        finally:
            cups.closePPD()


    def addItem(self, group, option, text, typ, value, choices, default, read_only=False, suffix=""):
        widget, control = None, None

        if typ == cups.PPD_UI_BOOLEAN: # () On (*) Off widget
            widget = self.getWidget()
            layout = QGridLayout(widget, 1, 1, 5, 10, "layout")
            default = int(utils.to_bool(str(default)))
            value = int(utils.to_bool(str(value)))

            textLabel1 = QLabel(widget, "textLabel1")
            layout.addWidget(textLabel1, 0, 0)

            buttonGroup = OptionButtonGroup(widget, "buttonGroup", group, option, default)
            buttonGroup.setLineWidth(0)
            buttonGroup.setColumnLayout(0,Qt.Vertical)
            buttonGroup.layout().setSpacing(1)
            buttonGroup.layout().setMargin(5)
            buttonGroupLayout = QHBoxLayout(buttonGroup.layout())
            buttonGroupLayout.setAlignment(Qt.AlignTop)

            defaultPushButton = DefaultPushButton(widget,"defaultPushButton", group, option,
                choices, default, buttonGroup, typ)

            buttonGroup.setDefaultPushbutton(defaultPushButton)

            layout.addWidget(defaultPushButton, 0, 3)

            spacer1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addItem(spacer1, 0, 1)

            onRadioButton = QRadioButton(buttonGroup,"onRadioButton")
            buttonGroup.insert(onRadioButton, 1)
            buttonGroupLayout.addWidget(onRadioButton)

            offRadioButton = QRadioButton(buttonGroup,"offRadioButton")
            buttonGroup.insert(offRadioButton, 0)
            buttonGroupLayout.addWidget(offRadioButton)

            layout.addWidget(buttonGroup, 0, 2)

            textLabel1.setText(text)
            onRadioButton.setText(self.__tr("On"))
            offRadioButton.setText(self.__tr("Off"))

            if value == default:
                defaultPushButton.setEnabled(False)

            self.connect(defaultPushButton, SIGNAL("clicked()"), self.defaultPushButton_clicked)
            self.connect(buttonGroup, SIGNAL("clicked(int)"), self.optionButtonGroup_clicked)

            x = self.__tr('Off')
            if default:
                x = self.__tr('On')

            if value:
                buttonGroup.setButton(1)
            else:
                buttonGroup.setButton(0)

            if read_only:
                onRadioButton.setEnabled(False)
                offRadioButton.setEnabled(False)
                defaultPushButton.setEnabled(False)
            else:
                QToolTip.add(defaultPushButton, self.__tr('Set to default value of "%1".').arg(x))

            defaultPushButton.setText("Default")

        elif typ == cups.PPD_UI_PICKONE: # Combo box widget
            widget = self.getWidget()

            layout1 = QHBoxLayout(widget,5,10,"layout1")

            textLabel1 = QLabel(widget,"textLabel1")
            layout1.addWidget(textLabel1)

            spacer1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout1.addItem(spacer1)

            optionComboBox = OptionComboBox(0, widget, "optionComboBox", group, option, choices, default)
            layout1.addWidget(optionComboBox)

            defaultPushButton = DefaultPushButton(widget,"defaultPushButton", group, option,
                choices, default, optionComboBox, typ)

            optionComboBox.setDefaultPushbutton(defaultPushButton)

            layout1.addWidget(defaultPushButton)

            textLabel1.setText(text)
            defaultPushButton.setText("Default")

            x, y = None, None
            for c, t in choices:
                d = c.lower()
                if value is not None and d == value.lower():
                    x = t

                if d == default.lower():
                    y = t

                optionComboBox.insertItem(t)

            if x is not None:
                optionComboBox.setCurrentText(x)

            if value is not None and value.lower() == default.lower():
                defaultPushButton.setEnabled(False)

            self.linkPrintoutModeAndQuality(option, value)

            if read_only:
                optionComboBox.setEnabled(False)
                defaultPushButton.setEnabled(False)
            elif y is not None:
                QToolTip.add(defaultPushButton, self.__tr('Set to default value of "%1".').arg(y))

            self.connect(defaultPushButton, SIGNAL("clicked()"), self.defaultPushButton_clicked)
            self.connect(optionComboBox, SIGNAL("activated(const QString&)"), self.optionComboBox_activated)
            self.connect(optionComboBox, SIGNAL("activated(const QString &)"), self.ComboBox_indexChanged)

            control = optionComboBox

        elif typ == cups.UI_SPINNER: # Spinner widget
            widget = self.getWidget()

            layout1 = QHBoxLayout(widget,5,10, "layout1")

            textLabel1 = QLabel(widget, "textLabel1")
            layout1.addWidget(textLabel1)

            spacer1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout1.addItem(spacer1)

            optionSpinBox = OptionSpinBox(widget,"optionSpinBox", group, option, default)
            layout1.addWidget(optionSpinBox)

            defaultPushButton = DefaultPushButton(widget, "defaultPushButton", group, option, choices,
                default, optionSpinBox, typ)

            optionSpinBox.setDefaultPushbutton(defaultPushButton)

            layout1.addWidget(defaultPushButton)

            min, max = choices
            optionSpinBox.setMinValue(min)
            optionSpinBox.setMaxValue(max)
            optionSpinBox.setValue(value)

            if suffix:
                optionSpinBox.setSuffix(suffix)

            textLabel1.setText(text)
            defaultPushButton.setText("Default")

            self.connect(optionSpinBox, SIGNAL("valueChanged(int)"), self.optionSpinBox_valueChanged)
            self.connect(defaultPushButton, SIGNAL("clicked()"), self.defaultPushButton_clicked)

            if value == default:
                defaultPushButton.setEnabled(False)

            if read_only:
                self.optionSpinBox.setEnabled(False)
                self.defaultPushButton.setEnabled()
            else:
                QToolTip.add(defaultPushButton,
                    self.__tr('Set to default value of "%1".').arg(default))

        elif typ == cups.UI_BANNER_JOB_SHEETS:  # Job sheets widget
            widget = self.getWidget()

            layout1 = QGridLayout(widget,1,1,5,10,"layout1")

            startComboBox = OptionComboBox(0, widget, "startComboBox", group,
                "start", choices, default, typ)

            layout1.addWidget(startComboBox,0,3)

            startTextLabel = QLabel(widget,"startTextLabel")
            layout1.addWidget(startTextLabel,0,2)

            endTextLabel = QLabel(widget,"endTextLabel")
            layout1.addWidget(endTextLabel,0,4)

            endComboBox = OptionComboBox(0, widget, "endComboBox", group, "end", choices,
                default, typ, startComboBox)

            layout1.addWidget(endComboBox,0,5)

            startComboBox.setOther(endComboBox)

            defaultPushButton = DefaultPushButton(widget, "defaultPushButton", group, option, choices,
                default, (startComboBox, endComboBox), typ)

            layout1.addWidget(defaultPushButton,0,6)

            startComboBox.setDefaultPushbutton(defaultPushButton)
            endComboBox.setDefaultPushbutton(defaultPushButton)

            textLabel1 = QLabel(widget,"textLabel1")
            layout1.addWidget(textLabel1,0,0)

            spacer1 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
            layout1.addItem(spacer1,0,1)

            textLabel1.setText(text)
            defaultPushButton.setText("Default")

            startTextLabel.setText(self.__tr("Start:"))
            endTextLabel.setText(self.__tr("End:"))

            s, e, y, z = None, None, None, None
            for c, t in choices:
                d = c.lower()
                if value is not None:
                    if d == value[0].lower():
                        s = t

                    if d == value[1].lower():
                        e = t

                if d == default[0].lower():
                    y = t

                if d == default[1].lower():
                    z = t

                startComboBox.insertItem(t)
                endComboBox.insertItem(t)

            if s is not None:
                startComboBox.setCurrentText(s)

            if e is not None:
                endComboBox.setCurrentText(e)

            if value is not None and \
                value[0].lower() == default[0].lower() and \
                value[1].lower() == default[1].lower():

                defaultPushButton.setEnabled(False)

            if y is not None and z is not None:
                QToolTip.add(defaultPushButton, self.__tr('Set to default value of "Start: %1, End: %2".').arg(y).arg(z))

            self.connect(startComboBox, SIGNAL("activated(const QString&)"), self.optionComboBox_activated)
            self.connect(endComboBox, SIGNAL("activated(const QString&)"), self.optionComboBox_activated)
            self.connect(defaultPushButton, SIGNAL("clicked()"), self.defaultPushButton_clicked)

        elif typ == cups.PPD_UI_PICKMANY:
            log.error("Unrecognized type: pickmany")

        elif typ == cups.UI_UNITS_SPINNER:
            widget = self.getWidget()

            layout1 = QHBoxLayout(widget,5,10,"layout1")

            textLabel1 = QLabel(widget,"textLabel1")
            layout1.addWidget(textLabel1)

            spacer1 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
            layout1.addItem(spacer1)

            lineEdit1 = QLineEdit(widget,"lineEdit1")
            layout1.addWidget(lineEdit1)

            comboBox1 = QComboBox(0,widget,"comboBox1")
            layout1.addWidget(comboBox1)

            defaultPushButton = QPushButton(widget,"defaultPushButton")
            layout1.addWidget(defaultPushButton)

            textLabel1.setText(text)
            defaultPushButton.setText("Default")

        elif typ == cups.UI_INFO:
            widget = self.getWidget()

            layout1 = QHBoxLayout(widget,5,10,"layout1")

            textPropName = QLabel(widget,"textPropName")
            layout1.addWidget(textPropName)
            textPropName.setText(text)            

            spacer1 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
            layout1.addItem(spacer1)
            
            if text == 'Print Quality':
                self.PQValueLabel = QLabel(widget,"textPropValue")
                layout1.addWidget(self.PQValueLabel)
                self.PQValueLabel.setText(value)
            elif text == 'Color Input / Black Render':
                self.PQColorInputLabel = QLabel(widget,"textPropValue")
                layout1.addWidget(self.PQColorInputLabel)
                self.PQColorInputLabel.setText(value)
            else:
                textPropValue = QLabel(widget,"textPropValue")
                layout1.addWidget(textPropValue)
                textPropValue.setText(value)
            
        else:
            log.error("Invalid UI value: %s/%s" % (group, option))

        if widget is not None:
            self.addWidget(widget, "o:"+option, control)
            return widget



    def __tr(self,s,c = None):
        return qApp.translate("ScrollPrintSettingsView",s,c)
