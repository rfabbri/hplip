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
# Authors: Don Welch, Pete Parks, Naga Samrat Chowdary Narla,
#

from __future__ import generators

# Std Lib
import sys
import time
import os
import gzip
import select
import struct
import threading
import Queue
import signal

# Local
from base.g import *
from base import device, utils, pml, maint, pkit, os_utils
from prnt import cups
from base.codes import *
from ui_utils import load_pixmap
from installer.core_install import *

# Qt
from qt import *

# Main form
from devmgr4_base import DevMgr4_base

# Scrollviews
from scrollview import ScrollView
from scrollprintsettings import ScrollPrintSettingsView

# Alignment and ColorCal forms
from alignform import AlignForm
from aligntype6form1 import AlignType6Form1
from aligntype6form2 import AlignType6Form2
from paperedgealignform import PaperEdgeAlignForm
from colorcalform import ColorCalForm # Type 1 color cal
from coloradjform import ColorAdjForm  # Type 5 and 6 color adj
from colorcalform2 import ColorCalForm2 # Type 2 color cal
from colorcal4form import ColorCal4Form # Type 4 color cal
from align10form import Align10Form # Type 10 and 11 alignment
from align13form import Align13Form # Type 13 alignment

# Misc forms
from loadpaperform import LoadPaperForm
from settingsdialog import SettingsDialog
from aboutdlg import AboutDlg
from cleaningform import CleaningForm
from cleaningform2 import CleaningForm2
from waitform import WaitForm
from faxsettingsform import FaxSettingsForm
from nodevicesform import NoDevicesForm
from settingsdialog import SettingsDialog
from firmwaredialog import FirmwareDialog

# all in seconds
MIN_AUTO_REFRESH_RATE = 5
MAX_AUTO_REFRESH_RATE = 60
DEF_AUTO_REFRESH_RATE = 30


devices = {}    # { Device_URI : device.Device(), ... }
devices_lock = threading.RLock()

RESPONSE_START = 1
RESPONSE_DONE = 2

# ***********************************************************************************
#
# LISTVIEW/UTILITY UI CLASSES
#
# ***********************************************************************************

class IconViewToolTip(QToolTip):
    def __init__(self, parent, tooltip_text):
        QToolTip.__init__(self, parent.viewport())
        self.parent = parent


    def maybeTip(self, pos):
        abs_coords = QPoint(pos.x() + self.parent.contentsX(),
            pos.y() + self.parent.contentsY())

        item = self.parent.findItem(abs_coords)

        if item is not None and item.tooltip_text:
            rel_coords = QRect()
            rel_coords.setX(pos.x())
            rel_coords.setY(pos.y())
            i = item.rect()
            rel_coords.setWidth(i.width())
            rel_coords.setHeight(i.height())
            self.tip(rel_coords, item.tooltip_text)



class FuncViewItem(QIconViewItem):
    def __init__(self, parent, text, pixmap, tooltip_text, cmd):
        QIconViewItem.__init__(self, parent, text, pixmap)
        self.tooltip_text = tooltip_text
        self.cmd = cmd

        self.tooltip = IconViewToolTip(parent, tooltip_text)



class DeviceViewItem(QIconViewItem):
    def __init__(self, parent, text, pixmap, device_uri, is_avail=True):
        QIconViewItem.__init__(self, parent, text, pixmap)
        self.device_uri = device_uri
        self.is_avail = is_avail



class SuppliesListViewItem(QListViewItem):
    def __init__(self, parent, pixmap, desc, part_no, level_pixmap, status):
        QListViewItem.__init__(self, parent, '', desc, part_no, '', status)
        if pixmap is not None:
            self.setPixmap(0, pixmap)
        if level_pixmap is not None:
            self.setPixmap(3, level_pixmap)

    def paintCell(self, p, cg, c, w, a):
        color = QColorGroup(cg)
        pos = self.listView().itemPos(self)
        h = self.totalHeight()

        if (pos/h) % 2:
            color.setColor(QColorGroup.Base,  QColor(220, 228, 249))

        QListViewItem.paintCell(self, p, color, c, w, a)



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



class ScrollDialog(QDialog):
    def __init__(self, scrollview_cls, cur_device, cur_printer, service,
        parent = None, name=None, modal=0, fl=0):

        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ScrollDialog")

        self.setSizeGripEnabled(1)
        ScrollDialogLayout = QGridLayout(self,1,1,11,6,"ScrollDialogLayout")
        Layout1 = QHBoxLayout(None,0,6,"Layout1")
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)
        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)
        ScrollDialogLayout.addLayout(Layout1,1,0)

        self.scrollview = scrollview_cls(service, self)
        ScrollDialogLayout.addWidget(self.scrollview,0,0)

        self.scrollview.onDeviceChange(cur_device)
        self.scrollview.onPrinterChange(cur_printer)
        self.languageChange()

        self.resize(QSize(520,457).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager"))
        self.buttonOk.setText(self.__tr("Close"))
        self.buttonOk.setAccel(QKeySequence(QString.null))

    def __tr(self,s,c = None):
        return qApp.translate("ScrollDialog",s,c)


def showPasswordUI(prompt):
    try:
        dlg = PasswordDialog(prompt, None)

        if dlg.exec_loop() == QDialog.Accepted:
            return (dlg.getUsername(), dlg.getPassword())

    finally:
        pass

    return ("", "")


class StatusListViewItem(QListViewItem):
    def __init__(self, parent, pixmap, ess, tt, event_code, job_id, username):
        QListViewItem.__init__(self, parent, '', ess, tt, event_code, job_id, username)
        self.setPixmap(0, pixmap)

    def paintCell(self, p, cg, c, w, a):
        color = QColorGroup(cg)
        pos = self.listView().itemPos(self)
        h = self.totalHeight()
        row = pos/2

        if row % 2:
            color.setColor(QColorGroup.Base,  QColor(220, 228, 249))

        QListViewItem.paintCell(self, p, color, c, w, a)



class JobListViewItem(QCheckListItem):
    def __init__(self, parent, pixmap, desc, status, job_id):
        QCheckListItem.__init__(self, parent, '', QCheckListItem.CheckBox)
        self.job_id = job_id
        self.setPixmap(1, pixmap)
        self.setText(2, desc)
        self.setText(3, status)
        self.setText(4, job_id)

    def paintCell(self, p, cg, c, w, a):
        color = QColorGroup(cg)
        pos = self.listView().itemPos(self)
        h = self.totalHeight()

        if (pos/h) % 2:
            color.setColor(QColorGroup.Base,  QColor(220, 228, 249))

        QCheckListItem.paintCell(self, p, color, c, w, a)



class JobInfoDialog(QDialog):
    def __init__(self, text, parent=None, name=None, modal=0, fl=0):
        QDialog.__init__(self, parent, name, modal, fl)

        if not name:
            self.setName("JobInfoDialog")

        Form1Layout = QGridLayout(self,1,1,11,6,"Form1Layout")
        spacer6 = QSpacerItem(371,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Form1Layout.addItem(spacer6,1,0)
        self.pushButton4 = QPushButton(self,"pushButton4")
        Form1Layout.addWidget(self.pushButton4,1,1)
        self.textEdit = QTextEdit(self,"textEdit")
        Form1Layout.addMultiCellWidget(self.textEdit,0,0,0,1)

        self.languageChange()

        self.resize(QSize(571,542).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton4,SIGNAL("clicked()"),self.close)

        self.textEdit.setText(text)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Job Log"))
        self.pushButton4.setText(self.__tr("Close"))


    def __tr(self,s,c = None):
        return qApp.translate("JobInfoDialog",s,c)


# ***********************************************************************************
#
# DEVICE UPDATE THREAD
#
# ***********************************************************************************


class UpdateThread(QThread):
    def __init__(self, response_queue=None, request_queue=None):
        self.response_queue = response_queue # update queue -> main window
        self.request_queue = request_queue # main window -> update queue

        QThread.__init__(self)

    def run(self):
        while True:
            dev = self.request_queue.get(True)

            if dev is None:
                log.debug("Update thread: exit")
                break

            log.debug("Update thread start: %s" % dev.device_uri)

            try:
                #print "THREAD LOCK ACQUIRE"
                devices_lock.acquire()
                #print "THREAD LOCK ACQUIRE - OK"
                self.response_queue.put((RESPONSE_START, dev.device_uri))
                log.debug(log.bold("Update: %s %s %s" % ("*"*20, dev.device_uri, "*"*20)))

                if dev.supported:
                    try:
                        dev.open()
                    except Error, e:
                        log.warn(e.msg)

                    time.sleep(0.1)

                    if dev.device_state == DEVICE_STATE_NOT_FOUND:
                        dev.error_state = ERROR_STATE_ERROR
                    else:
                        try:
                            dev.queryDevice()

                        except Error, e:
                            log.error("Query device error (%s)." % e.msg)
                            dev.error_state = ERROR_STATE_ERROR

            finally:
                dev.close()
                #print "THREAD LOCK RELEASE"
                cups.releaseCupsInstance()
                devices_lock.release()

            log.debug("Device state = %d" % dev.device_state)
            log.debug("Status code = %d" % dev.status_code)
            log.debug("Error state = %d" % dev.error_state)

            log.debug("Update thread end: %s" % dev.device_uri)

            self.response_queue.put((RESPONSE_DONE, dev.device_uri))


# ***********************************************************************************
#
# MAINWINDOW
#
# ***********************************************************************************

class DevMgr4(DevMgr4_base):
    def __init__(self, read_pipe=None, toolbox_version='0.0',
                 initial_device_uri=None, disable_dbus=False,
                 parent=None, name=None, fl = 0):


        # Distro insformation
        core =  CoreInstall(MODE_CHECK)
#        core.init()
        self.Is_autoInstaller_distro = core.is_auto_installer_support()
        self.Latest_ver= user_conf.get('upgrade', 'latest_available_version')
        installed_version=sys_conf.get('hplip','version')
        if utils.Is_HPLIP_older_version(installed_version, self.Latest_ver):
            DevMgr4_base.__init__(self, parent, name, fl,self.Latest_ver,self.Is_autoInstaller_distro)
        else:
            self.Latest_ver = ""
            DevMgr4_base.__init__(self, parent, name, fl,self.Latest_ver,self.Is_autoInstaller_distro)
        log.debug("Initializing toolbox UI (Qt3)...")
        log.debug("HPLIP Version: %s" % prop.installed_version)

        self.disable_dbus = disable_dbus
        self.toolbox_version = toolbox_version
        self.cur_device_uri = user_conf.get('last_used', 'device_uri')
        self.device_vars = {}
        self.num_devices = 0
        self.cur_device = None
        self.rescanning = False
        self.initial_device_uri = initial_device_uri

        # dbus setup
        if not self.disable_dbus:
            self.dbus_avail, self.service, session_bus = device.init_dbus()

            if not self.dbus_avail:
                self.FailureUI("<b>Error</b><p>hp-systray must be running to get device status. hp-systray requires dbus support. Device status will not be available.")
            else:
                log.debug("dbus enabled")

        else:
            log.debug("dbus disabled")
            self.dbus_avail, self.service = False, None


        # Update thread setup
        self.request_queue = Queue.Queue()
        self.response_queue = Queue.Queue()
        self.update_thread = UpdateThread(self.response_queue, self.request_queue)
        self.update_thread.start()

        # Pipe from toolbox/dbus setup
        self.fmt = "80s80sI32sI80sf"
        self.fmt_size = struct.calcsize(self.fmt)

        if read_pipe is not None and not disable_dbus:
            log.debug("Setting up read_pipe")
            self.notifier = QSocketNotifier(read_pipe, QSocketNotifier.Read)
            QObject.connect(self.notifier, SIGNAL("activated(int)"), self.notifier_activated)

        # Application icon
        self.setIcon(load_pixmap('hp_logo', '128x128'))

        # User settings
        self.user_settings = utils.UserSettings()
        self.cmd_fab = self.user_settings.cmd_fab
        log.debug("FAB command: %s" % self.cmd_fab)

        if not self.user_settings.auto_refresh:
            self.autoRefresh.toggle()

        # Other initialization
        self.InitPixmaps()
        self.InitMisc()
        self.InitUI()

        cups.setPasswordCallback(showPasswordUI)

        if not prop.doc_build:
            self.helpContentsAction.setEnabled(False)

        self.allow_auto_refresh = True
        QTimer.singleShot(0, self.InitialUpdate)


    # ***********************************************************************************
    #
    # INIT
    #
    # ***********************************************************************************

    def InitPixmaps(self):
        self.func_icons_cached = False
        self.func_icons = {}
        self.device_icons = {}

        # TODO: Use Qt pixmap cache for all pixmaps?

        # Device icon list overlays
        self.warning_pix = load_pixmap('warning', '16x16')
        self.error_pix = load_pixmap('error', '16x16')
        self.ok_pix = load_pixmap('ok', '16x16')
        self.lowink_pix = load_pixmap('inkdrop', '16x16')
        self.lowtoner_pix = load_pixmap('toner', '16x16')
        self.busy_pix = load_pixmap('busy', '16x16')
        self.lowpaper_pix = load_pixmap('paper', '16x16')
        self.refresh_pix = load_pixmap('refresh', '16x16')
        self.refresh1_pix = load_pixmap('refresh1', '16x16')
        self.fax_icon = load_pixmap('fax2', 'other')
        self.idle_pix = load_pixmap('idle', '16x16')
        self.scan_pix = load_pixmap("scan", '16x16')
        self.print_pix = load_pixmap("print", '16x16')
        self.sendfax_pix =load_pixmap("fax", '16x16')
        self.pcard_pix = load_pixmap("pcard", '16x16')
        self.makecopies_pix = load_pixmap("makecopies", '16x16')
        self.help_pix = load_pixmap("help", '16x16')


        # pixmaps: (inkjet, laserjet)
        self.SMALL_ICONS = { ERROR_STATE_CLEAR : (None, None),
            ERROR_STATE_BUSY : (self.busy_pix, self.busy_pix),
            ERROR_STATE_ERROR : (self.error_pix, self.error_pix),
            ERROR_STATE_LOW_SUPPLIES : (self.lowink_pix, self.lowtoner_pix),
            ERROR_STATE_OK : (self.ok_pix, self.ok_pix),
            ERROR_STATE_WARNING : (self.warning_pix, self.warning_pix),
            ERROR_STATE_LOW_PAPER: (self.lowpaper_pix, self.lowpaper_pix),
            ERROR_STATE_PRINTING : (self.busy_pix, self.busy_pix),
            ERROR_STATE_SCANNING : (self.busy_pix, self.busy_pix),
            ERROR_STATE_PHOTOCARD : (self.busy_pix, self.busy_pix),
            ERROR_STATE_FAXING : (self.busy_pix, self.busy_pix),
            ERROR_STATE_COPYING : (self.busy_pix, self.busy_pix),
            ERROR_STATE_REFRESHING : (self.refresh1_pix, self.refresh1_pix),
        }

        self.STATUS_ICONS = { ERROR_STATE_CLEAR : (self.idle_pix, self.idle_pix),
              ERROR_STATE_BUSY : (self.busy_pix, self.busy_pix),
              ERROR_STATE_ERROR : (self.error_pix, self.error_pix),
              ERROR_STATE_LOW_SUPPLIES : (self.lowink_pix, self.lowtoner_pix),
              ERROR_STATE_OK : (self.ok_pix, self.ok_pix),
              ERROR_STATE_WARNING : (self.warning_pix, self.warning_pix),
              ERROR_STATE_LOW_PAPER: (self.lowpaper_pix, self.lowpaper_pix),
              ERROR_STATE_PRINTING : (self.print_pix, self.print_pix),
              ERROR_STATE_SCANNING : (self.scan_pix, self.scan_pix),
              ERROR_STATE_PHOTOCARD : (self.pcard_pix, self.print_pix),
              ERROR_STATE_FAXING : (self.sendfax_pix, self.sendfax_pix),
              ERROR_STATE_COPYING :  (self.makecopies_pix, self.makecopies_pix),
            }



    def InitUI(self):
        # Setup device icon list
        self.DeviceList.setAutoArrange(True)
        self.DeviceList.setSorting(True)

        # Setup main menu
        self.deviceRescanAction.setIconSet(QIconSet(self.refresh1_pix))
        self.deviceRefreshAll.setIconSet(QIconSet(self.refresh_pix))
        self.deviceInstallAction.setIconSet(QIconSet(load_pixmap('list_add', '16x16')))
        self.deviceRemoveAction.setIconSet(QIconSet(load_pixmap('list_remove', '16x16')))
        self.settingsConfigure.setIconSet(QIconSet(load_pixmap('settings', '16x16')))
        self.helpContentsAction.setIconSet(QIconSet(self.help_pix))

        # Setup toolbar
        self.deviceRescanAction.addTo(self.Toolbar)
        self.deviceRefreshAll.addTo(self.Toolbar)
        self.Toolbar.addSeparator()
        self.deviceInstallAction.addTo(self.Toolbar)
        self.deviceRemoveAction.addTo(self.Toolbar)
        self.Toolbar.addSeparator()
        self.settingsConfigure.addTo(self.Toolbar)
        self.helpContentsAction.addTo(self.Toolbar)

        # Init tabs/controls
        self.InitFuncsTab()
        self.InitStatusTab()
        self.InitSuppliesTab()
        self.InitPrintSettingsTab()
        self.InitPrintControlTab()

        # Resize the splitter so that the device list starts as a single column
        self.splitter2.setSizes([120, 700])
        signal.signal(signal.SIGINT, signal.SIG_IGN)


    def InitMisc(self):
        self.unit_names = { "year" : (self.__tr("year"), self.__tr("years")),
            "month" : (self.__tr("month"), self.__tr("months")),
            "week" : (self.__tr("week"), self.__tr("weeks")),
            "day" : (self.__tr("day"), self.__tr("days")),
            "hour" : (self.__tr("hour"), self.__tr("hours")),
            "minute" : (self.__tr("minute"), self.__tr("minutes")),
            "second" : (self.__tr("second"), self.__tr("seconds")),
            }

        self.num_repr = { 1 : self.__tr("one"),
              2 : self.__tr("two"),
              3 : self.__tr("three"),
              4 : self.__tr("four"),
              5 : self.__tr("five"),
              6 : self.__tr("six"),
              7 : self.__tr("seven"),
              8 : self.__tr("eight"),
              9 : self.__tr("nine"),
              10 : self.__tr("ten"),
              11 : self.__tr("eleven"),
              12 : self.__tr("twelve")
              }

        if self.Latest_ver is "":
            self.TabIndex = { self.FunctionsTab: self.UpdateFuncsTab,
                self.StatusTab: self.UpdateStatusTab,
                self.SuppliesTab: self.UpdateSuppliesTab,
                self.PrintSettingsTab: self.UpdatePrintSettingsTab,
                self.PrintJobsTab: self.UpdatePrintControlTab,
                }
        else:
            self.TabIndex = { self.FunctionsTab: self.UpdateFuncsTab,
                self.StatusTab: self.UpdateStatusTab,
                self.SuppliesTab: self.UpdateSuppliesTab,
                self.PrintSettingsTab: self.UpdatePrintSettingsTab,
                self.PrintJobsTab: self.UpdatePrintControlTab,
                self.UpgradeTab:self.UpdateUpgradeTab,
                }



    def InitialUpdate(self):
        self.RescanDevices()

        cont = True
        if self.initial_device_uri is not None:
            if not self.ActivateDevice(self.initial_device_uri):
                log.error("Device %s not found" % self.initial_device_uri)
                cont = False

        self.refresh_timer = QTimer(self, "RefreshTimer")
        self.connect(self.refresh_timer, SIGNAL('timeout()'), self.TimedRefresh)

        if MIN_AUTO_REFRESH_RATE <= self.user_settings.auto_refresh_rate <= MAX_AUTO_REFRESH_RATE:
            self.refresh_timer.start(self.user_settings.auto_refresh_rate * 1000)

        self.update_timer = QTimer(self)
        self.connect(self.update_timer, SIGNAL("timeout()"), self.ThreadUpdate)
        self.update_timer.start(500)


    def ActivateDevice(self, device_uri):
        log.debug(log.bold("Activate: %s %s %s" % ("*"*20, device_uri, "*"*20)))
        d = self.DeviceList.firstItem()
        found = False

        while d is not None:
            if d.device_uri == device_uri:
                found = True
                self.DeviceList.setSelected(d, True)
                self.DeviceList.setCurrentItem(d)
                break

            d = d.nextItem()

        return found



    # ***********************************************************************************
    #
    # UPDATES/NOTIFICATIONS
    #
    # ***********************************************************************************

    def notifier_activated(self, sock): # dbus message has arrived
        m = ''
        while True:
            ready = select.select([sock], [], [], 0.1)

            if ready[0]:
                m = ''.join([m, os.read(sock, self.fmt_size)])
                if len(m) == self.fmt_size:
                    if self.cur_device is None or self.rescanning:
                        return

                    event = device.Event(*struct.unpack(self.fmt, m))
                    desc = device.queryString(event.event_code)
                    error_state = STATUS_TO_ERROR_STATE_MAP.get(event.event_code, ERROR_STATE_CLEAR)
                    log.debug("Status event: %s (%d)" % (event.device_uri, event.event_code))

                    if event.event_code > EVENT_MAX_USER_EVENT:

                        if event.event_code == EVENT_HISTORY_UPDATE: # 9003
                            log.debug("History update: %s" % event.device_uri)

                            if not self.rescanning:
                                dev = self.findDeviceByURI(event.device_uri)

                                self.UpdateHistory(dev)
                                self.UpdateDevice(dev)

                        elif event.event_code == EVENT_CUPS_QUEUES_REMOVED or event.event_code == EVENT_CUPS_QUEUES_ADDED:
                            pass

                        elif event.event_code == EVENT_RAISE_DEVICE_MANAGER: # 9001
                            log.debug("Raise requested")
                            self.showNormal()
                            self.setActiveWindow()
                            self.raiseW()

                    else:
                        log.debug("Ignored")

            else:
                break


    def TimedRefresh(self):
        if not self.rescanning and self.user_settings.auto_refresh and self.allow_auto_refresh:
            log.debug("Refresh timer...")
            self.CleanupChildren()

            if self.user_settings.auto_refresh_type == 0:
                self.RequestDeviceUpdate()
            else:
                self.RescanDevices()


    def ThreadUpdate(self): # periodically check for updates from update thread
        if not self.response_queue.empty():
            response_code, device_uri = self.response_queue.get()

            if response_code == RESPONSE_START:
                self.statusBar().message(self.__tr("Updating %1...").arg(device_uri))
                qApp.processEvents()

            elif response_code == RESPONSE_DONE:
                self.statusBar().message(QString("%1 (%2)").arg(self.cur_device_uri).\
                    arg(', '.join(self.cur_device.cups_printers)))

                dev = self.findDeviceByURI(device_uri)

                if dev is not None:
                    self.UpdateHistory(dev)
                    self.UpdateDevice(dev)

                qApp.processEvents()

            if self.response_queue.empty() and self.request_queue.empty():
                self.UpdateTitle()
                # Disable thread timer until more items placed in request queue?


    # ***********************************************************************************
    #
    # TAB/DEVICE CHANGE SLOTS
    #
    # ***********************************************************************************

    def Tabs_currentChanged(self, tab=None):
        """ Called when the active tab changes.
            Update newly displayed tab.
        """

        if tab is None:
            tab = self.Tabs.currentPage()

        try:
            self.TabIndex[tab]()
        except AttributeError:
            pass

    def Tabs_deviceChanged(self, tab=None):
        """ Called when the device changes.
            Update the currently displayed tab.
        """
        if tab is None:
            tab = self.Tabs.currentPage()

        self.TabIndex[tab]()


    # ***********************************************************************************
    #
    # DEVICE ICON LIST/DEVICE UPDATE(S)
    #
    # ***********************************************************************************

    def DeviceList_onItem(self, a0):
        pass


    def deviceRescanAction_activated(self):
        self.deviceRescanAction.setEnabled(False)
        self.RequestDeviceUpdate()
        self.deviceRescanAction.setEnabled(True)


    def deviceRefreshAll_activated(self):
        self.RescanDevices()


    def DeviceList_clicked(self,a0):
        pass


    def CreatePixmap(self, dev=None):
        if dev is None:
            dev = self.cur_device

        try:
            dev.icon
        except AttributeError:
            dev.icon = "default_printer"

        try:
            self.device_icons[dev.icon]
        except:
            self.device_icons[dev.icon] = load_pixmap(dev.icon, 'devices')

        pix = self.device_icons[dev.icon]

        w, h = pix.width(), pix.height()
        error_state = dev.error_state
        icon = QPixmap(w, h)
        p = QPainter(icon)
        p.eraseRect(0, 0, icon.width(), icon.height())
        p.drawPixmap(0, 0, pix)

        try:
            tech_type = dev.tech_type
        except AttributeError:
            tech_type = TECH_TYPE_NONE

        if dev.device_type == DEVICE_TYPE_FAX:
            p.drawPixmap(w - self.fax_icon.width(), 0, self.fax_icon)

        if error_state != ERROR_STATE_CLEAR:
            if tech_type in (TECH_TYPE_COLOR_INK, TECH_TYPE_MONO_INK):
                status_icon = self.SMALL_ICONS[error_state][0] # ink
            else:
                status_icon = self.SMALL_ICONS[error_state][1] # laser

            if status_icon is not None:
                p.drawPixmap(0, 0, status_icon)

        p.end()

        return icon


    def DeviceListRefresh(self):
        global devices
        log.debug("Rescanning device list...")

        if not self.rescanning:
            self.setCaption(self.__tr("Refreshing Device List - HP Device Manager"))
            self.statusBar().message(self.__tr("Refreshing device list..."))

            self.rescanning = True
            self.cups_devices = device.getSupportedCUPSDevices(['hp', 'hpfax'])

            devices_lock.acquire()

            try:
                adds = []
                for d in self.cups_devices:
                    if d not in devices:
                        adds.append(d)

                log.debug("Adds: %s" % ','.join(adds))

                removals = []
                for d in devices:
                    if d not in self.cups_devices:
                        removals.append(d)

                log.debug("Removals (1): %s" % ','.join(removals))

                updates = []
                for d in devices:
                    if d not in adds and d not in removals:
                        updates.append(d)

                log.debug("Updates: %s" % ','.join(updates))


                for d in adds:
                    log.debug("adding: %s" % d)
                    try:
                        dev = device.Device(d, service=self.service, callback=self.callback,
                  disable_dbus=self.disable_dbus)
                    except Error:
                        log.error("Unexpected error in Device class.")
                        log.exception()

                    if not dev.supported:
                        log.debug("Unsupported model - removing device.")
                        removals.append(d)
                        continue

                    self.CheckForDeviceSettingsUI(dev)
                    icon = self.CreatePixmap(dev)

                    if dev.device_type == DEVICE_TYPE_FAX:
                        DeviceViewItem(self.DeviceList,  self.__tr("%1 (Fax)").arg(dev.model_ui),
                            icon, d)
                    else:
                        if dev.fax_type:
                            DeviceViewItem(self.DeviceList, self.__tr("%1 (Printer)").arg(dev.model_ui),
                                icon, d)
                        else:
                            DeviceViewItem(self.DeviceList, dev.model_ui,
                                icon, d)

                    devices[d] = dev

                log.debug("Removals (2): %s" % ','.join(removals))
                removed_device=None
                for d in removals:
                    removed_device = d
                    item = self.DeviceList.firstItem()
                    log.debug("removing: %s" % d)

                    try:
                        del devices[d]
                    except KeyError:
                        pass


                    while item is not None:
                        if item.device_uri == d:
                            self.DeviceList.takeItem(item)
                            break

                        item = item.nextItem()

                    qApp.processEvents()

                self.DeviceList.adjustItems()
                self.DeviceList.updateGeometry()
                qApp.processEvents()
                # sending Event to remove this device from hp-systray
                if removed_device:
                    utils.sendEvent(EVENT_CUPS_QUEUES_REMOVED,removed_device, "")

                if len(devices):
                    for tab in self.TabIndex:
                        self.Tabs.setTabEnabled(tab, True)

                    if self.cur_device_uri:
                        item = first_item = self.DeviceList.firstItem()

                        while item is not None:
                            qApp.processEvents()
                            if item.device_uri == self.cur_device_uri:
                                self.DeviceList.setCurrentItem(item)
                                self.DeviceList.setSelected(item, True)
                                self.statusBar().message(self.cur_device_uri)
                                break

                            item = item.nextItem()

                        else:
                            self.cur_device = None
                            self.cur_device_uri = ''

                    if self.cur_device is None:
                        self.cur_device_uri = self.DeviceList.firstItem().device_uri
                        self.cur_device = devices[self.cur_device_uri]
                        self.DeviceList.setCurrentItem(self.DeviceList.firstItem())

                    self.Tabs.setTabEnabled(self.SuppliesTab, self.cur_device.device_type == DEVICE_TYPE_PRINTER and
                        self.cur_device.error_state != ERROR_STATE_ERROR)

                    self.UpdatePrinterCombos()

                    user_conf.set('last_used', 'device_uri', self.cur_device_uri)

                    for d in updates + adds:
                        if d not in removals:
                            self.RequestDeviceUpdate(devices[d])

                else:
                    self.cur_device = None
                    self.deviceRescanAction.setEnabled(False)
                    self.deviceRemoveAction.setEnabled(False)
                    self.rescanning = False
                    self.statusBar().message(self.__tr("Press F6 to refresh."))

                    for tab in self.TabIndex:
                        self.Tabs.setTabEnabled(tab, False)

                    dlg = NoDevicesForm(self, "", True)
                    dlg.show()

            finally:
                self.rescanning = False
                devices_lock.release()

            self.deviceRescanAction.setEnabled(True)
            self.deviceRemoveAction.setEnabled(True)



    def UpdateTitle(self):
        if self.cur_device.device_type == DEVICE_TYPE_FAX:
                self.setCaption(self.__tr("HP Device Manager - %1 (Fax)").arg(self.cur_device.model_ui))
        else:
            if self.cur_device.fax_type:
                self.setCaption(self.__tr("HP Device Manager - %1 (Printer)").arg(self.cur_device.model_ui))
            else:
                self.setCaption(self.__tr("HP Device Manager - %1").arg(self.cur_device.model_ui))


    def UpdateDeviceByURI(self, device_uri):
        return self.UpdateDevice(self.findDeviceByURI(device_uri))


    def UpdateDevice(self, dev=None, update_tab=True):
        """ Update the device icon and currently displayed tab.
        """
        if dev is None:
            dev = self.cur_device

        log.debug("UpdateDevice(%s)" % dev.device_uri)

        item = self.findItem(dev)

        if item is not None:
            item.setPixmap(self.CreatePixmap(dev))

        if dev is self.cur_device and dev.error_state == ERROR_STATE_ERROR:
            self.Tabs.setCurrentPage(1)

        if dev is self.cur_device and update_tab:
            self.UpdatePrinterCombos()
            self.TabIndex[self.Tabs.currentPage()]()
            
            if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                self.Tabs.changeTab(self.PrintSettingsTab,self.__tr("Print Settings"))
                self.Tabs.changeTab(self.PrintJobsTab,self.__tr("Print Control"))
            else:
                self.Tabs.changeTab(self.PrintSettingsTab,self.__tr("Fax Settings"))
                self.Tabs.changeTab(self.PrintJobsTab,self.__tr("Fax Control"))
        qApp.processEvents()


    def DeviceList_currentChanged(self, i):
        if i is not None: # and not self.rescanning:
            self.cur_device_uri = self.DeviceList.currentItem().device_uri
            self.cur_device = devices[self.cur_device_uri]
            user_conf.set('last_used', 'device_uri', self.cur_device_uri)

            self.Tabs.setTabEnabled(self.SuppliesTab, self.cur_device.device_type == DEVICE_TYPE_PRINTER and
                self.cur_device.error_state != ERROR_STATE_ERROR)

            self.UpdateDevice()
            self.UpdateTitle()


    def findItem(self, dev):
        if dev is None:
            dev = self.cur_device

        return self.findItemByURI(dev.device_uri)


    def findItemByURI(self, device_uri):
        item = self.DeviceList.firstItem()

        while item is not None:
            if item.device_uri == device_uri:
                return item
            item = item.nextItem()


    def findDeviceByURI(self, device_uri):
        try:
            return devices[device_uri]
        except:
            return None


    def RequestDeviceUpdate(self, dev=None, item=None):
        """ Submit device update request to update thread. """

        if dev is None:
            dev = self.cur_device

        if dev is not None:
            #log.debug("RequestDeviceUpdate(%s)" % dev.device_uri)
            dev.error_state = ERROR_STATE_REFRESHING
            self.UpdateDevice(dev, update_tab=False)
            qApp.processEvents()

            self.request_queue.put(dev)


    def RescanDevices(self):
        #log.debug("RescanDevices()")
        if not self.rescanning:
            self.deviceRefreshAll.setEnabled(False)
            try:
                self.DeviceListRefresh()
            finally:
                self.deviceRefreshAll.setEnabled(True)


    def callback(self):
        qApp.processEvents()


    # ***********************************************************************************
    #
    # DEVICE LIST RIGHT CLICK
    #
    # ***********************************************************************************

    def DeviceList_rightButtonClicked(self, item, pos):
        popup = QPopupMenu(self)

        if item is not None and item is self.DeviceList.currentItem():
            if self.cur_device.error_state != ERROR_STATE_ERROR:
                if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                    popup.insertItem(self.__tr("Print..."), self.PrintButton_clicked)

                    if self.cur_device.scan_type:
                        popup.insertItem(self.__tr("Scan..."), self.ScanButton_clicked)

                    if self.cur_device.pcard_type:
                        popup.insertItem(self.__tr("Access Photo Cards..."), self.PCardButton_clicked)

                    if self.cur_device.copy_type:
                        popup.insertItem(self.__tr("Make Copies..."), self.MakeCopiesButton_clicked)

                elif self.cur_device.device_type == DEVICE_TYPE_FAX:
                    if self.cur_device.fax_type:
                        popup.insertItem(self.__tr("Send Fax..."), self.SendFaxButton_clicked)

                popup.insertSeparator()

                if self.cur_device.device_settings_ui is not None:
                    popup.insertItem(self.__tr("Device Settings..."), self.deviceSettingsButton_clicked)

            if not self.rescanning:
                popup.insertItem(self.__tr("Refresh Device"), self.deviceRescanAction_activated)

        if not self.rescanning:
            popup.insertItem(self.__tr("Refresh All"), self.deviceRefreshAll_activated)

        popup.popup(pos)


    # ***********************************************************************************
    #
    # PRINTER NAME COMBOS
    #
    # ***********************************************************************************

    def updatePrinterList(self):
        if self.cur_device is not None and \
            self.cur_device.supported:

            printers = cups.getPrinters()
            self.cur_device.cups_printers = []

            for p in printers:
                if p.device_uri == self.cur_device_uri:
                    self.cur_device.cups_printers.append(p.name)


    def UpdatePrinterCombos(self):
        self.PrintSettingsPrinterCombo.clear()
        self.PrintJobPrinterCombo.clear()

        if self.cur_device is not None and \
            self.cur_device.supported:

            for c in self.cur_device.cups_printers:
                self.PrintSettingsPrinterCombo.insertItem(c.decode("utf-8"))
                self.PrintJobPrinterCombo.insertItem(c.decode("utf-8"))

            self.cur_printer = unicode(self.PrintSettingsPrinterCombo.currentText())

    def PrintSettingsPrinterCombo_activated(self, s):
        self.cur_printer = unicode(s)
        self.PrintJobPrinterCombo.setCurrentText(self.cur_printer.encode("latin1")) # TODO: ?
        return self.PrinterCombo_activated(self.cur_printer)

    def PrintJobPrinterCombo_activated(self, s):
        self.cur_printer = unicode(s)
        self.PrintSettingsPrinterCombo.setCurrentText(self.cur_printer.encode("latin1")) # TODO: ?
        return self.PrinterCombo_activated(self.cur_printer)

    def PrinterCombo_activated(self, printer):
        self.TabIndex[self.Tabs.currentPage()]()
        self.UpdatePrintSettingsTabPrinter()



    # ***********************************************************************************
    #
    # FUNCTIONS/ACTION TAB
    #
    # ***********************************************************************************

    def InitFuncsTab(self):
        self.click_lock = None

    def UpdateFuncsTab(self):
        self.iconList.clear()

        d = self.cur_device

        if d is not None:

            avail = d.device_state != DEVICE_STATE_NOT_FOUND and d.supported
            fax = d.fax_type and prop.fax_build and d.device_type == DEVICE_TYPE_FAX and \
                sys.hexversion >= 0x020300f0 and avail
            printer = d.device_type == DEVICE_TYPE_PRINTER and avail
            req_plugin = d.plugin == PLUGIN_REQUIRED
            opt_plugin = d.plugin == PLUGIN_OPTIONAL

            hplip_conf = ConfigParser.ConfigParser()
            fp = open("/etc/hp/hplip.conf", "r")
            hplip_conf.readfp(fp)
            fp.close()

            try:
                plugin_installed = utils.to_bool(hplip_conf.get("hplip", "plugin"))
            except ConfigParser.NoOptionError:
                plugin_installed = False

            if d.plugin:
                if req_plugin and plugin_installed:
                    x = self.__tr("Download and install<br>required plugin (already installed).")

                elif req_plugin and not plugin_installed:
                    x = self.__tr("Download and install<br>required plugin (needs installation).")

                elif opt_plugin and plugin_installed:
                    x = self.__tr("Download and install<br>optional plugin (already installed).")

                elif opt_plugin and not plugin_installed:
                    x = self.__tr("Download and install<br>optional plugin (needs installation).")

            else:
                x = ''


            self.ICONS = [

                # PRINTER

                (lambda : printer,                 # filter func
                self.__tr("Print"),                      # Text
                "print",       # Icon
                self.__tr("Print documents or files."),  # Tooltip
                self.user_settings.cmd_print),           # command/action

                (lambda : d.scan_type and prop.scan_build and \
                    d.device_type == DEVICE_TYPE_PRINTER and avail,
                self.__tr("Scan"),
                "scan",
                self.__tr("Scan a document, image, or photograph.<br>"),
                self.user_settings.cmd_scan),

                (lambda : d.copy_type and d.device_type == DEVICE_TYPE_PRINTER and avail,
                self.__tr("Make Copies"),
                "makecopies",
                self.__tr("Make copies on the device controlled by the PC.<br>"),
                self.user_settings.cmd_copy),

                (lambda : d.pcard_type and d.device_type == DEVICE_TYPE_PRINTER and avail,
                self.__tr("Unload Photo Card"),
                "makecopies",
                self.__tr("Copy images from the device's photo card to the PC."),
                self.PCardButton_clicked),

                # FAX

                (lambda: fax,
                self.__tr("Send Fax"),
                "fax",
                self.__tr("Send a fax from the PC."),
                self.user_settings.cmd_fax),

                (lambda: fax,
                self.__tr("Fax Setup"),
                "fax_setup",
                self.__tr("Fax support must be setup before you can send faxes."),
                self.faxSettingsButton_clicked),

                (lambda: fax,
                self.__tr("Fax Address Book"),
                "fab",
                self.__tr("Setup fax phone numbers to use when sending faxes from the PC."),
                self.cmd_fab),

                # SETTINGS/TOOLS

                (lambda : self.cur_device.device_settings_ui is not None and avail,
                self.__tr("Device Settings"),
                "settings",
                self.__tr("Your device has special device settings.<br>You may alter these settings here."),
                self.deviceSettingsButton_clicked),

                (lambda : printer,
                self.__tr("Print Test Page"),
                "testpage",
                self.__tr("Print a test page to test the setup of your printer."),
                self.PrintTestPageButton_clicked),

                (lambda : True,
                self.__tr("View Printer (Queue) Information"),
                "cups",
                self.__tr("View the printers (queues) installed in CUPS."),
                self.viewPrinterInformation),

                (lambda : True,
                self.__tr("View Device Information"),
                "info",
                self.__tr("This information is primarily useful for <br>debugging and troubleshooting (advanced)."),
                self.viewInformation),

                (lambda: printer and d.align_type,
                self.__tr("Align Cartridges (Print Heads)"),
                "align",
                self.__tr("This will improve the quality of output when a new cartridge is installed."),
                self.AlignPensButton_clicked),

                (lambda: printer and d.clean_type,
                self.__tr("Clean Cartridges"),
                "clean",
                self.__tr("You only need to perform this action if you are<br>having problems with poor printout quality due to clogged ink nozzles."),
                self.CleanPensButton_clicked),

                (lambda: printer and d.color_cal_type and d.color_cal_type == COLOR_CAL_TYPE_TYPHOON,
                self.__tr("Color Calibration"),
                "colorcal",
                self.__tr("Use this procedure to optimimize your printer's color output<br>(requires glossy photo paper)."),
                self.ColorCalibrationButton_clicked),

                (lambda: printer and d.color_cal_type and d.color_cal_type != COLOR_CAL_TYPE_TYPHOON,
                self.__tr("Color Calibration"),
                "colorcal",
                self.__tr("Use this procedure to optimimize your printer's color output."),
                self.ColorCalibrationButton_clicked),

                (lambda: printer and d.linefeed_cal_type,
                self.__tr("Line Feed Calibration"),
                "linefeed_cal",
                self.__tr("Use line feed calibration to optimize print quality<br>(to remove gaps in the printed output)."),
                self.linefeedCalibration),

                (lambda: printer and d.pq_diag_type,
                self.__tr("Print Diagnostic Page"),
                "pq_diag",
                self.__tr("Your printer can print a test page <br>to help diagnose print quality problems."),
                self.pqDiag),

                # FIRMWARE

                (lambda : printer and d.fw_download,
                self.__tr("Download Firmware"),
                "firmware",
                self.__tr("Download firmware to your printer <br>(required on some devices after each power-up)."),
                self.ShowFirmwareDlg),

                # PLUGIN

                (lambda : req_plugin,
                self.__tr("Install Required Plugin"),
                "plugin",
                x, #self.__tr("Download and install the HPLIP plugin."),
                self.downloadPlugin),

                (lambda : opt_plugin,
                self.__tr("Install Optional Plugin"),
                "plugin",
                x, #self.__tr("Download and install the HPLIP plugin."),
                self.downloadPlugin),

                # HELP/WEBSITE

                (lambda : True,
                self.__tr("Visit HPLIP Website"),
                "hp_logo",
                self.__tr("Visit HPLIP website."),
                self.viewSupport),

                (lambda : True,
                self.__tr("Help"),
                "help",
                self.__tr("View HPLIP help."),
                self.viewHelp),
            ]

            if not self.func_icons_cached:
                for filter, text, icon, tooltip, cmd in self.ICONS:
                    self.func_icons[icon] = load_pixmap(icon, '32x32')
                self.func_icons_cached = True

            for filter, text, icon, tooltip, cmd in self.ICONS:
                if filter is not None:
                    if not filter():
                        continue

                FuncViewItem(self.iconList, text,
                    self.func_icons[icon],
                    tooltip,
                    cmd)


    def downloadPlugin(self):
        ok, sudo_ok = pkit.run_plugin_command(self.cur_device.plugin == PLUGIN_REQUIRED, self.cur_device.mq['plugin-reason'])
        if not sudo_ok:
            QMessageBox.critical(self,
                self.caption(),
                self.__tr("<b>Unable to find an appropriate su/sudo utility to run hp-plugin.</b><p>Install kdesu, gnomesu, or gksu.</p>"),
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton)
        else:
            self.UpdateFuncsTab()


    def iconList_clicked(self, item):
        return self.RunFuncCmd(item)


    def RunFuncCmd(self, item):
        if item is not None and self.click_lock is not item:
            try:
                item.cmd()
            except TypeError:
                self.RunCommand(item.cmd)

            self.click_lock = item
            QTimer.singleShot(1000, self.UnlockClick)


    def UnlockClick(self):
        self.click_lock = None


    def RunFuncCmdContext(self):
        return self.RunFuncCmd(self.iconList.currentItem())


    def iconList_contextMenuRequested(self, item, pos):
        if item is not None and item is self.iconList.currentItem():
            popup = QPopupMenu(self)
            popup.insertItem(self.__tr("Open..."), self.RunFuncCmdContext)
            popup.popup(pos)


    def iconList_returnPressed(self, item):
        return self.RunFuncCmd(item)


    def deviceSettingsButton_clicked(self):
        try:
            self.cur_device.open()
            self.cur_device.device_settings_ui(self.cur_device, self)
        finally:
            self.cur_device.close()


    def setupDevice_activated(self):
        try:
            self.cur_device.open()
            self.cur_device.device_settings_ui(self.cur_device, self)
        finally:
            self.cur_device.close()


    def PrintButton_clicked(self):
        self.RunCommand(self.user_settings.cmd_print)


    def ScanButton_clicked(self):
        self.RunCommand(self.user_settings.cmd_scan)


    def PCardButton_clicked(self):
        if self.cur_device.pcard_type == PCARD_TYPE_MLC:
            self.RunCommand(self.user_settings.cmd_pcard)

        elif self.cur_device.pcard_type == PCARD_TYPE_USB_MASS_STORAGE:
            self.FailureUI(self.__tr("<p><b>Photocards on your printer are only available by mounting them as drives using USB mass storage.</b><p>Please refer to your distribution's documentation for setup and usage instructions."))


    def SendFaxButton_clicked(self):
        self.RunCommand(self.user_settings.cmd_fax)


    def MakeCopiesButton_clicked(self):
        self.RunCommand(self.user_settings.cmd_copy)


    def ConfigureFeaturesButton_clicked(self):
        self.settingsConfigure_activated(2)


    def viewInformation(self):
        dlg = ScrollDialog(ScrollDeviceInfoView, self.cur_device, self.cur_printer, self.service, self)
        dlg.exec_loop()


    def viewPrinterInformation(self):
        dlg = ScrollDialog(ScrollPrinterInfoView, self.cur_device, self.cur_printer, self.service, self)
        dlg.exec_loop()


    def viewHelp(self):
        f = "http://hplip.sf.net"

        if prop.doc_build:
            g = os.path.join(sys_conf.get('dirs', 'doc'), 'index.html')
            if os.path.exists(g):
                f = "file://%s" % g

        log.debug(f)
        utils.openURL(f)


    def viewSupport(self):
        f = "http://hplip.sf.net"
        log.debug(f)
        utils.openURL(f)


    def pqDiag(self):
        d = self.cur_device
        pq_diag = d.pq_diag_type

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    QApplication.restoreOverrideCursor()

                    if pq_diag == 1:
                        maint.printQualityDiagType1(d, self.LoadPaperUI)

                    elif pq_diag == 2:
                        maint.printQualityDiagType2(d, self.LoadPaperUI)

                else:
                    self.CheckDeviceUI()

        finally:
            d.close()
            QApplication.restoreOverrideCursor()


    def linefeedCalibration(self):
        d = self.cur_device
        linefeed_type = d.linefeed_cal_type

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    QApplication.restoreOverrideCursor()

                    if linefeed_type == 1:
                        maint.linefeedCalType1(d, self.LoadPaperUI)

                    elif linefeed_type == 2:
                        maint.linefeedCalType2(d, self.LoadPaperUI)

                else:
                    self.CheckDeviceUI()

        finally:
            d.close()
            QApplication.restoreOverrideCursor()


    def downloadFirmware(self):
        d = self.cur_device
        ok = False

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)
            d.open()

            if d.isIdleAndNoError():
                ok = d.downloadFirmware()

        finally:
            d.close()
            QApplication.restoreOverrideCursor()

            if not ok:
                self.FailureUI(self.__tr("<b>An error occured downloading firmware file.</b><p>Please check your printer and ensure that the HPLIP plugin has been installed."))


    def CheckDeviceUI(self):
        self.FailureUI(self.__tr("<b>Device is busy or in an error state.</b><p>Please check device and try again."))


    def LoadPaperUI(self, msg="", title=""):
        LPFObj = LoadPaperForm(self)
        if title:
            LPFObj.setCaption(title)
        if msg:
            LPFObj.textLabel7.setText(msg)

        if LPFObj.exec_loop() == QDialog.Accepted:
            return True
        return False


    def AlignmentNumberUI(self, letter, hortvert, colors, line_count, choice_count):
        dlg = AlignForm(self, letter, hortvert, colors, line_count, choice_count)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.value
        else:
            return False, 0


    def PaperEdgeUI(self, maximum):
        dlg = PaperEdgeAlignForm(self)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.value
        else:
            return False, 0


    def BothPensRequiredUI(self):
        self.WarningUI(self.__tr("<p><b>Both cartridges are required for alignment.</b><p>Please install both cartridges and try again."))


    def InvalidPenUI(self):
        self.WarningUI(self.__tr("<p><b>One or more cartiridges are missing from the printer.</b><p>Please install cartridge(s) and try again."))


    def PhotoPenRequiredUI(self):
        self.WarningUI(self.__tr("<p><b>Both the photo and color cartridges must be inserted into the printer to perform color calibration.</b><p>If you are planning on printing with the photo cartridge, please insert it and try again."))


    def PhotoPenRequiredUI2(self):
        self.WarningUI(self.__tr("<p><b>Both the photo (regular photo or photo blue) and color cartridges must be inserted into the printer to perform color calibration.</b><p>If you are planning on printing with the photo or photo blue cartridge, please insert it and try again."))


    def NotPhotoOnlyRequired(self): # Type 11
        self.WarningUI(self.__tr("<p><b>Cannot align with only the photo cartridge installed.</b><p>Please install other cartridges and try again."))


    def AioUI1(self):
        dlg = AlignType6Form1(self)
        return dlg.exec_loop() == QDialog.Accepted


    def AioUI2(self):
        AlignType6Form2(self).exec_loop()


    def Align10and11UI(self, pattern, align_type):
        dlg = Align10Form(pattern, align_type, self)
        dlg.exec_loop()
        return dlg.getValues()


    def Align13UI(self):
        dlg = Align13Form(self)
        dlg.exec_loop()
        return True


    def AlignPensButton_clicked(self):
        d = self.cur_device
        align_type = d.align_type

        log.debug("Align: %s %s (type=%d) %s" % ("*"*20, self.cur_device.device_uri, align_type, "*"*20))

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    QApplication.restoreOverrideCursor()

                    if align_type == ALIGN_TYPE_AUTO:
                        maint.AlignType1(d, self.LoadPaperUI)

                    elif align_type == ALIGN_TYPE_8XX:
                        maint.AlignType2(d, self.LoadPaperUI, self.AlignmentNumberUI,
               self.BothPensRequiredUI)

                    elif align_type in (ALIGN_TYPE_9XX,ALIGN_TYPE_9XX_NO_EDGE_ALIGN):
                         maint.AlignType3(d, self.LoadPaperUI, self.AlignmentNumberUI,
                self.PaperEdgeUI, align_type)

                    elif align_type in (ALIGN_TYPE_LIDIL_0_3_8, ALIGN_TYPE_LIDIL_0_4_3, ALIGN_TYPE_LIDIL_VIP):
                        maint.AlignxBow(d, align_type, self.LoadPaperUI, self.AlignmentNumberUI,
              self.PaperEdgeUI, self.InvalidPenUI, self.ColorAdjUI)

                    elif align_type == ALIGN_TYPE_LIDIL_AIO:
                        maint.AlignType6(d, self.AioUI1, self.AioUI2, self.LoadPaperUI)

                    elif align_type == ALIGN_TYPE_DESKJET_450:
                        maint.AlignType8(d, self.LoadPaperUI, self.AlignmentNumberUI)

                    elif align_type == ALIGN_TYPE_LBOW:
                        maint.AlignType10(d, self.LoadPaperUI, self.Align10and11UI)

                    elif align_type == ALIGN_TYPE_LIDIL_0_5_4:
                        maint.AlignType11(d, self.LoadPaperUI, self.Align10and11UI, self.NotPhotoOnlyRequired)

                    elif align_type == ALIGN_TYPE_OJ_PRO:
                        maint.AlignType12(d, self.LoadPaperUI)

                    elif align_type == ALIGN_TYPE_AIO:
                        maint.AlignType13(d, self.LoadPaperUI, self.Align13UI)

                    elif align_type == ALIGN_TYPE_LEDM:
                        maint.AlignType15(d, self.LoadPaperUI, self.Align13UI)

                    elif align_type == ALIGN_TYPE_LEDM_MANUAL:
                        maint.AlignType16(d, self.LoadPaperUI, self.AlignmentNumberUI)

                    elif align_type == ALIGN_TYPE_LEDM_FF_CC_0:
                        maint.AlignType17(d, self.LoadPaperUI, self.Align13UI)

                    elif align_type == ALIGN_TYPE_UNSUPPORTED:
                        self.WarningUI(self.__tr("<p><b>Alignment through HPLIP not supported for this printer. Please use the printer's front panel to perform cartridge alignment.</b>"))

                else:
                    self.CheckDeviceUI()

        finally:
            d.close()
            QApplication.restoreOverrideCursor()


    def ColorAdjUI(self, line, maximum=0):
        dlg = ColorAdjForm(self, line)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.value
        else:
            return False, 0


    def ColorCalUI(self):
        dlg = ColorCalForm(self)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.value
        else:
            return False, 0


    def ColorCalUI2(self):
        dlg = ColorCalForm2(self)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.value
        else:
            return False, 0


    def ColorCalUI4(self):
        dlg = ColorCal4Form(self)
        if dlg.exec_loop() == QDialog.Accepted:
            return True, dlg.values
        else:
            return False, None


    def ColorCalibrationButton_clicked(self):
        d = self.cur_device
        color_cal_type = d.color_cal_type
        log.debug("Color-cal: %s %s (type=%d) %s" % ("*"*20, self.cur_device.device_uri, color_cal_type, "*"*20))

        if color_cal_type == COLOR_CAL_TYPE_TYPHOON:
            dlg = ScrollDialog(ScrollColorCalView, self.cur_device, self.cur_printer, self.service, self)
            dlg.exec_loop()
        else:
            try:
                QApplication.setOverrideCursor(QApplication.waitCursor)

                try:
                    d.open()
                except Error:
                    self.CheckDeviceUI()
                else:
                    if d.isIdleAndNoError():
                        QApplication.restoreOverrideCursor()

                        if color_cal_type == COLOR_CAL_TYPE_DESKJET_450:
                            maint.colorCalType1(d, self.LoadPaperUI, self.ColorCalUI,
                                self.PhotoPenRequiredUI)

                        elif color_cal_type == COLOR_CAL_TYPE_MALIBU_CRICK:
                            maint.colorCalType2(d, self.LoadPaperUI, self.ColorCalUI2,
                                self.InvalidPenUI)

                        elif color_cal_type == COLOR_CAL_TYPE_STRINGRAY_LONGBOW_TORNADO:
                            maint.colorCalType3(d, self.LoadPaperUI, self.ColorAdjUI,
                                self.PhotoPenRequiredUI2)

                        elif color_cal_type == COLOR_CAL_TYPE_CONNERY:
                            maint.colorCalType4(d, self.LoadPaperUI, self.ColorCalUI4,
                                self.WaitUI)

                        elif color_cal_type == COLOR_CAL_TYPE_COUSTEAU:
                            maint.colorCalType5(d, self.LoadPaperUI)

                        elif color_cal_type == COLOR_CAL_TYPE_CARRIER:
                            maint.colorCalType6(d, self.LoadPaperUI)

                    else:
                        self.CheckDeviceUI()

            finally:
                d.close()
                QApplication.restoreOverrideCursor()


    def PrintTestPageButton_clicked(self):
        dlg = ScrollDialog(ScrollTestpageView, self.cur_device, self.cur_printer, self.service, self)
        dlg.exec_loop()


    def CleanUI1(self, msg=""):
        CFObj = CleaningForm(self, self.cur_device, 1)
        if msg:
            CFObj.CleaningText.setText(msg)
        return CFObj.exec_loop() == QDialog.Accepted


    def CleanUI2(self, msg=""):
        CFObj = CleaningForm(self, self.cur_device, 2)
        if msg:
            CFObj.CleaningText.setText(msg)
        return CFObj.exec_loop() == QDialog.Accepted


    def CleanUI3(self, msg=""):
        CleaningForm2(self).exec_loop()
        return True


    def WaitUI(self, seconds):
        WaitForm(seconds, None, self).exec_loop()


    def CleanPensButton_clicked(self):
        d = self.cur_device
        clean_type = d.clean_type
        log.debug("Clean: %s %s (type=%d) %s" % ("*"*20, self.cur_device.device_uri, clean_type, "*"*20))

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    QApplication.restoreOverrideCursor()

                    if clean_type == CLEAN_TYPE_PCL:
                        maint.cleaning(d, clean_type, maint.cleanType1, maint.primeType1,
                            maint.wipeAndSpitType1, self.LoadPaperUI,
                            self.CleanUI1, self.CleanUI2, self.CleanUI3,
                            self.WaitUI)

                    elif clean_type == CLEAN_TYPE_LIDIL:
                        maint.cleaning(d, clean_type, maint.cleanType2, maint.primeType2,
                            maint.wipeAndSpitType2, self.LoadPaperUI,
                            self.CleanUI1, self.CleanUI2, self.CleanUI3,
                            self.WaitUI)

                    elif clean_type == CLEAN_TYPE_PCL_WITH_PRINTOUT:
                        maint.cleaning(d, clean_type, maint.cleanType1, maint.primeType1,
                            maint.wipeAndSpitType1, self.LoadPaperUI,
                            self.CleanUI1, self.CleanUI2, self.CleanUI3,
                            self.WaitUI)

                    elif clean_type == CLEAN_TYPE_LEDM:
                        maint.cleaning(d, clean_type, maint.cleanTypeLedm, maint.cleanTypeLedm1,
                            maint.cleanTypeLedm2, self.LoadPaperUI,
                            self.CleanUI1, self.CleanUI2, self.CleanUI3,
                            self.WaitUI, maint.isCleanTypeLedmWithPrint)

                    elif clean_type == CLEAN_TYPE_UNSUPPORTED:
                        self.WarningUI(self.__tr("<p><b>Cleaning through HPLIP not supported for this printer. Please use the printer's front panel to perform cartridge cleaning.</b>"))

                else:
                    self.CheckDeviceUI()

        finally:
            d.close()
            QApplication.restoreOverrideCursor()


    def OpenEmbeddedBrowserButton_clicked(self):
        utils.openURL("http://%s" % self.cur_device.host)


    def faxAddressBookButton_clicked(self):
        self.RunCommand(self.cmd_fab)


    def faxSettingsButton_clicked(self):
        try:
            try:
                self.cur_device.open()
            except Error:
                self.CheckDeviceUI()
            else:
                try:
                    result_code, fax_num = self.cur_device.getPML(pml.OID_FAX_LOCAL_PHONE_NUM)
                except Error:
                    log.error("PML failure.")
                    self.FailureUI(self.__tr("<p><b>Operation failed. Device busy.</b>"))
                    return

                fax_num = str(fax_num)

                try:
                    result_code, name = self.cur_device.getPML(pml.OID_FAX_STATION_NAME)
                except Error:
                    log.error("PML failure.")
                    self.FailureUI(self.__tr("<p><b>Operation failed. Device busy.</b>"))
                    return

                name = str(name)

                dlg = FaxSettingsForm(self.cur_device, fax_num, name, self)
                dlg.exec_loop()

        finally:
            self.cur_device.close()


    def addressBookButton_clicked(self):
        self.RunCommand(self.cmd_fab)


    def ShowFirmwareDlg(self):
        dlg = FirmwareDialog(self, self.cur_device_uri)
        dlg.show()
        return dlg.exec_loop() == QDialog.Accepted

    # ***********************************************************************************
    #
    # STATUS TAB
    #
    # ***********************************************************************************

    def InitStatusTab(self):
        self.statusListView.setSorting(-1)
        self.statusListView.setColumnText(0, QString(""))
        #self.statusListView.setColumnWidthMode(0, QListView.Manual)
        self.statusListView.setColumnWidth(0, 16)


    def UpdateStatusTab(self):
        #log.debug("UpdateStatusTab()")
        self.UpdateHistory()
        self.UpdatePanel()
        self.UpdateStatusList()


    def UpdatePanel(self):
        if self.cur_device is not None and \
            self.cur_device.hist and \
            self.cur_device.supported:

            dq = self.cur_device.dq

            if dq.get('panel', 0) == 1:
                line1 = dq.get('panel-line1', '')
                line2 = dq.get('panel-line2', '')
            else:
                try:
                    line1 = device.queryString(self.cur_device.hist[0].event_code)
                except (AttributeError, TypeError):
                    line1 = ''

                line2 = ''

            pm = load_pixmap('panel_lcd', 'other')

            p = QPainter()
            p.begin(pm)
            p.setPen(QColor(0, 0, 0))
            p.setFont(self.font())

            x, y_line1, y_line2 = 10, 17, 33

            # TODO: Scroll long lines
            p.drawText(x, y_line1, line1)
            p.drawText(x, y_line2, line2)
            p.end()

            self.panel.setPixmap(pm)

        else:
            self.panel.setPixmap(load_pixmap('panel_lcd', 'other'))


    def UpdateHistory(self, dev=None):
        if self.dbus_avail:
            if dev is None:
                dev = self.cur_device

            return dev.queryHistory()

        self.cur_device.hist = [self.cur_device.last_event]



    def UpdateStatusList(self):
        self.statusListView.clear()
        row = 0
        hist = self.cur_device.hist[:]

        if hist:
            hist.reverse()
            row = len(hist)-1

            for e in hist:
                if e is None:
                    continue

                ess = device.queryString(e.event_code, 0)
                esl = device.queryString(e.event_code, 1)

                if row == 0:
                    desc = self.__tr("(most recent)")

                else:
                    desc = self.getTimeDeltaDesc(e.timedate)

                dt = QDateTime()
                dt.setTime_t(int(e.timedate), Qt.LocalTime)

                # TODO: In Qt4.x, use QLocale.toString(date, format)
                tt = QString("%1 %2").arg(dt.toString()).arg(desc)

                if e.job_id:
                    job_id = unicode(e.job_id)
                else:
                    job_id = u''

                error_state = STATUS_TO_ERROR_STATE_MAP.get(e.event_code, ERROR_STATE_CLEAR)
                tech_type = self.cur_device.tech_type

                try:
                    if tech_type in (TECH_TYPE_COLOR_INK, TECH_TYPE_MONO_INK):
                        status_pix = self.STATUS_ICONS[error_state][0] # ink
                    else:
                        status_pix = self.STATUS_ICONS[error_state][1] # laser
                except KeyError:
                    status_pix = self.STATUS_ICONS[ERROR_STATE_CLEAR][0]

                StatusListViewItem(self.statusListView, status_pix, ess, tt, unicode(e.event_code),
                    job_id, unicode(e.username))

                row -= 1

        i = self.statusListView.firstChild()
        if i is not None:
            self.statusListView.setCurrentItem(i)


    def getTimeDeltaDesc(self, past):
        t1 = QDateTime()
        t1.setTime_t(int(past))
        t2 = QDateTime.currentDateTime()
        delta = t1.secsTo(t2)
        return self.__tr("(about %1 ago)").arg(self.stringify(delta))


    # "Nicely readable timedelta"
    # Credit: Bjorn Lindqvist
    # ASPN Python Recipe 498062
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/498062
    # Note: Modified from recipe
    def seconds_in_units(self, seconds):
        unit_limits = [("year", 31536000),
                       ("month", 2592000),
                       ("week", 604800),
                       ("day", 86400),
                       ("hour", 3600),
                       ("minute", 60)]

        for unit_name, limit in unit_limits:
            if seconds >= limit:
                amount = int(round(float(seconds) / limit))
                return amount, unit_name

        return seconds, "second"


    def stringify(self, seconds):
        amount, unit_name = self.seconds_in_units(seconds)

        try:
            i18n_amount = self.num_repr[amount]
        except KeyError:
            i18n_amount = unicode(amount)

        if amount == 1:
            i18n_unit = self.unit_names[unit_name][0]
        else:
            i18n_unit = self.unit_names[unit_name][1]

        return QString("%1 %2").arg(i18n_amount).arg(i18n_unit)




    # ***********************************************************************************
    #
    # SUPPLIES TAB
    #
    # ***********************************************************************************

    def InitSuppliesTab(self):
        self.pix_battery = load_pixmap('battery', '16x16')

        yellow = "#ffff00"
        light_yellow = "#ffffcc"
        cyan = "#00ffff"
        light_cyan = "#ccffff"
        magenta = "#ff00ff"
        light_magenta = "#ffccff"
        black = "#000000"
        blue = "#0000ff"
        gray = "#808080"
        dark_gray = "#a9a9a9"
        light_gray = "#c0c0c0"
        red = "#ff0000"

        self.TYPE_TO_PIX_MAP = {
                               AGENT_TYPE_UNSPECIFIED : [black],
                               AGENT_TYPE_BLACK: [black],
                               AGENT_TYPE_MATTE_BLACK : [black],
                               AGENT_TYPE_PHOTO_BLACK : [dark_gray],
                               AGENT_TYPE_BLACK_B8800: [black],
                               AGENT_TYPE_CMY: [cyan, magenta, yellow],
                               AGENT_TYPE_KCM: [light_cyan, light_magenta, light_yellow],
                               AGENT_TYPE_GGK: [dark_gray],
                               AGENT_TYPE_YELLOW: [yellow],
                               AGENT_TYPE_MAGENTA: [magenta],
                               AGENT_TYPE_CYAN : [cyan],
                               AGENT_TYPE_CYAN_LOW: [light_cyan],
                               AGENT_TYPE_YELLOW_LOW: [light_yellow],
                               AGENT_TYPE_MAGENTA_LOW: [light_magenta],
                               AGENT_TYPE_BLUE: [blue],
                               AGENT_TYPE_KCMY_CM: [yellow, cyan, magenta],
                               AGENT_TYPE_LC_LM: [light_cyan, light_magenta],
                               #AGENT_TYPE_Y_M: [yellow, magenta],
                               #AGENT_TYPE_C_K: [black, cyan],
                               AGENT_TYPE_LG_PK: [light_gray, dark_gray],
                               AGENT_TYPE_LG: [light_gray],
                               AGENT_TYPE_G: [gray],
                               AGENT_TYPE_DG: [dark_gray],
                               AGENT_TYPE_PG: [light_gray],
                               AGENT_TYPE_C_M: [cyan, magenta],
                               AGENT_TYPE_K_Y: [black, yellow],
                               AGENT_TYPE_LC: [light_cyan],
                               AGENT_TYPE_RED : [red],
                               }

        self.suppliesList.setSorting(-1)
        self.suppliesList.setColumnText(0, QString(""))
        #self.suppliesList.setColumnWidthMode(0, QListView.Manual)
        self.suppliesList.setColumnWidth(0, 16)
        self.suppliesList.setColumnWidth(3, 100)


    def UpdateSuppliesTab(self):
        #log.debug("UpdateSuppliesTab()")

        self.suppliesList.clear()

        if self.cur_device is not None and \
            self.cur_device.supported and \
            self.cur_device.status_type != STATUS_TYPE_NONE and \
            self.cur_device.device_state != DEVICE_STATE_NOT_FOUND:

            try:
                self.cur_device.sorted_supplies
            except AttributeError:
                self.cur_device.sorted_supplies = []

            if not self.cur_device.sorted_supplies:
                a = 1
                while True:
                    try:
                        agent_type = int(self.cur_device.dq['agent%d-type' % a])
                        agent_kind = int(self.cur_device.dq['agent%d-kind' % a])
                        agent_sku = self.cur_device.dq['agent%d-sku' % a]
                    except KeyError:
                        break
                    else:
                        self.cur_device.sorted_supplies.append((a, agent_kind, agent_type, agent_sku))

                    a += 1

                self.cur_device.sorted_supplies.sort(lambda x, y: cmp(x[1], y[1]) or cmp(x[3], y[3]), reverse=True)


            for x in self.cur_device.sorted_supplies:
                a, agent_kind, agent_type, agent_sku = x
                agent_level = int(self.cur_device.dq['agent%d-level' % a])
                agent_desc = self.cur_device.dq['agent%d-desc' % a]
                agent_health_desc = self.cur_device.dq['agent%d-health-desc' % a]

                # Bar graph level
                level_pixmap = None
                if agent_kind in (AGENT_KIND_SUPPLY,
                                  AGENT_KIND_HEAD,
                                  AGENT_KIND_HEAD_AND_SUPPLY,
                                  AGENT_KIND_TONER_CARTRIDGE,
                                  AGENT_KIND_MAINT_KIT,
                                  AGENT_KIND_ADF_KIT,
                                  AGENT_KIND_INT_BATTERY,
                                  AGENT_KIND_DRUM_KIT,
                                  ):

                    level_pixmap = self.createBarGraph(agent_level, agent_type)

                # Color icon
                pixmap = None
                if agent_kind in (AGENT_KIND_SUPPLY,
                                  AGENT_KIND_HEAD,
                                  AGENT_KIND_HEAD_AND_SUPPLY,
                                  AGENT_KIND_TONER_CARTRIDGE,
                                  #AGENT_KIND_MAINT_KIT,
                                  #AGENT_KIND_ADF_KIT,
                                  AGENT_KIND_INT_BATTERY,
                                  #AGENT_KIND_DRUM_KIT,
                                  ):

                    pixmap = self.getIcon(agent_kind, agent_type)


                SuppliesListViewItem(self.suppliesList, pixmap, agent_desc,
                    agent_sku, level_pixmap, agent_health_desc)

            i = self.suppliesList.firstChild()
            if i is not None:
                self.suppliesList.setCurrentItem(i)




    def getIcon(self, agent_kind, agent_type):
        if agent_kind in (AGENT_KIND_SUPPLY,
                          AGENT_KIND_HEAD,
                          AGENT_KIND_HEAD_AND_SUPPLY,
                          AGENT_KIND_TONER_CARTRIDGE):

            map = self.TYPE_TO_PIX_MAP[agent_type]

            if isinstance(map, list):
                map_len = len(map)
                pix = QPixmap(16, 16) #, -1, QPixmap.DefaultOptim)
                pix.fill(qApp.palette().color(QPalette.Active, QColorGroup.Background))
                p = QPainter()
                p.begin(pix)
                p.setBackgroundMode(Qt.OpaqueMode)

                if map_len == 1:
                    p.setPen(QColor(map[0]))
                    p.setBrush(QBrush(QColor(map[0]), Qt.SolidPattern))
                    p.drawPie(2, 2, 10, 10, 0, 5760)

                elif map_len == 2:
                    p.setPen(QColor(map[0]))
                    p.setBrush(QBrush(QColor(map[0]), Qt.SolidPattern))
                    p.drawPie(2, 4, 8, 8, 0, 5760)

                    p.setPen(QColor(map[1]))
                    p.setBrush(QBrush(QColor(map[1]), Qt.SolidPattern))
                    p.drawPie(6, 4, 8, 8, 0, 5760)

                elif map_len == 3:
                    p.setPen(QColor(map[2]))
                    p.setBrush(QBrush(QColor(map[2]), Qt.SolidPattern))
                    p.drawPie(6, 6, 8, 8, 0, 5760)

                    p.setPen(QColor(map[1]))
                    p.setBrush(QBrush(QColor(map[1]), Qt.SolidPattern))
                    p.drawPie(2, 6, 8, 8, 0, 5760)

                    p.setPen(QColor(map[0]))
                    p.setBrush(QBrush(QColor(map[0]), Qt.SolidPattern))
                    p.drawPie(4, 2, 8, 8, 0, 5760)

                p.end()
                return pix

            else:
                return map

        elif agent_kind == AGENT_KIND_INT_BATTERY:
                return self.pix_battery


    def createBarGraph(self, percent, agent_type, w=100, h=18):
        fw = w/100*percent
        px = QPixmap(w, h)
        px.fill(qApp.palette().color(QPalette.Active, QColorGroup.Background))

        pp = QPainter(px)
        pp.setPen(Qt.black)
        pp.setBackgroundColor(qApp.palette().color(QPalette.Active, QColorGroup.Base))

        map = self.TYPE_TO_PIX_MAP[agent_type]
        map_len = len(map)

        if map_len == 1 or map_len > 3:
            pp.fillRect(0, 0, fw, h, QBrush(QColor(map[0])))

        elif map_len == 2:
            h2 = h / 2
            pp.fillRect(0, 0, fw, h2, QBrush(QColor(map[0])))
            pp.fillRect(0, h2, fw, h, QBrush(QColor(map[1])))

        elif map_len == 3:
            h3 = h / 3
            h23 = 2 * h3
            pp.fillRect(0, 0, fw, h3, QBrush(QColor(map[0])))
            pp.fillRect(0, h3, fw, h23, QBrush(QColor(map[1])))
            pp.fillRect(0, h23, fw, h, QBrush(QColor(map[2])))

        # draw black frame
        pp.drawRect(0, 0, w, h)

        if percent > 75 and agent_type in \
          (AGENT_TYPE_BLACK, AGENT_TYPE_UNSPECIFIED, AGENT_TYPE_BLUE):
            pp.setPen(Qt.white)

        # 75% ticks
        w1 = 3 * w / 4
        h6 = h / 6
        pp.drawLine(w1, 0, w1, h6)
        pp.drawLine(w1, h, w1, h-h6)

        if percent > 50 and agent_type in \
          (AGENT_TYPE_BLACK, AGENT_TYPE_UNSPECIFIED, AGENT_TYPE_BLUE):
            pp.setPen(Qt.white)

        # 50% ticks
        w2 = w / 2
        h4 = h / 4
        pp.drawLine(w2, 0, w2, h4)
        pp.drawLine(w2, h, w2, h-h4)

        if percent > 25 and agent_type in \
          (AGENT_TYPE_BLACK, AGENT_TYPE_UNSPECIFIED, AGENT_TYPE_BLUE):
            pp.setPen(Qt.white)

        # 25% ticks
        w4 = w / 4
        pp.drawLine(w4, 0, w4, h6)
        pp.drawLine(w4, h, w4, h-h6)

        return px



    # ***********************************************************************************
    #
    # PRINTER SETTINGS TAB
    #
    # ***********************************************************************************

    def InitPrintSettingsTab(self): # Add Scrolling Print Settings
        PrintJobsTabLayout = QGridLayout(self.PrintSettingsTab,1,1,11,6,"PrintJobsTabLayout")

        self.PrintSettingsList = ScrollPrintSettingsView(self.service, self.PrintSettingsTab, "PrintSettingsView")
        PrintJobsTabLayout.addMultiCellWidget(self.PrintSettingsList,1,1,0,3)

        self.PrintSettingsPrinterCombo = QComboBox(0,self.PrintSettingsTab,"comboBox5")

        self.PrintSettingsPrinterCombo.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed,0,0,
            self.PrintSettingsPrinterCombo.sizePolicy().hasHeightForWidth()))

        PrintJobsTabLayout.addWidget(self.PrintSettingsPrinterCombo, 0, 2)

        self.settingTextLabel = QLabel(self.PrintSettingsTab,"self.settingTextLabel")
        PrintJobsTabLayout.addWidget(self.settingTextLabel,0,1)

        self.settingTextLabel.setText(self.__tr("Printer Name:"))

        spacer34 = QSpacerItem(20,20,QSizePolicy.Preferred, QSizePolicy.Minimum)
        PrintJobsTabLayout.addItem(spacer34,0,3)

        spacer35 = QSpacerItem(20,20,QSizePolicy.Preferred, QSizePolicy.Minimum)
        PrintJobsTabLayout.addItem(spacer35,0,0)

        self.connect(self.PrintSettingsPrinterCombo, SIGNAL("activated(const QString&)"),
            self.PrintSettingsPrinterCombo_activated)


    def UpdatePrintSettingsTab(self):
        #log.debug("UpdatePrintSettingsTab()")
        if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
            self.settingTextLabel.setText(self.__tr("Printer Name:"))
        else:
            self.settingTextLabel.setText(self.__tr("Fax Name:"))

        self.PrintSettingsList.onDeviceChange(self.cur_device)


    def UpdatePrintSettingsTabPrinter(self):
        self.PrintSettingsList.onPrinterChange(self.cur_printer)


    # ***********************************************************************************
    #
    # PRINTER CONTROL TAB
    #
    # ***********************************************************************************

    def InitPrintControlTab(self):
        self.JOB_STATES = { cups.IPP_JOB_PENDING : self.__tr("Pending"),
                            cups.IPP_JOB_HELD : self.__tr("On hold"),
                            cups.IPP_JOB_PROCESSING : self.__tr("Printing"),
                            cups.IPP_JOB_STOPPED : self.__tr("Stopped"),
                            cups.IPP_JOB_CANCELLED : self.__tr("Canceled"),
                            cups.IPP_JOB_ABORTED : self.__tr("Aborted"),
                            cups.IPP_JOB_COMPLETED : self.__tr("Completed"),
                           }

        self.cancelToolButton.setIconSet(QIconSet(load_pixmap('cancel', '16x16')))
        self.infoToolButton.setIconSet(QIconSet(load_pixmap('info', '16x16')))

        self.JOB_STATE_ICONS = { cups.IPP_JOB_PENDING: self.busy_pix,
                                 cups.IPP_JOB_HELD : self.busy_pix,
                                 cups.IPP_JOB_PROCESSING : self.print_pix,
                                 cups.IPP_JOB_STOPPED : self.warning_pix,
                                 cups.IPP_JOB_CANCELLED : self.warning_pix,
                                 cups.IPP_JOB_ABORTED : self.error_pix,
                                 cups.IPP_JOB_COMPLETED : self.ok_pix,
                                }

        self.jobList.setSorting(-1)
        self.jobList.setColumnText(0, QString(""))
        #self.jobList.setColumnWidthMode(0, QListView.Manual)
        self.jobList.setColumnWidth(0, 16)
        self.jobList.setColumnText(1, QString(""))
        #self.jobList.setColumnWidthMode(1, QListView.Manual)
        self.jobList.setColumnWidth(1, 16)
        self.jobList.setColumnWidth(2, 300)
        self.cancelToolButton.setEnabled(False)
        self.infoToolButton.setEnabled(False)

        self.printer_state = cups.IPP_PRINTER_STATE_IDLE

        # TODO: Check queues at startup and send events if stopped or rejecting


    def UpdatePrintControlTab(self):
        #log.debug("UpdatePrintControlTab()")

        if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
            self.printerTextLabel.setText(self.__tr("Printer Name:"))
            self.groupBox1.setTitle(self.__tr("Printer Queue Control"))

        else:
            self.printerTextLabel.setText(self.__tr("Fax Name:"))
            self.groupBox1.setTitle(self.__tr("Fax Queue Control"))

        self.jobList.clear()
        self.UpdatePrintController()

        jobs = cups.getJobs()
        num_jobs = 0
        for j in jobs:
            if j.dest.decode('utf-8') == unicode(self.cur_printer):
                num_jobs += 1

        for j in jobs:
            if j.dest == self.cur_printer:
                JobListViewItem(self.jobList, self.JOB_STATE_ICONS[j.state],
                    j.title, self.JOB_STATES[j.state], unicode(j.id))

        i = self.jobList.firstChild()
        if i is not None:
            self.jobList.setCurrentItem(i)


    def jobList_clicked(self, i):
        num = 0
        item = self.jobList.firstChild()
        while item is not None:
            if item.isOn():
                num += 1

            item = item.nextSibling()

        self.cancelToolButton.setEnabled(num)
        self.infoToolButton.setEnabled(num == 1)


    def infoToolButton_clicked(self):
        item = self.jobList.firstChild()
        while item is not None:
            if item.isOn():
                return self.showJobInfoDialog(item)

            item = item.nextSibling()


    def cancelToolButton_clicked(self):
        self.cancelCheckedJobs()


    def jobList_contextMenuRequested(self, item, pos, a2):
        if item is not None and item is self.jobList.currentItem():
            popup = QPopupMenu(self)

            popup.insertItem(self.__tr("Cancel Job"), self.cancelJob)
            popup.insertSeparator()
            popup.insertItem(self.__tr("View Job Log (advanced)..."), self.getJobInfo)

            popup.popup(pos)


    def cancelJob(self):
        item = self.jobList.currentItem()

        if item is not None:
            self.cur_device.cancelJob(int(item.job_id))


    def getJobInfo(self):
        return self.showJobInfoDialog(self.jobList.currentItem())


    def showJobInfoDialog(self, item):
        if item is not None:
            text = cups.getPrintJobErrorLog(int(item.job_id))

            if text:
                dlg = JobInfoDialog(text, self)
                dlg.setCaption(self.__tr("HP Device Manager - Job Log - %1 - Job %2").\
                    arg(self.cur_printer).arg(unicode(item.job_id)))

                dlg.exec_loop()

            else:
                self.FailureUI(self.__tr("<b>No log output found.</b><p>If the print job is stopped or the printer is rejecting jobs, there might not be any output. Also, you will receive more output in the CUPS LogLevel is set to 'debug'."))


    def UpdatePrintController(self):
        # default printer
        self.defaultPushButton.setText(self.__tr("Set as Default"))
        
        if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
            device_string = "Printer"
        else:
            device_string = "Fax"

        
        default_printer = cups.getDefaultPrinter()
        if default_printer is not None:
            default_printer = default_printer.decode('utf8')

        if default_printer == self.cur_printer:
            s = self.__tr("SET AS DEFAULT")
            self.defaultPushButton.setEnabled(False)

        else:
            s = self.__tr("NOT SET AS DEFAULT")
            self.defaultPushButton.setEnabled(True)

        QToolTip.add(self.defaultPushButton, self.__tr("The %2 is currently: %1").arg(s,device_string))


        self.printer_state = cups.IPP_PRINTER_STATE_IDLE

        cups_printers = cups.getPrinters()

        for p in cups_printers:
            if p.name.decode('utf-8') == self.cur_printer:
                self.printer_state = p.state
                self.printer_accepting = p.accepting
                break

        # start/stop
        if self.printer_state == cups.IPP_PRINTER_STATE_IDLE:
            s = self.__tr("IDLE")
            self.stopstartPushButton.setText(self.__tr("Stop %s"%device_string))

        elif self.printer_state == cups.IPP_PRINTER_STATE_PROCESSING:
            s = self.__tr("PROCESSING")
            self.stopstartPushButton.setText(self.__tr("Stop %s"%device_string))

        else:
            s = self.__tr("STOPPED")
            self.stopstartPushButton.setText(self.__tr("Start %s"%device_string))

        QToolTip.add(self.stopstartPushButton, self.__tr("The %2 is currently: %1").arg(s,device_string))

        # reject/accept
        if self.printer_accepting:
            s = self.__tr("ACCEPTING JOBS")
            self.rejectacceptPushButton.setText(self.__tr("Reject Jobs"))

        else:
            s = self.__tr("REJECTING JOBS")
            self.rejectacceptPushButton.setText(self.__tr("Accept Jobs"))

        QToolTip.add(self.rejectacceptPushButton, self.__tr("The %2 is currently: %1").arg(s,device_string))



    def stopstartPushButton_clicked(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            if self.printer_state in (cups.IPP_PRINTER_STATE_IDLE, cups.IPP_PRINTER_STATE_PROCESSING):

                result, result_str = cups.cups_operation(cups.stop, GUI_MODE, 'qt3', self, self.cur_printer)
                if result == cups.IPP_OK:
                    if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                        e = EVENT_PRINTER_QUEUE_STOPPED
                    else:
                        e = EVENT_FAX_QUEUE_STOPPED

            else:
                result, result_str = cups.cups_operation(cups.start, GUI_MODE, 'qt3', self, self.cur_printer)
                if result == cups.IPP_OK:
                    if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                        e = EVENT_PRINTER_QUEUE_STARTED
                    else:
                        e = EVENT_FAX_QUEUE_STARTED

            if result == cups.IPP_OK:
                self.UpdatePrintController()
                self.cur_device.sendEvent(e, self.cur_printer)
            else:
                log.error("Start/Stop printer operation failed")
                self.FailureUI(self.__tr("<b>Start/Stop printer operation failed.</b><p> Error : %s"%result_str))
                cups.releaseCupsInstance()

        finally:
            QApplication.restoreOverrideCursor()


    def rejectacceptPushButton_clicked(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            if self.printer_accepting:
                result ,result_str = cups.cups_operation(cups.reject, GUI_MODE, 'qt3', self, self.cur_printer)
                if result == cups.IPP_OK:
                    if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                        e = EVENT_PRINTER_QUEUE_REJECTING_JOBS
                    else:
                        e = EVENT_FAX_QUEUE_REJECTING_JOBS

            else:
                result ,result_str = cups.cups_operation(cups.accept, GUI_MODE, 'qt3', self, self.cur_printer)
                if result == cups.IPP_OK:
                    if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                        e = EVENT_PRINTER_QUEUE_ACCEPTING_JOBS
                    else:
                        e = EVENT_FAX_QUEUE_ACCEPTING_JOBS

            if result == cups.IPP_OK:
                self.UpdatePrintController()
                self.cur_device.sendEvent(e, self.cur_printer)
            else:
                log.error("Reject/Accept jobs operation failed")
                self.FailureUI(self.__tr("<b>Accept/Reject printer operation failed.</b><p>Error : %s"%result_str))
                cups.releaseCupsInstance()

        finally:
            QApplication.restoreOverrideCursor()


    def defaultPushButton_clicked(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            result, result_str = cups.cups_operation(cups.setDefaultPrinter, GUI_MODE, 'qt3', self, self.cur_printer.encode('utf8'))

            if result != cups.IPP_OK:
                log.error("Set default printer failed.")
                self.FailureUI(self.__tr("<b>Set default printer operation failed.</b><p>Error : %s"%result_str))
                cups.releaseCupsInstance()
            else:
                self.UpdatePrintController()
                if self.cur_device.device_type == DEVICE_TYPE_PRINTER:
                    e = EVENT_PRINTER_QUEUE_SET_AS_DEFAULT
                else:
                    e = EVENT_FAX_QUEUE_SET_AS_DEFAULT

                self.cur_device.sendEvent(e, self.cur_printer)

        finally:
            QApplication.restoreOverrideCursor()


    def cancelCheckedJobs(self):
        QApplication.setOverrideCursor(QApplication.waitCursor)
        try:
            item = self.jobList.firstChild()
            while item is not None:
                if item.isOn():
                    self.cur_device.cancelJob(int(item.job_id))

                item = item.nextSibling()

        finally:
            QApplication.restoreOverrideCursor()

        self.UpdatePrintControlTab()

    def UpdateUpgradeTab(self):
        log.debug("Upgrade Tab is pressed")
        self.InstallPushButton_lock = False

    def InstallPushButton_clicked(self):
        if self.InstallPushButton_lock is True:
            return

        if self.Is_autoInstaller_distro:
            self.InstallPushButton.setEnabled(False)
            terminal_cmd = utils.get_terminal()
            if terminal_cmd is not None and utils.which("hp-upgrade"):
                cmd = terminal_cmd + " 'hp-upgrade -w'"
                os_utils.execute(cmd)
            else:
                log.error("Failed to run hp-upgrade command from terminal =%s "%terminal_cmd)
            self.InstallPushButton.setEnabled(True)
        else:
            self.InstallPushButton_lock = True
            utils.openURL("http://hplipopensource.com/hplip-web/install/manual/index.html")
            QTimer.singleShot(1000, self.InstallPushButton_unlock)

    def InstallPushButton_unlock(self):
        self.InstallPushButton_lock = False

    # ***********************************************************************************
    #
    # EXIT/CHILD CLEANUP
    #
    # ***********************************************************************************

    def closeEvent(self, event):
        self.Cleanup()
        self.request_queue.put(None)
        event.accept()


    def Cleanup(self):
        self.request_queue.put(None)
        self.CleanupChildren()
        if not self.update_thread.wait(5000):
            self.update_thread.terminate()


    def CleanupChildren(self):
        log.debug("Cleaning up child processes.")
        try:
            os.waitpid(-1, os.WNOHANG)
        except OSError:
            pass


    # ***********************************************************************************
    #
    # DEVICE SETTINGS PLUGIN
    #
    # ***********************************************************************************

    def CheckForDeviceSettingsUI(self, dev):
        dev.device_settings_ui = None
        name = '.'.join(['plugins', dev.model])
        log.debug("Attempting to load plugin: %s" % name)
        try:
            mod = __import__(name, globals(), locals(), [])
        except ImportError:
            log.debug("No plugin found.")
            return
        else:
            components = name.split('.')
            for c in components[1:]:
                mod = getattr(mod, c)
            log.debug("Loaded: %s" % repr(mod))
            dev.device_settings_ui = mod.settingsUI


    # ***********************************************************************************
    #
    # SETTINGS DIALOG
    #
    # ***********************************************************************************

    def settingsConfigure_activated(self, tab_to_show=0):
        dlg = SettingsDialog(self)
        dlg.TabWidget.setCurrentPage(tab_to_show)

        if dlg.exec_loop() == QDialog.Accepted:
            old_auto_refresh = self.user_settings.auto_refresh_rate
            self.user_settings.load()

            if self.user_settings.auto_refresh and old_auto_refresh != self.user_settings.auto_refresh_rate:
                self.refresh_timer.changeInterval(self.user_settings.auto_refresh_rate * 1000)

            if old_auto_refresh != self.user_settings.auto_refresh:
                self.autoRefresh.toggle()


    # ***********************************************************************************
    #
    # SETUP/REMOVE
    #
    # ***********************************************************************************

    def deviceInstallAction_activated(self):
        if utils.which('hp-setup'):
            cmd = 'hp-setup -u'
        else:
            cmd = 'python ./setup.py --gui'

        log.debug(cmd)
        utils.run(cmd)
        self.RescanDevices()


    def deviceRemoveAction_activated(self):
        if self.cur_device is not None:
            x = QMessageBox.critical(self,
           self.caption(),
           self.__tr("<b>Annoying Confirmation: Are you sure you want to remove this device?</b>"),
            QMessageBox.Yes,
            QMessageBox.No | QMessageBox.Default,
            QMessageBox.NoButton)
            if x == QMessageBox.Yes:
                QApplication.setOverrideCursor(QApplication.waitCursor)
                print_uri = self.cur_device.device_uri
                fax_uri = print_uri.replace('hp:', 'hpfax:')

                log.debug(print_uri)
                log.debug(fax_uri)

                self.cups_devices = device.getSupportedCUPSDevices(['hp', 'hpfax'])

                for d in self.cups_devices:
                    if d in (print_uri, fax_uri):
                        for p in self.cups_devices[d]:
                            log.debug("Removing %s" % p)
                            r, result_str = cups.cups_operation(cups.delPrinter, GUI_MODE, 'qt3', self, p)

                            if r != cups.IPP_OK:
                                self.FailureUI(self.__tr("<p><b>Delete printer queue fails.</b><p>Error : %s"%result_str))
                                print_uri =""   # Ignoring further devices delete operation, as authentication is failed or cancelled.
                                fax_uri = ""

                self.cur_device = None
                self.cur_device_uri = ''
                user_conf.set('last_used', 'device_uri', '')
                QApplication.restoreOverrideCursor()

                self.RescanDevices()


    # ***********************************************************************************
    #
    # MISC
    #
    # ***********************************************************************************


    def RunCommand(self, cmd, macro_char='%'):
        QApplication.setOverrideCursor(QApplication.waitCursor)

        try:
            if len(cmd) == 0:
                self.FailureUI(self.__tr("<p><b>Unable to run command. No command specified.</b><p>Use <pre>Configure...</pre> to specify a command to run."))
                log.error("No command specified. Use settings to configure commands.")
            else:
                log.debug("Run: %s %s (%s) %s" % ("*"*20, cmd, self.cur_device_uri, "*"*20))
                log.debug(cmd)

                try:
                    cmd = ''.join([self.cur_device.device_vars.get(x, x) \
           for x in cmd.split(macro_char)])
                except AttributeError:
                    pass

                log.debug(cmd)

                path = cmd.split()[0]
                args = cmd.split()

                log.debug(path)
                log.debug(args)

                self.CleanupChildren()
                os.spawnvp(os.P_NOWAIT, path, args)
                qApp.processEvents()

        finally:
            QApplication.restoreOverrideCursor()


    def helpContents(self):
        f = "http://hplip.sf.net"

        if prop.doc_build:
            g = os.path.join(sys_conf.get('dirs', 'doc'), 'index.html')
            if os.path.exists(g):
                f = "file://%s" % g

        log.debug(f)
        utils.openURL(f)


    def helpAbout(self):
        dlg = AboutDlg(self)
        dlg.VersionText.setText(prop.version)
        dlg.ToolboxVersionText.setText(self.toolbox_version + " (Qt3)")
        dlg.exec_loop()


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
        return qApp.translate("DevMgr4",s,c)



# ***********************************************************************************
#
# ScrollDeviceInfoView (View Device Information)
#
# ***********************************************************************************

class ScrollDeviceInfoView(ScrollView):
    def __init__(self, service, parent=None, form=None, name=None, fl=0):
        ScrollView.__init__(self, service, parent, name, fl)


    def fillControls(self):
        ScrollView.fillControls(self)
        self.addDeviceInfo()
        self.maximizeControl()


    def addDeviceInfo(self):
        self.addGroupHeading("info_title", self.__tr("Device Information"))

        widget = self.getWidget()

        layout37 = QGridLayout(widget,1,1,5,10,"layout37")

        self.infoListView = QListView(widget,"fileListView")
        self.infoListView.addColumn(self.__tr("Static/Dynamic"))
        self.infoListView.addColumn(self.__tr("Key"))
        self.infoListView.addColumn(self.__tr("Value"))
        self.infoListView.setAllColumnsShowFocus(1)
        self.infoListView.setShowSortIndicator(1)
        self.infoListView.setColumnWidth(0, 50)
        self.infoListView.setColumnWidth(1, 150)
        self.infoListView.setColumnWidth(2, 300)
        self.infoListView.setItemMargin(2)
        self.infoListView.setSorting(-1)

        layout37.addMultiCellWidget(self.infoListView,1,1,0,3)

        mq_keys = self.cur_device.mq.keys()
        mq_keys.sort()
        mq_keys.reverse()
        for key,i in zip(mq_keys, range(len(mq_keys))):
            QListViewItem(self.infoListView, self.__tr("Static"), key, str(self.cur_device.mq[key]))

        dq_keys = self.cur_device.dq.keys()
        dq_keys.sort()
        dq_keys.reverse()
        for key,i in zip(dq_keys, range(len(dq_keys))):
            QListViewItem(self.infoListView, self.__tr("Dynamic"), key, str(self.cur_device.dq[key]))

        self.addWidget(widget, "file_list", maximize=True)


    def __tr(self,s,c = None):
        return qApp.translate("ScrollDeviceInfoView",s,c)



# ***********************************************************************************
#
# ScrollTestpageView (Print Test Page)
#
# ***********************************************************************************

class ScrollTestpageView(ScrollView):
    def __init__(self, service, parent=None, form=None, name=None, fl=0):
        ScrollView.__init__(self, service, parent, name, fl)
        self.dialog = parent


    def fillControls(self):
        ScrollView.fillControls(self)

        if self.addPrinterFaxList():
            self.addTestpageType()

            self.addLoadPaper()

            self.printButton = self.addActionButton("bottom_nav", self.__tr("Print Test Page"),
                self.printButton_clicked, 'print.png', None)


    def addTestpageType(self):
        self.addGroupHeading("testpage_type", self.__tr("Test Page Type"))
        widget = self.getWidget()

        Form4Layout = QGridLayout(widget,1,1,5,10,"Form4Layout")

        self.buttonGroup3 = QButtonGroup(widget,"buttonGroup3")
        self.buttonGroup3.setLineWidth(0)
        self.buttonGroup3.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup3.layout().setSpacing(5)
        self.buttonGroup3.layout().setMargin(10)

        buttonGroup3Layout = QGridLayout(self.buttonGroup3.layout())
        buttonGroup3Layout.setAlignment(Qt.AlignTop)

        self.radioButton6 = QRadioButton(self.buttonGroup3,"radioButton6")
        self.radioButton6.setEnabled(False)
        buttonGroup3Layout.addWidget(self.radioButton6,1,0)

        self.radioButton5 = QRadioButton(self.buttonGroup3,"radioButton5")
        self.radioButton5.setChecked(1)
        buttonGroup3Layout.addWidget(self.radioButton5,0,0)

        Form4Layout.addWidget(self.buttonGroup3,0,0)

        self.radioButton6.setText(self.__tr("Printer diagnostic page (does not test print driver)"))
        self.radioButton5.setText(self.__tr("HPLIP test page (tests print driver)"))

        self.addWidget(widget, "page_type")


    def printButton_clicked(self):
        d = self.cur_device
        printer_name = self.cur_printer
        printed = False

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                try:
                    if d.isIdleAndNoError():
                        QApplication.restoreOverrideCursor()
                        d.close()

                        d.printTestPage(printer_name)
                        printed = True

                    else:
                        d.close()
                        self.CheckDeviceUI()
                except Error:
                    self.CheckDeviceUI()

        finally:
            QApplication.restoreOverrideCursor()

        if printed:
            QMessageBox.information(self,
                self.caption(),
                self.__tr("<p><b>A test page should be printing on your printer.</b><p>If the page fails to print, please visit http://hplip.sourceforge.net for troubleshooting and support."),
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton)

        self.dialog.accept()


    def CheckDeviceUI(self):
            self.FailureUI(self.__tr("<b>Device is busy or in an error state.</b><p>Please check device and try again."))


    def FailureUI(self, error_text):
        QMessageBox.critical(self,
            self.caption(),
            error_text,
            QMessageBox.Ok,
            QMessageBox.NoButton,
            QMessageBox.NoButton)


    def __tr(self,s,c = None):
        return qApp.translate("ScrollTestpageView",s,c)

# ***********************************************************************************
#
# ScrollPrinterInfoView (View Device Information)
#
# ***********************************************************************************

class ScrollPrinterInfoView(ScrollView):
    def __init__(self, service, parent = None, form=None, name = None,fl = 0):
        ScrollView.__init__(self, service, parent, name, fl)


    def fillControls(self):
        ScrollView.fillControls(self)

        printers = []
        for p in self.printers:
            if p.device_uri == self.cur_device.device_uri:
                printers.append(p)

        if not printers:
            self.addGroupHeading("error_title", self.__tr("No printers found for this device."))
        else:
            for p in printers:
                self.addPrinterInfo(p)

        self.maximizeControl()


    def addPrinterInfo(self, p):
        self.addGroupHeading(p.name, p.name)
        widget = self.getWidget()

        layout1 = QVBoxLayout(widget,5,10,"layout1")

        textLabel2 = QLabel(widget,"textLabel2")

        if p.device_uri.startswith("hpfax:"):
            s = self.__tr("Fax")
        else:
            s = self.__tr("Printer")

        textLabel2.setText(self.__tr("Type: %1").arg(s))
        layout1.addWidget(textLabel2)

        textLabel3 = QLabel(widget,"textLabel3")
        textLabel3.setText(self.__tr("Location: %1").arg(p.location))
        layout1.addWidget(textLabel3)

        textLabel4 = QLabel(widget,"textLabel4")
        textLabel4.setText(self.__tr("Description/Info: %1").arg(p.info))
        layout1.addWidget(textLabel4)

        textLabel5 = QLabel(widget,"textLabel5")

        if p.state == cups.IPP_PRINTER_STATE_IDLE:
            s = self.__tr("Idle")
        elif p.state == cups.IPP_PRINTER_STATE_PROCESSING:
            s = self.__tr("Processing")
        elif p.state == cups.IPP_PRINTER_STATE_STOPPED:
            s = self.__tr("Stopped")
        else:
            s = self.__tr("Unknown")

        textLabel5.setText(self.__tr("State: %1").arg(s))
        layout1.addWidget(textLabel5)

        textLabel6 = QLabel(widget,"textLabel6")
        textLabel6.setText(self.__tr("PPD/Driver: %1").arg(p.makemodel))
        layout1.addWidget(textLabel6)

        textLabel7 = QLabel(widget,"textLabel7")
        textLabel7.setText(self.__tr("CUPS/IPP Printer URI: %1").arg(p.printer_uri))
        layout1.addWidget(textLabel7)

        self.addWidget(widget, p.name)


    def __tr(self,s,c = None):
        return qApp.translate("ScrollPrinterInfoView",s,c)




# ***********************************************************************************
#
# Color cal type 7
#
# ***********************************************************************************

class ScrollColorCalView(ScrollView):
    def __init__(self, service, parent = None, form=None, name = None,fl = 0):
        ScrollView.__init__(self, service, parent, name, fl)
        self.dialog = parent


    def fillControls(self):
        ScrollView.fillControls(self)
        self.addLoadPaper(PAPER_TYPE_HP_ADV_PHOTO)

        self.printButton = self.addActionButton("bottom_nav", self.__tr("Perform Color Calibration"),
            self.colorcalButton_clicked, 'print.png', None)


    def colorcalButton_clicked(self):
        d = self.cur_device
        printer_name = self.cur_printer
        printed = False

        try:
            QApplication.setOverrideCursor(QApplication.waitCursor)

            try:
                d.open()
            except Error:
                self.CheckDeviceUI()
            else:
                if d.isIdleAndNoError():
                    QApplication.restoreOverrideCursor()
                    d.close()

                    d.setPML(pml.OID_PRINT_INTERNAL_PAGE, pml.PRINT_INTERNAL_PAGE_AUTOMATIC_COLOR_CALIBRATION)
                    printed = True

                else:
                    d.close()
                    self.CheckDeviceUI()

        finally:
            QApplication.restoreOverrideCursor()

        if printed:
            QMessageBox.information(self,
                self.caption(),
                self.__tr("<p><b>A test page should be printing on your printer.</b><p>If the page fails to print, please visit http://hplip.sourceforge.net for troubleshooting and support."),
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton)

        self.dialog.accept()


    def CheckDeviceUI(self):
            self.FailureUI(self.__tr("<b>Device is busy or in an error state.</b><p>Please check device and try again."))


    def FailureUI(self, error_text):
        QMessageBox.critical(self,
            self.caption(),
            error_text,
            QMessageBox.Ok,
            QMessageBox.NoButton,
            QMessageBox.NoButton)


    def __tr(self,s,c = None):
        return qApp.translate("ScrollColorCalView",s,c)
