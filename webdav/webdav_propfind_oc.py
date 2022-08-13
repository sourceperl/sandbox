#!/usr/bin/env python3

import urllib3
from xml.dom import minidom
import requests
import dateutil.parser

# configure package (disable warning for self-signed certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# some consts
WEBDAV_URL_HOST = 'http://localhost:8080'
WEBDAV_URL_PATH = '/remote.php/webdav/'
WEBDAV_USER = 'admin'
WEBDAV_PASS = 'admin'
HTTP_MULTI_STATUS = 207
PROPFIND_REQUEST = '''<?xml version="1.0" encoding="utf-8" ?>
<d:propfind xmlns:d="DAV:">
<d:prop xmlns:oc="http://owncloud.org/ns">
  <d:getlastmodified/>
  <oc:checksums/>
  <oc:size/>
</d:prop>
</d:propfind>'''

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='PROPFIND', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH + 'Documents/',
              data=PROPFIND_REQUEST, headers={'Depth': '1'}, verify=False)

# check result
if r.status_code == HTTP_MULTI_STATUS:
    print('RAW XML: \n%s\n' % r.text)
    # parse XML
    dom = minidom.parseString(r.text.encode('ascii', 'xmlcharrefreplace'))
    # d:href in d:response
    for response in dom.getElementsByTagName('d:response'):
        href = response.getElementsByTagName('d:href')[0].firstChild.data
        # d:getlastmodified, oc:checksum and oc:size in d:response/d:propstat/d:prop
        prop_stat = response.getElementsByTagName('d:propstat')[0]
        prop = prop_stat.getElementsByTagName('d:prop')[0]
        get_last_modified = prop.getElementsByTagName('d:getlastmodified')[0].firstChild.data
        try:
            oc_checksums = prop.getElementsByTagName('oc:checksum')[0].firstChild.data
        except IndexError:
            oc_checksums = ''
        oc_size = prop.getElementsByTagName('oc:size')[0].firstChild.data
        # extract md5 hash
        md5_hash = 'n/a'
        for c_sum in oc_checksums.split(' '):
            if c_sum.startswith('MD5:'):
                try:
                    md5_hash = c_sum.split(':')[1]
                except IndexError:
                    pass
        # display result
        print('d:href = %s' % href)
        print('d:getlastmodified = %s' % dateutil.parser.parse(get_last_modified))
        print('md5 hash of file = %s' % md5_hash)
        print('oc:size = %s' % oc_size)
else:
    print('HTTP error (code %d)' % r.status_code)
