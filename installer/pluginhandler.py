# -*- coding: utf-8 -*-
#
# (c) Copyright @ 20013 Hewlett-Packard Development Company, L.P.
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

import os
import cStringIO
import time
import string
import shutil
import urllib # TODO: Replace with urllib2 (urllib is deprecated in Python 3.0)

from base import utils, tui, os_utils
from base.g import *
from installer import core_install
from base import pexpect

try:
    import hashlib # new in 2.5

    def get_checksum(s):
        return hashlib.sha1(s).hexdigest()

except ImportError:
    import sha # deprecated in 2.6/3.0

    def get_checksum(s):
        return sha.new(s).hexdigest()


PLUGIN_STATE_FILE = '/var/lib/hp/hplip.state'
PLUGIN_FALLBACK_LOCATION = 'http://hplipopensource.com/hplip-web/plugin/'


# Plug-in download errors
PLUGIN_INSTALL_ERROR_NONE = 0
PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND = 1
PLUGIN_INSTALL_ERROR_DIGITAL_SIGN_NOT_FOUND = 2
PLUGIN_INSTALL_ERROR_DIGITAL_SIGN_BAD = 3
PLUGIN_INSTALL_ERROR_PLUGIN_FILE_CHECKSUM_ERROR = 4
PLUGIN_INSTALL_ERROR_NO_NETWORK = 5
PLUGIN_INSTALL_ERROR_DIRECTORY_ERROR = 6
PLUGIN_INSTALL_ERROR_UNABLE_TO_RECV_KEYS = 7


class PluginHandle(object):
    def __init__(self, pluginPath = prop.user_dir):
        self.__plugin_path = pluginPath
        self.__required_version = ""
        self.__plugin_name = ""
        self.__plugin_state = PLUGIN_NOT_INSTALLED
        self.__installed_version = ''
        self.__plugin_conf_file = ""

        self.__setPluginConfFile()
        self.__setPluginVersion()
        self.__readPluginStatus()

#################### Private functions ########################
    def __getPluginFilesList(self, src_dir):
        if not os.path.exists(src_dir+"/plugin.spec"):
            log.warn("%s/plugin.spec file doesn't exists."%src_dir)
            return []

        cwd = os.getcwd()
        os.chdir(src_dir)
        
        plugin_spec = ConfigBase("plugin.spec")
        products = plugin_spec.keys("products")

        BITNESS = utils.getBitness()
        ENDIAN = utils.getEndian()
        PPDDIR = sys_conf.get('dirs', 'ppd')
        DRVDIR = sys_conf.get('dirs', 'drv')
        HOMEDIR = sys_conf.get('dirs', 'home')
        DOCDIR = sys_conf.get('dirs', 'doc')
        CUPSBACKENDDIR = sys_conf.get('dirs', 'cupsbackend')
        CUPSFILTERDIR = sys_conf.get('dirs', 'cupsfilter')
        RULESDIR = '/etc/udev/rules.d'
        BIN = sys_conf.get('dirs', 'bin')

        # Copying plugin.spec file to home dir.
        if src_dir != HOMEDIR:
            shutil.copyfile(src_dir+"/plugin.spec", HOMEDIR+"/plugin.spec")
            os.chmod(HOMEDIR+"/plugin.spec",0644)

        processor = utils.getProcessor()
        if processor == 'power_machintosh':
            ARCH = 'ppc'
        else:
            ARCH = 'x86_%d' % BITNESS

        if BITNESS == 64:
            SANELIBDIR = '/usr/lib64/sane'
            LIBDIR = '/usr/lib64'
        else:
            SANELIBDIR = '/usr/lib/sane'
            LIBDIR = '/usr/lib'

        copies = []

        for PRODUCT in products:
            MODEL = PRODUCT.replace('hp-', '').replace('hp_', '')
            for s in plugin_spec.get("products", PRODUCT).split(','):

                if not plugin_spec.has_section(s):
                    log.error("Missing section [%s]" % s)
                    os.chdir(cwd)
                    return []

                src = plugin_spec.get(s, 'src', '')
                trg = plugin_spec.get(s, 'trg', '')
                link = plugin_spec.get(s, 'link', '')

                if not src:
                    log.error("Missing 'src=' value in section [%s]" % s)
                    os.chdir(cwd)
                    return []

                if not trg:
                    log.error("Missing 'trg=' value in section [%s]" % s)
                    os.chdir(cwd)
                    return []

                src = os.path.basename(utils.cat(src))
                trg = utils.cat(trg)

                if link:
                    link = utils.cat(link)

                copies.append((src, trg, link))

        copies = utils.uniqueList(copies)
        copies.sort()
        os.chdir(cwd)
        return copies


    def __setPluginVersion(self):
        self.__required_version = prop.installed_version
        self.__plugin_name = 'hplip-%s-plugin.run' % self.__required_version


    def __readPluginStatus(self):
        plugin_state_conf = ConfigBase( PLUGIN_STATE_FILE)
        self.__plugin_state = plugin_state_conf.get('plugin', 'installed', PLUGIN_NOT_INSTALLED)
        if self.__plugin_state == PLUGIN_NOT_INSTALLED:
            self.__installed_version = ''
        else:
            self.__installed_version = plugin_state_conf.get('plugin','version', '')
            hplip_version = sys_conf.get('hplip', 'version', '0.0.0')
            if self.__installed_version != hplip_version:
                self.__plugin_state = PLUGIN_VERSION_MISMATCH
            else:
                home = sys_conf.get('dirs', 'home')
                copies = self.__getPluginFilesList( home )

                for src, trg, link in copies:
                    if link != "":
                        if utils.check_library(link) == False:
                            self.__plugin_state = PLUGIN_FILES_CORRUPTED


    def __getPluginInformation(self, callback=None):
        status, url, check_sum = PLUGIN_INSTALL_ERROR_NO_NETWORK, '',''

        if self.__plugin_conf_file.startswith('http://'):
            if not utils.check_network_connection():
                log.error("Network connection not detected.")
                return PLUGIN_INSTALL_ERROR_NO_NETWORK, '',0

        local_conf_fp, local_conf = utils.make_temp_file()

        try:
            try:
                if self.__plugin_conf_file.startswith('file://'):
                    filename, headers = urllib.urlretrieve(self.__plugin_conf_file, local_conf, callback)

                else:
                    wget = utils.which("wget", True)
                    if wget:
                        status, output = utils.run("%s --timeout=60 --output-document=%s %s --cache=off" %(wget, local_conf, self.__plugin_conf_file))
                        if status:
                            log.error("Plugin download failed with error code = %d" %status)
                            return status, url, check_sum
                    else:
                        log.error("Please install wget package to download the plugin.")
                        return status, url, check_sum
            except IOError, e:
                log.error("I/O Error: %s" % e.strerror)
                return status, url, check_sum

            if not os.path.exists(local_conf):
                log.error("plugin.conf not found.")
                return status, url, check_sum

            try:
                plugin_conf_p = ConfigBase(local_conf)
                url = plugin_conf_p.get(self.__required_version, 'url','')
                check_sum  = plugin_conf_p.get(self.__required_version, 'checksum')
                status = PLUGIN_INSTALL_ERROR_NONE
            except (KeyError, ConfigParser.NoSectionError):
                log.error("Error reading plugin.conf: Missing section [%s]" % self.__required_version)
                return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND, url, check_sum

            if url == '':
                return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND, url, check_sum

        finally:
            os.close(local_conf_fp)
            os.remove(local_conf)

        return status, url, check_sum


    def __validatePlugin(self,plugin_file, digsig_file, req_checksum):
        calc_checksum = get_checksum(file(plugin_file, 'r').read())
        log.debug("D/L file checksum=%s" % calc_checksum)

        if req_checksum and req_checksum != calc_checksum:
            return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_CHECKSUM_ERROR

        gpg = utils.which('gpg',True)
        if gpg:
            cmd = '%s --no-permission-warning --keyserver pgp.mit.edu --recv-keys 0xA59047B9' % gpg
            log.info("Receiving digital keys: %s" % cmd)
            status, output = utils.run(cmd)
            log.debug(output)

            if status != 0:
                return PLUGIN_INSTALL_ERROR_UNABLE_TO_RECV_KEYS

            cmd = '%s --no-permission-warning --verify %s %s' % (gpg, digsig_file, plugin_file)
            log.debug("Verifying plugin with digital keys: %s" % cmd)
            status, output = utils.run(cmd)
            log.debug(output)
            log.debug("%s status: %d" % (gpg, status))

            if status != 0:
                return PLUGIN_INSTALL_ERROR_DIGITAL_SIGN_BAD

        return PLUGIN_INSTALL_ERROR_NONE


    def __setPluginConfFile(self):
        home = sys_conf.get('dirs', 'home')

        if os.path.exists('/etc/hp/plugin.conf'):
            self.__plugin_conf_file = "file:///etc/hp/plugin.conf"

        elif os.path.exists(os.path.join(home, 'plugin.conf')):
            self.__plugin_conf_file = "file://" + os.path.join(home, 'plugin.conf')

        else:
            self.__plugin_conf_file = "http://hplip.sf.net/plugin.conf"


#################### Public functions ########################


    def download(self, pluginPath='',callback = None):
        core = core_install.CoreInstall()

        if pluginPath:#     and os.path.exists(pluginPath):
            src = pluginPath
            checksum = ""       # TBD: Local copy may have different checksum. So ignoring checksum
        else:
            sts, url, checksum = self.__getPluginInformation(callback)
            src = url
            if sts != PLUGIN_INSTALL_ERROR_NONE:
                return sts, ""

        log.debug("Downloading %s plug-in file from '%s' to '%s'..." % (self.__required_version, src, self.__plugin_path))
        plugin_file = os.path.join(self.__plugin_path, self.__plugin_name)
        try:
            os.umask(0)
            if not os.path.exists(self.__plugin_path):
                os.makedirs(self.__plugin_path, 0755)
            if os.path.exists(plugin_file):
                os.remove(plugin_file)
            if os.path.exists(plugin_file+'.asc'):
                os.remove(plugin_file+'.asc')

        except (OSError, IOError), e:
            log.error("Failed in OS operations:%s "%e.strerror)
            return PLUGIN_INSTALL_ERROR_DIRECTORY_ERROR, ""

        try:
            if src.startswith('file://'):
                filename, headers = urllib.urlretrieve(src, plugin_file, callback)
            else:
                wget = utils.which("wget", True)
                if wget:
                    cmd = "%s --cache=off -P %s %s" % (wget,self.__plugin_path,src)
                    log.debug(cmd)
                    status, output = utils.run(cmd)
                    log.debug("wget returned: %d" % status)

                #Check whether plugin is accessible in Openprinting.org website otherwise dowload plugin from alternate location.
                if status != 0 or os_utils.getFileSize(plugin_file) <= 0:
                    src = os.path.join(PLUGIN_FALLBACK_LOCATION, self.__plugin_name)
                    log.info("Plugin is not accessible. Trying to download it from fallback location: [%s]" % src)
                    cmd = "%s --cache=off -P %s %s" % (wget,self.__plugin_path,src)
                    log.debug(cmd)
                    status, output = utils.run(cmd)

                if status != 0 or os_utils.getFileSize(plugin_file) <= 0:
                    log.error("Plug-in download is failed from both URL and fallback location.")
                    return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND, ""

        except IOError, e:
            log.error("Plug-in download failed: %s" % e.strerror)
            return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND, ""

        if core.isErrorPage(file(plugin_file, 'r').read(1024)):
            log.debug(file(plugin_file, 'r').read(1024))
            os.remove(plugin_file)
            return PLUGIN_INSTALL_ERROR_PLUGIN_FILE_NOT_FOUND, ""

        # Try to download and check the GPG digital signature
        digsig_url = src + '.asc'
        digsig_file = plugin_file + '.asc'

        log.debug("Downloading %s plug-in digital signature file from '%s' to '%s'..." % (self.__required_version, digsig_url, digsig_file))

        try:
            if digsig_url.startswith('file://'):
                filename, headers = urllib.urlretrieve(digsig_url, digsig_file, callback)
            else:
                cmd = "%s --cache=off -P %s %s" % (wget,self.__plugin_path,digsig_url)
                log.debug(cmd)
                status, output = utils.run(cmd)
        except IOError, e:
            log.error("Plug-in GPG file [%s] download failed: %s" % (digsig_url,e.strerror))
            return PLUGIN_INSTALL_ERROR_DIGITAL_SIGN_NOT_FOUND, plugin_file

        if core.isErrorPage(file(digsig_file, 'r').read(1024)):
            log.debug(file(digsig_file, 'r').read())
            os.remove(digsig_file)
            return PLUGIN_INSTALL_ERROR_DIGITAL_SIGN_NOT_FOUND, plugin_file

        sts = self.__validatePlugin(plugin_file, digsig_file, checksum)
        return sts, plugin_file


    def run_plugin(self, plugin_file, mode=GUI_MODE):
        result = False
        log.debug("run_plugin plugin_file =%s mode=%d"%(plugin_file, mode))

        cwd = os.getcwd()
        os.chdir(self.__plugin_path)

        if mode == GUI_MODE:
            cmd = "sh %s --keep --nox11 -- -u" % plugin_file
        else:
            cmd = "sh %s --keep --nox11 -- -i" % plugin_file

        if os_utils.execute(cmd) == 0:
            result = True
        else:
            log.error("Python gobject/dbus may be not installed")
            result = False

        try:
            shutil.rmtree('./plugin_tmp')
        except OSError:
            log.warn("Failed to remove the temporary files")

        os.chdir(cwd)
        return result


    def copyFiles(self, src_dir):

        copies = self.__getPluginFilesList(src_dir)
        os.umask(0)

        for src, trg, link in copies:

            if not os.path.exists(src):
                log.debug("Source file %s does not exist. Skipping." % src)
                continue

            if os.path.exists(trg):
                log.debug("Target file %s already exists. Replacing." % trg)
                os.remove(trg)

            trg_dir = os.path.dirname(trg)

            if not os.path.exists(trg_dir):
                log.debug("Target directory %s does not exist. Creating." % trg_dir)
                os.makedirs(trg_dir, 0755)

            if not os.path.isdir(trg_dir):
                log.error("Target directory %s exists but is not a directory. Skipping." % trg_dir)
                continue

            try:
                shutil.copyfile(src, trg)
            except (IOError, OSError), e:
                log.error("File copy failed: %s" % e.strerror)
                continue

            else:
                if not os.path.exists(trg):
                    log.error("Target file %s does not exist. File copy failed." % trg)
                    continue
                else:
                    os.chmod(trg, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

                if link:
                    if os.path.exists(link):
                        log.debug("Symlink already exists. Replacing.")
                        os.remove(link)

                    log.debug("Creating symlink %s (link) to file %s (target)..." %(link, trg))

                    try:
                        os.symlink(trg, link)
                    except (OSError, IOError), e:
                        log.debug("Unable to create symlink: %s" % e.strerror)
                        pass

        log.debug("Updating hplip.state - installed = 1")
        plugin_state_conf = ConfigBase( PLUGIN_STATE_FILE)
        plugin_state_conf.set('plugin', "installed", '1')
        log.debug("Updating hplip.state - eula = 1")
        plugin_state_conf.set('plugin', "eula", '1')
        hplip_version = sys_conf.get('hplip', 'version', '0.0.0')
        log.debug("Updating hplip.state - version = %s"%hplip_version)
        plugin_state_conf.set('plugin','version', hplip_version)

        self.__plugin_state = PLUGIN_INSTALLED
        self.__installed_version = hplip_version

        return True


    def uninstall(self):
        home = sys_conf.get('dirs', 'home')
        files = self.__getPluginFilesList(home)

        if size(files) == 0:
            log.debug("Fail to get Plugin files list")
            return False

        for src, trg, link in files:
            log.debug("Deleting %s,%s files."%(trg,link))
            if trg != "":
                os.unlink(trg)
            if link != "":
                os.unlink(link)

        return True


    def getInstalledVersion(self):
        return self.__installed_version


    def getStatus(self):
        self.__readPluginStatus()
        log.debug("Plugin status = %s"%self.__plugin_state)
        return self.__plugin_state


    def getFileName(self):
        return self.__plugin_name


    def deleteInstallationFiles(self, plugin_file):
        digsig_file = plugin_file + ".asc"

        if os.path.exists(plugin_file):
            os.unlink(plugin_file)
        if os.path.exists(digsig_file):
            os.unlink(digsig_file)
