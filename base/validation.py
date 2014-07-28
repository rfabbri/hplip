#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
#Global imports
import os

#Local imports
from base import utils
from base.g import *


# GPGP validation errors
DIGSIG_ERROR_NONE = 0
DIGSIG_ERROR_FILE_NOT_FOUND = 1
DIGSIG_ERROR_DIGITAL_SIGN_NOT_FOUND = 2
DIGSIG_ERROR_DIGITAL_SIGN_BAD = 3
DIGSIG_ERROR_UNABLE_TO_RECV_KEYS = 4
DIGSIG_ERROR_GPG_CMD_NOT_FOUND = 5
DIGSIG_ERROR_INCORRECT_PASSWORD = 6


DIGSIG_ERROR_GPG_CMD_NOT_FOUND_STR ="GPG Command Not Found"

class DigiSign_Verification(object):
    def __init__(self):
        pass

    def validate(self):
        pass


class GPG_Verification(DigiSign_Verification):
    def __init__(self, pgp_site = 'pgp.mit.edu', key = 0xA59047B9):
        self.__pgp_site = pgp_site
        self.__key = key
        self.__gpg = utils.which('gpg',True)
        if not self.__gpg:
            raise Exception(DIGSIG_ERROR_GPG_CMD_NOT_FOUND_STR)


    def __gpg_check(self, hplip_package, hplip_digsig, passwordObj):
        cmd = '%s --no-permission-warning --verify %s %s' % (self.__gpg, hplip_digsig, hplip_package)
        cmd = passwordObj.getAuthCmd()%cmd
        log.debug("Verifying file %s with digital keys: %s" % (hplip_package,cmd))

        status, output = utils.run(cmd, passwordObj)
        log.debug("%s status: %d  output:%s" % (self.__gpg, status,output))
        return status


    def acquire_gpg_key(self, passwordObj):
        cmd = '%s --no-permission-warning --keyserver %s --recv-keys 0x%X' \
              % (self.__gpg, self.__pgp_site, self.__key)

        cmd = passwordObj.getAuthCmd()%cmd
        log.info("Receiving digital keys: %s" % cmd)

        status, output = utils.run(cmd, passwordObj)
        log.debug(output)
        return status 


    def validate(self, hplip_package, hplip_digsig, passwordObj):
        if not os.path.exists(hplip_package):
            log.error("%s file doesn't exists." %(hplip_package))
            return DIGSIG_ERROR_FILE_NOT_FOUND

        if not os.path.exists(hplip_digsig):
            log.warn("%s file doesn't exists." %(hplip_digsig))
            return DIGSIG_ERROR_DIGITAL_SIGN_NOT_FOUND

        log.info(log.bold("\n\nNeed authentication to validate HPLIP package."))
        if not passwordObj.getPassword():
            return DIGSIG_ERROR_INCORRECT_PASSWORD

        status = self.acquire_gpg_key(passwordObj)
        if status != 0:
            return DIGSIG_ERROR_UNABLE_TO_RECV_KEYS

        status = self.__gpg_check(hplip_package, hplip_digsig, passwordObj)
        if status != 0:
            return DIGSIG_ERROR_DIGITAL_SIGN_BAD
        else:
            return DIGSIG_ERROR_NONE

