# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2009 Hewlett-Packard Development Company, L.P.
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

# StdLib
import time
import cStringIO
from base.g import *
try:
   import xml.parsers.expat
except ImportError,e:
   log.info("\n")
   log.error("Failed to import xml.parsers.expat(%s).\nThis may be due to the incompatible version of python-xml package.\n"%(e))
   if "undefined symbol" in str(e):
       log.info(log.blue("Please re-install compatible version (other than 2.7.2-7.14.1) due to bug reported at 'https://bugzilla.novell.com/show_bug.cgi?id=766778'."))
       log.info(log.blue("\n        Run the following commands in root mode to change the python-xml package.(i.e Installing 2.7.2-7.1.2)"))
       log.info(log.blue("\n        Using zypper:\n        'zypper remove python-xml'\n        'zypper install python-xml-2.7.2-7.1.2'"))
       log.info(log.blue("\n        Using apt-get:\n        'apt-get remove python-xml'\n        'apt-get install python-xml-2.7.2-7.1.2'"))
       log.info(log.blue("\n        Using yum:\n        'yum remove python-xml'\n        'yum install python-xml-2.7.2-7.1.2'"))

   sys.exit(1)
   
# Local
from base.g import *
from base import device, utils

MAX_NETWORKS = 100
MAX_RETRIES = 20
NS = "http://www.hp.com/schemas/imaging/cnc/dcsl/2006/05/WifiConfig"
PREAMBLE = """<?xml version="1.0" encoding="utf-8"?>
<WiFiConfig xmlns="%s">
""" % NS

def _readWriteWifiConfig(dev, request):
    if not request:
        log.error("Invalid request")
        return 'executionfailed', {}

    log.debug("Sending request on wifi config channel...")
    log.log_data(request)
    #log.xml(request)

    bytes_written = dev.writeWifiConfig(request)
    log.debug("Wrote %d bytes." % bytes_written)

    data = cStringIO.StringIO()
    log.debug("Reading response on wifi config channel...")
    bytesread = dev.readWifiConfig(device.MAX_BUFFER, stream=data, timeout=30)
    i = 0
    # if response data is > 8192 bytes, make sure we have read it all...
    while True:
        i += 1
        bytesread = dev.readWifiConfig(device.MAX_BUFFER, stream=data, timeout=1)
        if not bytesread or i > MAX_RETRIES:
            break

    data = data.getvalue()

    #log.xml(repr(data))

    # Convert any char references
    data = utils.unescape(data)

    #log.xml(repr(data))
    data = unicode(data, 'utf-8')

    #log.xml(repr(data))

    # C4380 returns invalid XML for DeviceCapabilitiesResponse
    # Eliminate any invalid characters
    data = data.replace(u"Devicecapabilities", u"DeviceCapabilities").replace('\x00', '')

    log.log_data(data)
    log.debug("Read %d bytes." % len(data))

    if not data:
        log.error("No data")
        return 'executionfailed', {}

    #log.xml(data)

    try:
        params = utils.XMLToDictParser().parseXML(data)
    except xml.parsers.expat.ExpatError, e:
        log.error("XML parser failed: %s" % e)
        match = re.search(r"""line\s*(\d+).*?column\s*(\d+)""", str(e), re.I)
        if match is not None:
            log.error(data[int(match.group(2)):])
        return 'executionfailed', {}

    #log.pprint(params)

    errorreturn = 'executionfailed'
    for p in params:
        if p.lower().endswith('errorreturn'):
            errorreturn = params[p].lower()
            break

    params['errorreturn'] = errorreturn

    return errorreturn, params

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def getDeviceCapabilities(dev):
    ret = {}
    request = PREAMBLE + """<GetDeviceCapabilitiesRequest>
</GetDeviceCapabilitiesRequest>
</WiFiConfig>"""

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("GetDeviceCapabilities returned an error: %s" % errorreturn)
        return ret

    param_keys = ['wificonfig-getdevicecapabilitiesresponse-devicecapabilities-numberofsupportedwifiaccessories',
                  'wificonfig-getdevicecapabilitiesresponse-interfaceversion-minorreleasenumber',
                  'wificonfig-getdevicecapabilitiesresponse-interfaceversion-majorreleasenumber',
                 ]

    for p in param_keys:
        try:
            ret[p.split('-')[-1]] = params[p]
        except KeyError:
            log.debug("Missing response key: %s" % p)
            continue

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def getAdaptorList(dev):
    ret = {}
    request = PREAMBLE + """<GetAdaptorListRequest>
</GetAdaptorListRequest>
</WiFiConfig>"""

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {'adaptorlistlength': 0}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("GetAdaptorList returned an error: %s" % errorreturn)
        return ret

    try:
        adaptor_list_length = int(params['wificonfig-getadaptorlistresponse-adaptorlistlength'])
    except (ValueError, KeyError):
        adaptor_list_length = 0

    ret['adaptorlistlength'] = adaptor_list_length

    if adaptor_list_length == 0:
        log.error("GetAdaptorList returned 0 adaptors")

    elif adaptor_list_length == 1:
        try:
            ret['adaptorid-0'] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorid']
            ret['adaptorname-0'] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorname']
            ret['adaptorpresence-0'] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorpresence']
            ret['adaptorstate-0'] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorstate']
            ret['adaptortype-0'] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptortype']
        except KeyError, e:
            log.debug("Missing response key: %s" % e)
    else:
        for a in xrange(adaptor_list_length):
            try:
                ret['adaptorid-%d' % a] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorid-%d' % a]
                ret['adaptorname-%d' % a] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorname-%d' % a]
                ret['adaptorpresence-%d' % a] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorpresence-%d' % a]
                ret['adaptorstate-%d' % a] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptorstate-%d' % a]
                ret['adaptortype-%d' % a] = params['wificonfig-getadaptorlistresponse-adaptorlist-adaptorinfo-adaptortype-%d' % a]
            except KeyError, e:
                log.debug("Missing response key: %s" % e)

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def getWifiAdaptorID(dev):
    # rVal: [[adaptor_id, name, state, presence]]
    # ret: [adaptor_id, name, state, presence]
    rVal = []
    ret = getAdaptorList(dev)

    try:
        num_adaptors = ret['adaptorlistlength']
    except KeyError:
        num_adaptors = 0

    for n in xrange(num_adaptors):
        try:
            name = ret['adaptortype-%d' % n]
        except KeyError:
            name = ''

        if name.lower() in ('wifiembedded', 'wifiaccessory'):
            params = ['adaptorid', 'adaptorname', 'adaptorstate', 'adaptorpresence']

            r = []
            for p in params:
                try:
                    x = ret[''.join([p, '-', str(n)])]
                except KeyError:
                    if p == 'adaptorid':
                        x = -1
                    else:
                        x = 'Unknown'

                r.append(x)

            rVal.append(r)
            
    return rVal


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                         
def setAdaptorPower(dev, adapterList, power_state='PowerOn'):
    adaptor_id=-1
    adaptorName =""
    for a in adapterList:
        adaptor_id = a[0]
        adaptorName = a[1]
        request = PREAMBLE + """<SetAdaptorPowerRequest>
<AdaptorID>%s</AdaptorID>
<PowerState>%s</PowerState>
</SetAdaptorPowerRequest>
</WiFiConfig>""" % (adaptor_id, power_state.encode('utf-8'))

        errorreturn, params = _readWriteWifiConfig(dev, request)
        if not params:
            return -1 ,"","",""

        if errorreturn != 'ok':
            log.error("SetAdaptorPower returned an error: %s" % errorreturn)
        else:
            log.debug("SetAdaptorPower returned Success.")
            return adaptor_id, adaptorName, a[2], a[3]

    return -1 ,"","",""

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def performScan(dev, adapterName, ssid=None):
    ret, i, scan_state = {}, 0, "NewScan"

    while True:
        if ssid is None: # Undirected
            request = PREAMBLE + """<UndirectedScanRequest>
<ScanState>%s</ScanState>
</UndirectedScanRequest>
</WiFiConfig>""" % scan_state

            typ = 'UndirectedScan'
            rsp = 'undirectedscanresponse'

        else: # Directed
            request = PREAMBLE + """<DirectedScanRequest>
<SSID>%s</SSID>
<ScanState>%s</ScanState>
</DirectedScanRequest>
</WiFiConfig>""" % (ssid.encode('utf-8'), scan_state)

            typ = 'Directed'
            rsp = 'directedscanresponse'

        errorreturn, params = _readWriteWifiConfig(dev, request)
        if not params:
            return {'numberofscanentries': 0}

        ret['errorreturn'] = errorreturn
        if errorreturn != 'ok':
            log.error("%s returned an error: %s" % (typ, errorreturn))
            return ret

        try:
            number_of_scan_entries = int(params['wificonfig-%s-numberofscanentries' % rsp])
        except (ValueError, KeyError):
            number_of_scan_entries = 0

        ret['numberofscanentries'] = number_of_scan_entries

        if number_of_scan_entries == 0:
            if scan_state.lower() == 'scancomplete':
                log.debug("%s returned 0 entries. Scan complete." % typ)
            else:
                log.debug("%s returned 0 entries. Resuming scan..." % typ)

        elif number_of_scan_entries == 1:
            try:
                ssid = params['wificonfig-%s-scanlist-scanentry-ssid' % rsp]
                if not ssid:
                    ret['ssid-0'] = u'(unknown)'
                else:
                    ret['ssid-0'] = ssid
                ret['bssid-0'] = params['wificonfig-%s-scanlist-scanentry-bssid' % rsp]
                ret['channel-0'] = params['wificonfig-%s-scanlist-scanentry-channel' % rsp]
                ret['communicationmode-0'] = params['wificonfig-%s-scanlist-scanentry-communicationmode' % rsp]
                ret['dbm-0'] = params['wificonfig-%s-scanlist-scanentry-dbm' % rsp]
                ret['encryptiontype-0'] = params['wificonfig-%s-scanlist-scanentry-encryptiontype' % rsp]
                ret['rank-0'] = params['wificonfig-%s-scanlist-scanentry-rank' % rsp]
                ret['signalstrength-0'] = params['wificonfig-%s-scanlist-scanentry-signalstrength' % rsp]
            except KeyError, e:
                log.debug("Missing response key: %s" % e)

        else:
            for a in xrange(number_of_scan_entries):
                j = a+i
                try:
                    ssid = params['wificonfig-%s-scanlist-scanentry-ssid-%d' % (rsp, j)]
                    if not ssid:
                        ret['ssid-%d' % j] = u'(unknown)'
                    else:
                        ret['ssid-%d' % j] = ssid
                    ret['bssid-%d' % j] = params['wificonfig-%s-scanlist-scanentry-bssid-%d' % (rsp, j)]
                    ret['channel-%d' % j] = params['wificonfig-%s-scanlist-scanentry-channel-%d' % (rsp, j)]
                    ret['communicationmode-%d' % j] = params['wificonfig-%s-scanlist-scanentry-communicationmode-%d' % (rsp, j)]
                    ret['dbm-%d' % j] = params['wificonfig-%s-scanlist-scanentry-dbm-%d' % (rsp, j)]
                    ret['encryptiontype-%d' % j] = params['wificonfig-%s-scanlist-scanentry-encryptiontype-%d' % (rsp, j)]
                    ret['rank-%d' % j] = params['wificonfig-%s-scanlist-scanentry-rank-%d' % (rsp, j)]
                    ret['signalstrength-%d' % j] = params['wificonfig-%s-scanlist-scanentry-signalstrength-%d' % (rsp, j)]
                except KeyError, e:
                    log.debug("Missing response key: %s" % e)

        try:
            scan_state = ret['scanstate'] = params['wificonfig-%s-scanstate' % rsp] # MoreEntriesAvailable, ScanComplete
            ret['signalstrengthmax'] = params['wificonfig-%s-scansettings-signalstrengthmax' % rsp]
            ret['signalstrengthmin'] = params['wificonfig-%s-scansettings-signalstrengthmin' % rsp]
        except KeyError, e:
            log.debug("Missing response key: %s" % e)

        if scan_state.lower() == 'scancomplete':
            break

        scan_state = "ResumeScan"
        i += number_of_scan_entries

        if i > MAX_NETWORKS:
            break

        time.sleep(2)

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def associate(dev, adapterName,ssid, communication_mode, encryption_type, key):
    ret = {}
    request = PREAMBLE + """<AssociateRequest>
<SSID>%s</SSID>
<CommunicationMode>%s</CommunicationMode>
<EncryptionType>%s</EncryptionType>
<EncryptedParameters>%s</EncryptedParameters>
<Key>%s</Key>
</AssociateRequest>
</WiFiConfig>""" % (ssid.encode('utf-8'), communication_mode.encode('utf-8'),
                    encryption_type.encode('utf-8'), u"False".encode('utf-8'),
                    key.encode('utf-8'))

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("Associate returned an error: %s" % errorreturn)
        return ret

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def getVSACodes(dev,adapterName):
    ret = []
    request = PREAMBLE + """<GetVSACodesRequest>
</GetVSACodesRequest>
</WiFiConfig>"""

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return []

    if errorreturn != 'ok':
        log.error("GetVSACodes returned an error: %s" % errorreturn)
        return ret

    try:
        rule = params['wificonfig-getvsacodesresponse-vsacodelist-vsacode-rulenumber']
        severity = params['wificonfig-getvsacodesresponse-vsacodelist-vsacode-severity']
    except KeyError:
        n = 0
        while True:
            try:
                rule = params['wificonfig-getvsacodesresponse-vsacodelist-vsacode-rulenumber-%d' % n]
            except KeyError:
                break

            severity = params['wificonfig-getvsacodesresponse-vsacodelist-vsacode-severity-%d' % n]

            ret.append((rule, severity))
            n += 1
    else:
        ret.append((rule, severity))

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def __getIPConfiguration(dev, adaptor_id=0):
    ret = {}
    request = PREAMBLE + """<GetIPConfigurationRequest>
<AdaptorID>%d</AdaptorID>
</GetIPConfigurationRequest>
</WiFiConfig>""" % adaptor_id

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("GetIPConfiguration returned an error: %s" % errorreturn)
        return ret

    param_keys = ['wificonfig-getipconfigurationresponse-ipconfiguration-addressmode',
                  'wificonfig-getipconfigurationresponse-ipconfiguration-alternatednsaddress',
                  'wificonfig-getipconfigurationresponse-ipconfiguration-gatewayaddress',
                  'wificonfig-getipconfigurationresponse-ipconfiguration-ipaddress',
                  'wificonfig-getipconfigurationresponse-ipconfiguration-primarydnsaddress',
                  'wificonfig-getipconfigurationresponse-ipconfiguration-subnetmask',
                  'wificonfig-getipconfigurationresponse-networkconfiguration-hostname',
                  ]

    for p in param_keys:
        try:
            ret[p.split('-')[-1]] = params[p]
        except KeyError:
            log.debug("Missing response key: %s" % p)
            continue

    return ret


def getIPConfiguration(dev, adapterName, adaptor_id=0):
    ip, hostname, addressmode, subnetmask, gateway, pridns, sec_dns = \
        '0.0.0.0', 'Unknown', 'Unknown', '0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0'
    ret = __getIPConfiguration(dev, adaptor_id)

    if ret and ret['errorreturn'].lower() == 'ok':
        try:
            ip = ret['ipaddress']
            hostname = ret['hostname']
            addressmode = ret['addressmode']
            subnetmask = ret['subnetmask']
            gateway = ret['gatewayaddress']
            pridns = ret['primarydnsaddress']
            sec_dns = ret['alternatednsaddress']
        except KeyError, e:
            log.debug("Missing response key: %s" % str(e))

    return ip, hostname, addressmode, subnetmask, gateway, pridns, sec_dns

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def __getSignalStrength(dev, adaptor_id=0):
    ret = {}
    request = PREAMBLE + """<GetSignalStrengthRequest>
<AdaptorID>%d</AdaptorID>
</GetSignalStrengthRequest>
</WiFiConfig>""" % adaptor_id

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("GetSignalStrength returned an error: %s" % errorreturn)
        return ret

    param_keys = ['wificonfig-getsignalstrengthresponse-signalstrength-dbm',
                  'wificonfig-getsignalstrengthresponse-signalstrength-signalstrengthmax',
                  'wificonfig-getsignalstrengthresponse-signalstrength-signalstrengthmin',
                  'wificonfig-getsignalstrengthresponse-signalstrength-signalstrengthvalue',
                  ]

    for p in param_keys:
        try:
            ret[p.split('-')[-1]] = params[p]
        except KeyError:
            log.debug("Missing response key: %s" % p)
            continue

    return ret


def getSignalStrength(dev, adapterName, ssid, adaptor_id=0):
    ss_max, ss_min, ss_val, ss_dbm = 5, 0, 0, -200
    ret = __getSignalStrength(dev, adaptor_id)

    if ret and ret['errorreturn'].lower() == 'ok':
        try:
            ss_max = ret['signalstrengthmax']
            ss_min = ret['signalstrengthmin']
            ss_val = ret['signalstrengthvalue']
            ss_dbm = ret['dbm']
        except KeyError, e:
            log.debug("Missing response key: %s" % str(e))

    return ss_max, ss_min, ss_val, ss_dbm


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def __getCryptoSuite(dev):
    ret = {}
    request = PREAMBLE + """<GetCryptoSuiteRequest>
</GetCryptoSuiteRequest>
</WiFiConfig>"""

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return {}

    ret['errorreturn'] = errorreturn
    if errorreturn != 'ok':
        log.error("GetSignalStrength returned an error: %s" % errorreturn)
        return ret

    #log.pprint(params)

    param_keys = ['wificonfig-getcryptosuiteresponse-cryposuite-crypoalgorithm',
                  'wificonfig-getcryptosuiteresponse-cryposuite-crypomode',
                  'wificonfig-getcryptosuiteresponse-cryposuite-secretid',]

    for p in param_keys:
        try:
            ret[p.split('-')[-1]] = params[p]
        except KeyError:
            log.debug("Missing response key: %s" % p)
            continue

    return ret


def getCryptoSuite(dev, adapterName):
    alg, mode, secretid = '', '', ''
    ret = __getCryptoSuite(dev)

    if ret and ret['errorreturn'].lower() == 'ok':
        try:
            alg = ret['crypoalgorithm']
            mode = ret['crypomode']
            secretid = ret['secretid']
        except KeyError, e:
            log.debug("Missing response key: %s" % str(e))

    return  alg, mode, secretid

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def getHostname(dev):
    ret = ''
    request = PREAMBLE + """<GetHostnameRequest>
</GetHostnameRequest>
</WiFiConfig>"""

    errorreturn, params = _readWriteWifiConfig(dev, request)
    if not params:
        return ret

    if errorreturn != 'ok':
       # log.error("GetHostname returned an error: %s" % errorreturn)
        return ret

    try:
        ret = params['wificonfig-gethostnameresponse-hostname']
    except KeyError:
        log.debug("Missing response key: hostname")

    return ret

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def getLocation(bssid, ss):
    log.debug("Getting location for wifi AP: %s" % bssid)
    request = """<?xml version='1.0'?>
<LocationRQ xmlns='http://skyhookwireless.com/wps/2005' version='2.6' street-address-lookup='full'>
<authentication version='2.0'>
<simple>
<username>beta</username>
<realm>js.loki.com</realm>
</simple>
</authentication>
<access-point>
<mac>%s</mac>
<signal-strength>%d</signal-strength>
</access-point>
</LocationRQ>""" % (bssid.encode("utf-8"), ss)

    import httplib, socket
    ret = {}
    request_len = len(request)

    log.log_data(request)

    try:
        conn = httplib.HTTPSConnection("api.skyhookwireless.com")
        conn.putrequest("POST", "/wps2/location")
        conn.putheader("Content-type", "text/xml")
        conn.putheader("Content-Length", str(request_len))
        conn.endheaders()
        conn.send(request)
    except (socket.gaierror, socket.error):
        log.debug("Host connection error")
        return {}

    response = conn.getresponse()
    if response.status != 200:
        log.debug("Connection to location server failed")
        return {}

    xml = response.read()
    log.log_data(xml)

    try:
        params = utils.XMLToDictParser().parseXML(xml)
    except xml.parsers.expat.ExpatError:
        return {}

    if 'locationrs-error' in params:
        log.debug("Location server returned failure")
        return {}

    ret['latitude'] = params.get('locationrs-location-latitude', 0)
    ret['longitude'] = params.get('locationrs-location-longitude', 0)
    street_number = params.get('locationrs-location-street-address-street-number', '')
    street_name = params.get('locationrs-location-street-address-address-line', '')
    city = params.get('locationrs-location-street-address-city', '')
    country = params.get('locationrs-location-street-address-country-code', '')

    address = "%s %s, %s, %s" % (street_number, street_name, city, country)
    ret['address'] = address.strip()

    return ret

