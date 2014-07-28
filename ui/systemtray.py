#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2008 Hewlett-Packard Development Company, L.P.
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
# Authors: Don Welch, Torsten Marek

# Std Lib
import sys
import struct
import select
import os
import signal
import os.path
import time

# Local
from base.g import *
from base import device, utils
from ui_utils import load_pixmap

# Qt
try:
    from qt import *
except ImportError:
    log.error("Python bindings for Qt3 not found. Exiting!")
    sys.exit(1)

# C types
try:
    import ctypes as c
    import ctypes.util as cu
except ImportError:
    log.error("Qt3 version of hp-systray requires python-ctypes module. Exiting!")
    sys.exit(1)

# dbus
try:
    import dbus
    from dbus import SessionBus, lowlevel
except ImportError:
    log.error("Python bindings for dbus not found. Exiting!")
    sys.exit(1)


# pynotify (optional)
have_pynotify = True
try:
    import pynotify
except ImportError:
    have_pynotify = False


TrayIcon_Warning = 0
TrayIcon_Critical = 1
TrayIcon_Information = 2

theBalloonTip = None
UPGRADE_CHECK_DELAY=24*60*60*1000               #1 day
CLEAN_EXEC_DELAY=4*60*60*1000                  #4 Hrs

class BalloonTip(QDialog):
    def __init__(self, msg_icon, title, msg, tray_icon):
        QDialog.__init__(self, tray_icon, "BalloonTip", False,
        Qt.WStyle_StaysOnTop | Qt.WStyle_Customize | Qt.WStyle_NoBorder | Qt.WStyle_Tool | Qt.WX11BypassWM)

        self.timerId = None
        self.bubbleActive = False

        QObject.connect(tray_icon, SIGNAL("destroyed()"), self.close)

        self.titleLabel = QLabel(self)
        self.titleLabel.installEventFilter(self)
        self.titleLabel.setText(title)
        f = self.titleLabel.font()
        f.setBold(True)
        self.titleLabel.setFont(f)
        self.titleLabel.setTextFormat(Qt.PlainText) # to maintain compat with windows

        self.closeButton = QPushButton(self)
        self.closeButton.setPixmap(load_pixmap('close', '16x16'))
        self.closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeButton.setFixedSize(18, 18)
        QObject.connect(self.closeButton, SIGNAL("clicked()"), self.close)

        self.msgLabel = QLabel(self)
        self.msgLabel.installEventFilter(self)
        self.msgLabel.setText(msg)
        self.msgLabel.setTextFormat(Qt.PlainText)
        self.msgLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        layout = QGridLayout(self)
        if msg_icon is not None:
            self.iconLabel = QLabel(self)
            self.iconLabel.setPixmap(msg_icon)
            self.iconLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.iconLabel.setMargin(2)
            layout.addWidget(self.iconLabel, 0, 0)
            layout.addWidget(self.titleLabel, 0, 1)
        else:
            layout.addMultiCellWidget(self.titleLabel, 0, 1, 0, 2)

        layout.addWidget(self.closeButton, 0, 3)
        layout.addMultiCellWidget(self.msgLabel, 1, 1, 0, 3)
        layout.setMargin(3)
        self.setPaletteBackgroundColor(QColor(255, 255, 224))


    def resizeEvent(self, e):
        QWidget.resizeEvent(self, e)


    def mousePressEvent(self, e):
        self.close()
        if e.button() == Qt.LeftButton:
            pass # TODO


    def timerEvent(self, e):
        if e.timerId() == self.timerId:
            self.killTimer(self.timerId)
            self.hide()
            self.close()

            return

        QWidget.timerEvent(self, e)


    def closeEvent(self, event):
        self.bubbleActive = False
        event.accept()


    def balloon(self, pos, msecs, showArrow):
        if self.bubbleActive:
            return

        self.bubbleActive = True

        scr = QApplication.desktop().screenGeometry(pos)
        sh = self.sizeHint()
        ao = 18
        if pos.y() + ao > scr.bottom():
            self.move(pos.x()-sh.width(), pos.y()-sh.height()-ao)
        else:
            self.move(pos.x()-sh.width(), pos.y()+ao)

        if msecs > 0:
            self.timerId = self.startTimer(msecs)

        self.show()


def showBalloon(msg_icon, title, msg, tray_icon, pos, timeout, showArrow=True):
    global theBalloonTip
    hideBalloon()

    theBalloonTip = BalloonTip(msg_icon, msg, title, tray_icon)

    if timeout < 0:
        timeout = 5000

    theBalloonTip.balloon(pos, timeout, showArrow)


def hideBalloon():
    global theBalloonTip
    if theBalloonTip is None:
        return

    theBalloonTip.hide()
    del theBalloonTip
    theBalloonTip = None



class SystrayIcon(QLabel):
    """ On construction, you have to supply a QPixmap instance holding the
        application icon.  The pixmap should not be bigger than 32x32,
        preferably 22x22. Currently, no check is made.

        The class can emits two signals:
            Leftclick on icon: activated()
            Rightclick on icon: contextMenuRequested(const QPoint&)

        Based on code: (C) 2004 Torsten Marek
        License: Public domain
    """

    def __init__(self, icon, parent=None, name=""):
        QLabel.__init__(self, parent, name, Qt.WMouseNoMask | Qt.WRepaintNoErase |
                           Qt.WType_TopLevel | Qt.WStyle_Customize |
                           Qt.WStyle_NoBorder | Qt.WStyle_StaysOnTop)

        self.setMinimumSize(22, 22)
        self.setBackgroundMode(Qt.X11ParentRelative)
        self.setBackgroundOrigin(QWidget.WindowOrigin)

        self.libX11 = c.cdll.LoadLibrary(cu.find_library('X11'))

        # get all functions, set arguments + return types
        self.XternAtom = self.libX11.XInternAtom
        self.XternAtom.argtypes = [c.c_void_p, c.c_char_p, c.c_int]

        XSelectInput = self.libX11.XSelectInput
        XSelectInput.argtypes = [c.c_void_p, c.c_int, c.c_long]

        XUngrabServer = self.libX11.XUngrabServer
        XUngrabServer.argtypes = [c.c_void_p]

        XFlush = self.libX11.XFlush
        XFlush.argtypes = [c.c_void_p]

        class data(c.Union):
            _fields_ = [("b", c.c_char * 20),
                        ("s", c.c_short * 10),
                        ("l", c.c_long * 5)]

        class XClientMessageEvent(c.Structure):
            _fields_ = [("type", c.c_int),
                        ("serial", c.c_ulong),
                        ("send_event", c.c_int),
                        ("display", c.c_void_p),
                        ("window", c.c_int),
                        ("message_type", c.c_int),
                        ("format", c.c_int),
                        ("data", data)]

        XSendEvent = self.libX11.XSendEvent
        XSendEvent.argtypes = [c.c_void_p, c.c_int, c.c_int, c.c_long, c.c_void_p]

        XSync = self.libX11.XSync
        XSync.argtypes = [c.c_void_p, c.c_int]

        XChangeProperty = self.libX11.XChangeProperty
        XChangeProperty.argtypes = [c.c_void_p, c.c_long, c.c_int, c.c_int,
                                    c.c_int, c.c_int, c.c_char_p, c.c_int]

        dpy = int(qt_xdisplay())
        trayWin  = self.winId()

        x = 0
        while True:
            managerWin = self.locateTray(dpy)
            if managerWin: break
            x += 1
            if x > 30: break
            time.sleep(2.0)


        # Make sure KDE puts the icon in the system tray
        class data2(c.Union):
            _fields_ = [("i", c.c_int, 32),
                        ("s", c.c_char * 4)]

        k = data2()
        k.i = 1
        pk = c.cast(c.pointer(k), c.c_char_p)

        r = self.XternAtom(dpy, "KWM_DOCKWINDOW", 0)
        XChangeProperty(dpy, trayWin, r, r, 32, 0, pk, 1)

        r = self.XternAtom(dpy, "_KDE_NET_WM_SYSTEM_TRAY_WINDOW_FOR", 0)
        XChangeProperty(dpy, trayWin, r, 33, 32, 0, pk, 1)

        if managerWin != 0:
            # set StructureNotifyMask (1L << 17)
            XSelectInput(dpy, managerWin, 1L << 17)

        #XUngrabServer(dpy)
        XFlush(dpy)

        if managerWin != 0:
            # send "SYSTEM_TRAY_OPCODE_REQUEST_DOCK to managerWin
            k = data()
            k.l = (0, # CurrentTime
                   0, # REQUEST_DOCK
                   trayWin, # window ID
                   0, # empty
                   0) # empty
            ev = XClientMessageEvent(33, #type: ClientMessage
                                     0, # serial
                                     0, # send_event
                                     dpy, # display
                                     managerWin, # systray manager
                                     self.XternAtom(dpy, "_NET_SYSTEM_TRAY_OPCODE", 0), # message type
                                     32, # format
                                     k) # message data
            XSendEvent(dpy, managerWin, 0, 0, c.addressof(ev))
            XSync(dpy, 0)

        self.setPixmap(icon)
        self.setAlignment(Qt.AlignHCenter)

        if parent:
            QToolTip.add(self, parent.caption())



    def locateTray(self, dpy):
        # get systray window (holds _NET_SYSTEM_TRAY_S<screen> atom)
        self.XScreenNumberOfScreen = self.libX11.XScreenNumberOfScreen
        self.XScreenNumberOfScreen.argtypes = [c.c_void_p]

        XDefaultScreenOfDisplay = self.libX11.XDefaultScreenOfDisplay
        XDefaultScreenOfDisplay.argtypes = [c.c_void_p]
        XDefaultScreenOfDisplay.restype = c.c_void_p

        XGetSelectionOwner = self.libX11.XGetSelectionOwner
        XGetSelectionOwner.argtypes = [c.c_void_p, c.c_int]

        XGrabServer = self.libX11.XGrabServer
        XGrabServer.argtypes = [c.c_void_p]

        iscreen = self.XScreenNumberOfScreen(XDefaultScreenOfDisplay(dpy))
        selectionAtom = self.XternAtom(dpy, "_NET_SYSTEM_TRAY_S%i" % iscreen, 0)
        #XGrabServer(dpy)

        managerWin = XGetSelectionOwner(dpy, selectionAtom)
        return managerWin


    def setTooltipText(self, text):
        QToolTip.add(self, text)


    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.emit(PYSIGNAL("contextMenuRequested(const QPoint&)"), (e.globalPos(),))

        elif e.button() == Qt.LeftButton:
            self.emit(PYSIGNAL("activated()"), ())


    def supportsMessages(self):
        return True


    def showMessage(self, title, msg, icon, msecs):
        if have_pynotify and pynotify.init("hplip"):
            n = pynotify.Notification(title, msg, icon)
            n.set_timeout(msecs)
            s.show()
        else:
            g = self.mapToGlobal(QPoint(0, 0))
            showBalloon(icon, msg, title, self,
                QPoint(g.x() + self.width()/2, g.y() + self.height()/2), msecs)



class TitleItem(QCustomMenuItem):
    def __init__(self, icon, text):
        QCustomMenuItem.__init__(self)
        self.font = QFont()
        self.font.setBold(True)
        self.pen = QPen(Qt.black)
        self.bg_color = qApp.palette().color(QPalette.Active, QColorGroup.Background)
        self.icon = icon
        self.text = text

    def paint(self, painter, cg, act, enabled, x, y, w, h):
        painter.setPen(self.pen)
        painter.setFont(self.font)
        painter.setBackgroundColor(self.bg_color)
        painter.eraseRect(x, y, w, h)
        painter.drawPixmap(2, 2, self.icon, 0, 0, -1, -1)
        painter.drawText(x, y, w, h, Qt.AlignLeft | Qt.AlignVCenter | Qt.ShowPrefix | Qt.DontClip, self.text)

    def sizeHint(self):
        return QFontMetrics(self.font).size(Qt.AlignLeft | Qt.AlignVCenter | Qt.ShowPrefix | Qt.DontClip, self.text)



class SystemTrayApp(QApplication):
    def __init__(self, args, read_pipe):
        QApplication.__init__(self, args)

        self.read_pipe = read_pipe
        self.fmt = "80s80sI32sI80sf"
        self.fmt_size = struct.calcsize(self.fmt)
        
        self.user_settings = utils.UserSettings()
        self.user_settings.load()
        self.user_settings.debug()

        self.tray_icon = SystrayIcon(load_pixmap("hp_logo", "32x32", (22, 22)))
        self.menu = QPopupMenu()

        title_item = TitleItem(load_pixmap('hp_logo', '16x16', (16, 16)), "HP Status Service")
        i = self.menu.insertItem(title_item)
        self.menu.setItemEnabled(i, False)

        self.menu.insertSeparator()

        self.menu.insertItem(self.tr("HP Device Manager..."), self.toolbox_triggered)

        # TODO:
        #icon2 = QIconSet(load_pixmap('settings', '16x16'))
        #self.menu.insertItem(icon2, self.tr("Options..."), self.preferences_triggered)

        self.menu.insertSeparator()

        icon3 = QIconSet(load_pixmap('quit', '16x16'))
        self.menu.insertItem(icon3, self.tr("Quit"),  self.quit_triggered)

        self.tray_icon.show()

        notifier = QSocketNotifier(self.read_pipe, QSocketNotifier.Read)
        QObject.connect(notifier, SIGNAL("activated(int)"), self.notifier_activated)

        QObject.connect(self.tray_icon, PYSIGNAL("contextMenuRequested(const QPoint&)"), self.menu_requested)

        self.icon_info = load_pixmap('info', '16x16')
        self.icon_warn = load_pixmap('warning', '16x16')
        self.icon_error = load_pixmap('error', '16x16')
        
        if "--ignore-update-firsttime" not in args:
            self.handle_hplip_updation()
        self.timer = QTimer()
        self.timer.connect(self.timer,SIGNAL("timeout()"),self.handle_hplip_updation)
        self.timer.start(UPGRADE_CHECK_DELAY)

        # Cleans the /var/log/hp/tmp directory
        #self.handle_hplip_clean()
        
        #self.clean_timer = QTimer()
        #self.clean_timer.connect(self.clean_timer,SIGNAL("timeout()"),self.handle_hplip_clean)
        #self.clean_timer.start(CLEAN_EXEC_DELAY)


        self.ERROR_STATE_TO_ICON = {
            ERROR_STATE_CLEAR: self.icon_info,
            ERROR_STATE_OK: self.icon_info,
            ERROR_STATE_WARNING: self.icon_warn,
            ERROR_STATE_ERROR: self.icon_error,
            ERROR_STATE_LOW_SUPPLIES: self.icon_warn,
            ERROR_STATE_BUSY: self.icon_warn,
            ERROR_STATE_LOW_PAPER: self.icon_warn,
            ERROR_STATE_PRINTING: self.icon_info,
            ERROR_STATE_SCANNING: self.icon_info,
            ERROR_STATE_PHOTOCARD: self.icon_info,
            ERROR_STATE_FAXING: self.icon_info,
            ERROR_STATE_COPYING: self.icon_info,
        }


    def menu_requested(self, pos):
        self.menu.popup(pos)


    def quit_triggered(self):
        device.Event('', '', EVENT_SYSTEMTRAY_EXIT).send_via_dbus(SessionBus())
        self.quit()


    def toolbox_triggered(self):
        try:
            os.waitpid(-1, os.WNOHANG)
        except OSError:
            pass

        # See if it is already running...
        ok, lock_file = utils.lock_app('hp-toolbox', True)

        if ok: # able to lock, not running...
            utils.unlock(lock_file)

            path = utils.which('hp-toolbox')
            if path:
                path = os.path.join(path, 'hp-toolbox')
            else:
                log.error("Unable to find hp-toolbox on PATH.")

                self.tray_icon.showMessage("HPLIP Status Service",
                                self.__tr("Unable to locate hp-toolbox on system PATH."),
                                self.icon_error, 5000)

                return

            log.debug(path)
            os.spawnlp(os.P_NOWAIT, path, 'hp-toolbox')

        else: # ...already running, raise it
            device.Event('', '', EVENT_RAISE_DEVICE_MANAGER).send_via_dbus(SessionBus(), 'com.hplip.Toolbox')


    def preferences_triggered(self):
        #print "\nPARENT: prefs!"
        pass


    def notifier_activated(self, s):
        m = ''
        while True:
            ready = select.select([self.read_pipe], [], [], 1.0)

            if ready[0]:
                m = ''.join([m, os.read(self.read_pipe, self.fmt_size)])
                if len(m) == self.fmt_size:
                    event = device.Event(*struct.unpack(self.fmt, m))

                    if event.event_code > EVENT_MAX_USER_EVENT:
                        continue

                    desc = device.queryString(event.event_code)
                    #print "BUBBLE:", event.device_uri, event.event_code, event.username
                    error_state = STATUS_TO_ERROR_STATE_MAP.get(event.event_code, ERROR_STATE_CLEAR)
                    icon = self.ERROR_STATE_TO_ICON.get(error_state, self.icon_info)

                    if self.tray_icon.supportsMessages():
                        if event.job_id and event.title:
                            self.tray_icon.showMessage("HPLIP Device Status",
                                QString("%1\n%2\n%3\n(%4/%5/%6)").\
                                arg(event.device_uri).arg(event.event_code).\
                                arg(desc).arg(event.username).arg(event.job_id).arg(event.title),
                                icon, 5000)
                        else:
                            self.tray_icon.showMessage("HPLIP Device Status",
                                QString("%1\n%2\n%3").arg(event.device_uri).\
                                arg(event.event_code).arg(desc),
                                icon, 5000)

            else:
                break


    def handle_hplip_clean(self):
        log.debug("handle_hplip_clean ")
        home_dir = sys_conf.get('dirs', 'home')
        cmd = 'sh %s/hplip_clean.sh'%home_dir
        os.system(cmd)


    def handle_hplip_updation(self):
        log.debug("handle_hplip_updation upgrade_notify =%d"%(self.user_settings.upgrade_notify))
        path = utils.which('hp-upgrade')
        if self.user_settings.upgrade_notify is False:
            log.debug("upgrade notification is disabled in systray ")
            if path:
                path = os.path.join(path, 'hp-upgrade')
                log.debug("Running hp-upgrade: %s " % (path))
                # this just updates the available version in conf file. But won't notify
                os.spawnlp(os.P_NOWAIT, path, 'hp-upgrade', '--check')
                time.sleep(5)
                try:
                    os.waitpid(0, os.WNOHANG)
                except OSError:
                    pass
            return


        current_time = time.time()

        if int(current_time) > self.user_settings.upgrade_pending_update_time:
            path = utils.which('hp-upgrade')
            if path:
                path = os.path.join(path, 'hp-upgrade')
                log.debug("Running hp-upgrade: %s " % (path))
                os.spawnlp(os.P_NOWAIT, path, 'hp-upgrade', '--notify')
                time.sleep(5)
            else:
                log.error("Unable to find hp-upgrade --notify on PATH.")
        else:
            log.debug("upgrade schedule time is not yet completed. schedule time =%d current time =%d " %(self.user_settings.upgrade_pending_update_time, current_time))
        try:
            os.waitpid(0, os.WNOHANG)
        except OSError:
            pass



    def __tr(self,s,c = None):
        return qApp.translate("SystemTrayApp",s,c)




def run(read_pipe):
    log.set_module("hp-systray(qt3)")

    app = SystemTrayApp(sys.argv, read_pipe)

    notifier = QSocketNotifier(read_pipe, QSocketNotifier.Read)
    QObject.connect(notifier, SIGNAL("activated(int)"), app.notifier_activated)

    try:
        app.exec_loop()
    except KeyboardInterrupt:
        log.debug("Ctrl-C: Exiting...")
