#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright @2013 Hewlett-Packard Development Company, L.P.
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
# Author: Amarnath Chitumalla
#


# Std Lib
import sys
import os.path
import re
import os

# Local
from base.g import *
from base import utils, tui


##### Global variables ###
HPLIP_INFO_SITE ="http://hplip.sourceforge.net/hplip_web.conf"


SIH_DISABLED_SUCCESSFULLY = 0
SIH_NO_SI_DEVICES = 1
SIH_FAILED_TO_DISABLE = 2
SIH_FAILED_TO_DOWNLOAD = 3
SIH_FAILED_TO_VERIFY_DIG_SIGN = 4
SIH_FAILED_TO_IMPORT_UI = 5
SIH_VERIFIED_DIG_SIGN = 6


########### methods ###########


def get_usb_details(vid_pid):
    result_cnt = 0
    param_result = {"idVendor":'', "iProduct":'',  "bNumInterfaces":'', "bInterfaceClass":''}
    param_search = {"idVendor": re.compile(r"""\s*idVendor\s*([0-9a-fx]{1,})\s*.*""", re.I),
                    "iProduct" : re.compile(r"""\s*iProduct\s*[0-9a-fx]{1,}\s*(.*)""", re.I),
                    "bNumInterfaces" : re.compile(r"""\s*bNumInterfaces\s*(\d{1,})\s*.*""", re.I),
                    "bInterfaceClass" : re.compile(r"""\s*bInterfaceClass\s*(\d{1,})\s*.*""", re.I)  }

    lsusb_cmd = utils.which('lsusb',True)
    if lsusb_cmd:
        sts,out = utils.run("%s -d %s -v"%(lsusb_cmd, vid_pid), passwordObj = None, pswd_msg='', log_output=False)
        if sts == 0:
            for l in out.splitlines():
                for s in param_search:
                    if s in l:
                        result_cnt += 1
                        if param_search[s].match(l):
                            param_result[s] = param_search[s].match(l).group(1)
                        else:
                            log.warn("TBD... Shouldn't have entered into this condition. key[%s]"%s)

                        if "idVendor" ==  s and param_result[s].lower() != "0x03f0":  # if non-HP vendor, ignoring usb parsing.
                            return False, {}
                        elif "iProduct" == s and param_result[s] == "":
                            return False, {}

                        break

                if result_cnt == len(param_result):  # To avoid extra parsing...
                     break

    return True, param_result


# get_smartinstall_enabled_devices function checks CD-ROM enabled devices.
#Input:
#       None
# Output:
#       smartinstall_dev_list (list) --> Returns CD-ROM enabled device list.
#
def get_smartinstall_enabled_devices():
    smartinstall_dev_list=[]
    lsusb_cmd = utils.which('lsusb',True)

    if not lsusb_cmd:
        log.error("Failed to find the lsusb command")
        return smartinstall_dev_list

    try:
        sts,out = utils.run(lsusb_cmd)
        if sts !=  0:
            log.error("Failed to run the %s command"%lsusb_cmd)
            return smartinstall_dev_list

        for d in out.splitlines():
            usb_dev_pat = re.compile(r""".*([0-9a-f]{4}:([0-9a-f]{4}))\s*""", re.I)

            if usb_dev_pat.match(d):
                vid_pid = usb_dev_pat.match(d).group(1)

                bsts, usb_params = get_usb_details(vid_pid)
                if not bsts:
                    continue    # These are not HP-devices

                log.debug("Product['%s'],Interfaces[%s],InterfaceClass[%s]"%(usb_params["iProduct"], usb_params["bNumInterfaces"],usb_params["bInterfaceClass"]))
                if usb_params["bNumInterfaces"] == '1' and usb_params["bInterfaceClass"] == '8' and "laserjet" in usb_params["iProduct"].lower():    #'8' is MASS STORAGE
                    smartinstall_dev_list.append(usb_params["iProduct"])

            else:
                log.warn("Failed to find vid and pid for USB device[%s]"%d)

    except KeyError:
        pass

    if smartinstall_dev_list:
        smartinstall_dev_list = utils.uniqueList(smartinstall_dev_list)

    return smartinstall_dev_list


def check_SmartInstall():
    devices = get_smartinstall_enabled_devices()
    if devices:
        return True
    else:
        return False


def get_SmartInstall_tool_info():
    url, file_name = "", ""
    if not utils.check_network_connection():
        log.error("Internet connection not found.")
    else:
        sts, HPLIP_file = utils.download_from_network(HPLIP_INFO_SITE)
        if sts is True:
            hplip_si_conf = ConfigBase(HPLIP_file)
            url = hplip_si_conf.get("SMART_INSTALL","reference","")
            if url:
                file_name = 'SmartInstallDisable-Tool.run'
            else:
                log.error("Failed to download %s."%HPLIP_INFO_SITE)
        else:
            log.error("Failed to download %s."%HPLIP_INFO_SITE)

    return url, file_name



def download(mode, passwordObj):
    if not utils.check_network_connection():
        log.error("Internet connection not found.")
        return SIH_FAILED_TO_DOWNLOAD, "" , ""

    else:
        sts, HPLIP_file = utils.download_from_network(HPLIP_INFO_SITE)
        if sts is True:
            hplip_si_conf = ConfigBase(HPLIP_file)
            source = hplip_si_conf.get("SMART_INSTALL","url","")
            if not source:
                log.error("Failed to download %s."%HPLIP_INFO_SITE)
                return SIH_FAILED_TO_DOWNLOAD, "" , ""

        sts, smart_install_run = utils.download_from_network(source)
        if not sts:
            log.error("Failed to download %s."%source)
            return SIH_FAILED_TO_DOWNLOAD, "" , ""

        sts, smart_install_asc = utils.download_from_network(source+'.asc')
        if not sts:
            log.error("Failed to download %s."%(source+'.asc'))
            return SIH_FAILED_TO_VERIFY_DIG_SIGN, smart_install_run , ""

        if passwordObj == None:
            try:
                from base.password import Password
            except ImportError:
                return SIH_FAILED_TO_VERIFY_DIG_SIGN, smart_install_run , ""
            passwordObj = Password(mode)

        if utils.ERROR_NONE == utils.validateDownloadFile(smart_install_run, smart_install_asc,"",passwordObj):
            return SIH_VERIFIED_DIG_SIGN, smart_install_run, smart_install_asc
        else:
            log.error("GPG verification failed for %s ."%source)
            return SIH_FAILED_TO_VERIFY_DIG_SIGN, smart_install_run, smart_install_asc


def disable(mode, ui_toolkit='qt4', dialog=None, app=None, passwordObj = None):

    dev_list = get_smartinstall_enabled_devices()
    if not dev_list:
        log.debug("No Smart Install Device found")
        return SIH_NO_SI_DEVICES

    return_val = SIH_FAILED_TO_DISABLE
    url, file_name = get_SmartInstall_tool_info()
    printer_names  = utils.list_to_string(dev_list)

    try:
        if mode == GUI_MODE:
            if ui_toolkit == 'qt3':
                try:
                    from ui.setupform import FailureMessageUI
                except ImportError:
                    log.error("Smart Install is enabled in %s device(s).\nAuto Smart Install disable is not supported in QT3.\nPlease refer link \'%s\' to disable manually"%(printer_names,url))
                else:
                    FailureMessageUI("Smart Install is enabled in %s device(s).\n\nAuto Smart Install disable is not supported in QT3.\nPlease refer link \'%s\' to disable manually"%(printer_names,url))

            else: #qt4
                if not utils.canEnterGUIMode4():
                    log.error("%s requires GUI support . Is Qt4 installed?" % __mod__)
                    return SIH_FAILED_TO_DISABLE

                if dialog and app:  # If QT app already opened, re-using same object
                    dialog.init(printer_names, "", QUEUES_SMART_INSTALL_ENABLED)
                else:   # If QT object is not created, creating QT app
                    try:
                        from ui4.queuesconf import QueuesDiagnose
                    except ImportError:
                        log.error("Unable to load Qt4 support. Is it installed?")
                    else:       #  app = QApplication(sys.argv)   # caller needs to inoke this, if already QApplication object is not created.
                        dialog = QueuesDiagnose(None, printer_names ,"",QUEUES_SMART_INSTALL_ENABLED)

                log.debug("Starting GUI loop...")
                dialog.exec_()

                if check_SmartInstall():
                    dialog.showMessage("Failed to disable smart install.\nPlease refer link \'%s\' for more information" %url)
                else:
                    dialog.showSuccessMessage("Smart install disabled successfully.")


        #Interaction mode
        else: 
            log.error("Smart Install is enabled in %s device(s). "%printer_names)
            response, value = tui.enter_choice("Do you want to download and disable smart install?(y=yes*, n=no):",['y', 'n'], 'y')

            if not response or value != 'y':   #User exit
                return_val = SIH_FAILED_TO_DISABLE

            else:
                sts, smart_install_run, smart_install_asc = download(mode, passwordObj)
                if sts == SIH_FAILED_TO_VERIFY_DIG_SIGN:
                    response, value = tui.enter_yes_no("Digital Sign verification failed, Do you want to continue?")
                    if not response or not value:
                        return_val = SIH_FAILED_TO_VERIFY_DIG_SIGN
                    else:   # Continue without validation succes.
                        sts = SIH_VERIFIED_DIG_SIGN

                if sts == SIH_VERIFIED_DIG_SIGN:
                    sts, out = utils.run("sh %s"%smart_install_run)

                    # Once smart install disabler installation completed, cross verifying to ensure no smart install devices found
                    if sts or check_SmartInstall():
                        log.error("Failed to disable smart install.")
                        log.error("Please refer link \'%s\' to disable manually"%url)
                    else:
                        log.info("Smart install disabled successfully.")
                        return_val = SIH_DISABLED_SUCCESSFULLY
                else:
                    return_val = sts

    except KeyboardInterrupt:
        log.error("User exit")
        sys.exit(0)

    return return_val

