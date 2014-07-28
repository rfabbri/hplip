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

# Std Lib

# Local
from base.g import *
from prnt import cups
from base import device
from ui_utils import load_pixmap

# Qt
from qt import *



class Widget(QWidget):
    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)
        self.control = None

    def setControl(self, control):
        self.control = control



class ScrollView(QScrollView):
    def __init__(self, service=None, parent=None, name=None, fl=0):
        QScrollView.__init__(self, parent, name, fl)

        self.service = service
        self.items = {}
        self.enableClipper(True)
        self.viewport().setPaletteBackgroundColor(qApp.palette().color(QPalette.Active, QColorGroup.Background))
        self.cur_device = None
        self.cur_printer = None
        self.item_margin = 2
        self.y = 0
        self.printers = []
        self.maximize = None
        self.orig_height = 0
        self.content_padding = 20

        if log.is_debug():
            self.heading_color = qApp.palette().color(QPalette.Active, QColorGroup.Base)
            self.frame_shape = QFrame.Box
        else:
            self.heading_color = qApp.palette().color(QPalette.Active, QColorGroup.Background)            
            self.frame_shape = QFrame.NoFrame

    def getWidget(self):
        widget = Widget(self.viewport(),"widget")
        widget.setPaletteBackgroundColor(qApp.palette().color(QPalette.Active, QColorGroup.Background))
        return widget

    def viewportResizeEvent(self, e):
        QScrollView.viewportResizeEvent(self, e)

        total_height = 0
        item_margin = self.item_margin
        width = e.size().width()

        for w in self.items:
            height  = self.items[w].size().height()
            self.items[w].resize(width, height)
            self.items[w].setMinimumWidth(width)
            total_height += (height + item_margin)

        if self.maximize is not None:
            self.maximizeControl(total_height)

        self.resizeContents(e.size().width(), total_height + self.content_padding)

    def maximizeControl(self, total_height=0):
        if self.maximize is not None:
            try:
                self.items[self.maximize]
            except KeyError:
                return
                
            if total_height == 0:
                item_margin = self.item_margin
                for w in self.items:
                    total_height += (self.items[w].size().height() + item_margin)
                    
            if len(self.items) == 1:
                #total_height += item_margin
                self.content_padding = 0

            width = self.items[self.maximize].size().width()
            old_height = self.items[self.maximize].size().height()

            new_height = max((self.visibleHeight()-(total_height-old_height)), 
                self.orig_height)

            delta = new_height - old_height

            if delta:
                self.items[self.maximize].resize(width, new_height)
                self.resizeContents(width, self.contentsHeight()+delta+self.content_padding)
                m_y = self.childY(self.items[self.maximize])

                for w in self.items:
                    w_y = self.childY(self.items[w])
                    if w_y > m_y:
                        self.moveChild(self.items[w], 0, w_y+delta)


    def onDeviceChange(self, cur_device=None, updating=False):
        if cur_device is not None:
            log.debug("ScrollView.onDeviceChange(%s)" % cur_device.device_uri)
        else:
            log.debug("ScrollView.onDeviceChange(None)")

        self.cur_device = cur_device

        if self.cur_device is not None and self.cur_device.supported:
            #if not updating or not self.cur_printer:
            if not self.cur_printer:
                try:
                    cur_printer = self.cur_device.cups_printers[0]
                except IndexError:
                    log.error("Printer list empty") # Shouldn't happen!
                    self.cur_printer = None
                    return
               
                #self.isFax()
                self.printers = cups.getPrinters()
                self.onPrinterChange(cur_printer)
                self.cur_printer = cur_printer

            #else:
            if 1:
                QApplication.setOverrideCursor(QApplication.waitCursor)
                try:
                    if 1:
                    #try:
                        self.fillControls()
                    #except Exception, e:
                    #    log.exception()
                finally:
                    QApplication.restoreOverrideCursor()

        else:
            log.debug("Unsupported device")
            self.y = 0
            self.clear()

            self.addGroupHeading("error", self.__tr("ERROR: No device found or unsupported device."))

    def onUpdate(self, cur_device=None):
        log.debug("ScrollView.onUpdate()")
        return self.onDeviceChange(cur_device, True)

    def fillControls(self):
        log.debug("fillControls(%s)" % str(self.name()))
        self.y = 0
        self.clear()

    def onPrinterChange(self, printer_name):
        if printer_name == self.cur_printer or printer_name is None:
            return

        self.cur_printer = unicode(printer_name)

        if self.cur_device is not None and self.cur_device.supported:
            #self.isFax()
            QApplication.setOverrideCursor(QApplication.waitCursor)
            try:
                if 1:
                #try:
                    self.fillControls()
                #except Exception, e:
                #    log.exception()
            finally:
                QApplication.restoreOverrideCursor()

            if self.cur_printer is not None:
                try:
                    self.printerComboBox.setCurrentText(self.cur_printer)
                except AttributeError:
                    pass

        else:
            self.y = 0
            self.clear()

    def addWidget(self, widget, key, control=None, maximize=False):
        try:
            self.items[key]
        except KeyError:
            if maximize:
                self.maximize = key
                widget.resize(widget.size().width(), 150)
                self.orig_height = widget.size().height()

            try:
                widget.setControl(control)
            except AttributeError:
                pass
            self.items[key] = widget
            widget.setMinimumWidth(self.visibleWidth())
            widget.adjustSize()
            self.addChild(widget, 0, self.y)
            self.y += (widget.size().height() + self.item_margin)
            self.resizeContents(self.visibleWidth(), self.y + self.content_padding)
            widget.show()
        #else:
        #    log.debug("ERROR: Duplicate control name: %s" % key)

    def clear(self):
        if len(self.items):
            for x in self.items:
                self.removeChild(self.items[x])
                self.items[x].hide()

            self.items.clear()

    def addGroupHeading(self, group, heading, read_only=False):
        widget = self.getWidget()
        widget.setMinimumHeight(30)

        layout = QGridLayout(widget, 0, 0, 5, 0, "layout")
        textLabel2 = QLabel(widget, "textLabel2")

        textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, 
            QSizePolicy.Maximum, 0, 0,
            textLabel2.sizePolicy().hasHeightForWidth()))

        if log.is_debug():
            textLabel2.setFrameShape(self.frame_shape)

        elif heading:
            textLabel2.setFrameShape(QFrame.TabWidgetPanel)
            textLabel2.setPaletteBackgroundColor(self.heading_color)

        if read_only:
            s = self.__tr("<b>%1 (read only)</b>").arg(heading) # <nobr>
        else:  
            s = QString("<b>%1</b>").arg(heading)

        # If label is kinda long, provide a tooltip to allow reading the whole thing
        if s.length() > 32:
            QToolTip.add(textLabel2, s)

        textLabel2.setText(s)
        textLabel2.setAlignment(QLabel.AlignLeft | QLabel.AlignVCenter | Qt.SingleLine)

        layout.addWidget(textLabel2, 0, 0)

        self.addWidget(widget, "g:"+unicode(group))


    def addActionButton(self, name, action_text, action_func, 
                        action_pixmap=None, disabled_action_pixmap=None,
                        nav_text ='', nav_func=None):

        widget = self.getWidget()

        self.actionPushButton = None
        self.navPushButton = None

        layout36 = QHBoxLayout(widget,5,10,"layout36")

        if nav_func is not None:
            self.navPushButton = QPushButton(widget,"navPushButton")
            navPushButton_font = QFont(self.navPushButton.font())
            navPushButton_font.setBold(1)
            self.navPushButton.setFont(navPushButton_font)
            self.navPushButton.setText(nav_text)
            layout36.addWidget(self.navPushButton)

            self.connect(self.navPushButton, SIGNAL("clicked()"), nav_func)

        spacer35 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout36.addItem(spacer35)

        if action_func is not None:
            if action_pixmap is None:
                self.actionPushButton = QPushButton(widget, "actionPushButton")
            else:
                self.actionPushButton = PixmapLabelButton(widget, action_pixmap, 
                    disabled_action_pixmap, 'actionPushButton')

            actionPushButton_font = QFont(self.actionPushButton.font())
            actionPushButton_font.setBold(1)
            self.actionPushButton.setFont(actionPushButton_font)
            layout36.addWidget(self.actionPushButton)

            self.actionPushButton.setText(action_text)

            self.connect(self.actionPushButton, SIGNAL("clicked()"), action_func)

        self.addWidget(widget, name)

        if self.actionPushButton is not None:
            return self.actionPushButton

        elif self.navPushButton is not None:
            return self.navPushButton

        else:
            return None

    def printerComboBox_activated(self, p):
        self.cur_printer = str(p)

    def addPrinterFaxList(self): # printers=True, faxes=False):
        widget = self.getWidget()

        layout = QGridLayout(widget,1,1,5,10,"layout")

        self.printernameTextLabel = QLabel(widget,"printernameTextLabel")
        layout.addWidget(self.printernameTextLabel,0,0)

        self.printerComboBox = QComboBox(0,widget,"printerComboBox")
        layout.addWidget(self.printerComboBox,0,1)

        #print self.cur_device.device_type
        if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
            self.addGroupHeading("printer_list_heading", self.__tr("Printer"))
            self.printernameTextLabel.setText(self.__tr("Printer Name:"))
        else:
            self.addGroupHeading("fax_list_heading", self.__tr("Fax"))
            self.printernameTextLabel.setText(self.__tr("Fax Name:"))

        self.printers = cups.getPrinters()
        self.cur_printer = None
        for p in self.printers:
            if p.device_uri == self.cur_device.device_uri:

                self.printerComboBox.insertItem(p.name)

                if self.cur_printer is None:
                    self.cur_printer = p.name

        if self.cur_printer is None:
            #log.error("No fax queue found")
            self.y = 0
            self.clear()

            #if printers and faxes:
            if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                self.addGroupHeading("error", self.__tr("ERROR: No CUPS queue found for device."))
            else:
                self.addGroupHeading("error", self.__tr("ERROR: No CUPS fax queue found for device."))

            return False

        else:
            self.connect(self.printerComboBox, SIGNAL("activated(const QString&)"), self.printerComboBox_activated)

            self.addWidget(widget, "printer_list")
            return True


    def addLoadPaper(self, paper_type=PAPER_TYPE_PLAIN):
        self.addGroupHeading("load_paper", self.__tr("Load Paper"))

        widget = self.getWidget()
        layout1 = QGridLayout(widget, 1, 2, 5, 10,"layout1")

        layout1.setColStretch(0, 1)
        layout1.setColStretch(1, 10)

        icon = QLabel(widget, "icon")
        icon.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed, 0, 0,
            icon.sizePolicy().hasHeightForWidth()))

        icon.setScaledContents(1)
        layout1.addWidget(icon, 0, 0)

        textLabel = QLabel(widget, "textLabel")
        textLabel.setAlignment(QLabel.WordBreak)
        textLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred, 0, 0,
            textLabel.sizePolicy().hasHeightForWidth()))        
        textLabel.setFrameShape(self.frame_shape)
        layout1.addWidget(textLabel, 0, 1)

        spacer1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout1.addItem(spacer1, 0, 2)

        if paper_type == PAPER_TYPE_PLAIN:
            textLabel.setText(self.__tr("A page will be printed. Please load Letter/A4 <b>Plain Paper</b> into the printer."))
        elif paper_type == PAPER_TYPE_HP_ADV_PHOTO:
            textLabel.setText(self.__tr("A page will be printed. Please load Letter/A4 <b>HP Advanced Photo Paper - Glossy</b> into the printer."))

        icon.setPixmap(load_pixmap("load_paper", 'other'))

        self.addWidget(widget, "load_paper")

        
    def cleanup(self):
        pass
        
    def __tr(self,s,c = None):
        return qApp.translate("ScrollView",s,c)



class PixmapLabelButton(QPushButton):
    def __init__(self, parent=None, pixmap=None, disabled_pixmap=None, name='', subdir=None):
        QPushButton.__init__(self, parent, name)

        if subdir is None:
            subdir = '16x16'

        if type(pixmap) == type(''):
            self.pixmap = load_pixmap(pixmap, subdir)
        else:
            self.pixmap = pixmap

        if type(disabled_pixmap) == type(''):
            self.disabled_pixmap = load_pixmap(disabled_pixmap, subdir) 
        else:
            self.disabled_pixmap = disabled_pixmap

        self.pixmap_width, self.pixmap_height = self.pixmap.width(), self.pixmap.height()
        self.width_set = None


    def drawButtonLabel(self, painter):
        button_width, button_height = self.width(), self.height()

        adj = 0
        if self.isDown():
            adj = 1

        if self.isEnabled():
            painter.setPen(Qt.black)
        else:
            painter.setPen(Qt.gray)

        text_rect = painter.boundingRect(0, 0, 1000, 1000, Qt.AlignLeft, self.text())
        text_width, text_height = text_rect.right() - text_rect.left(), text_rect.bottom() - text_rect.top()

        button_width_center = button_width/2
        button_height_center = button_height/2
        combined_width_center = (self.pixmap_width + text_width + 10)/2


        if self.isEnabled() or self.disabled_pixmap is None:
            painter.drawPixmap(button_width_center - combined_width_center + adj,
                button_height_center - self.pixmap_height/2 + adj, self.pixmap)
        else:
            painter.drawPixmap(button_width_center - combined_width_center + adj,
                button_height_center - self.pixmap_height/2 + adj, self.disabled_pixmap)

        if self.width_set is None:
            self.setMinimumWidth(self.pixmap_width + text_width + 20)
            self.width_set = 0

        painter.drawText(button_width_center - combined_width_center + 
            self.pixmap_width + 5 + adj, 
            button_height_center - text_height/2 + adj, 1000, 1000, 
            Qt.AlignLeft, self.text())

