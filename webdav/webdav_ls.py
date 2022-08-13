#!/usr/bin/env python3

from xml.dom import minidom
import urllib3
import urllib.parse
import requests

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
  <oc:size/>
</d:prop>
</d:propfind>'''

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='PROPFIND', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH, data=PROPFIND_REQUEST,
              headers={'Depth': '1'}, verify=False)

# check result
if r.status_code == HTTP_MULTI_STATUS:
    # parse XML
    dom = minidom.parseString(r.text.encode('ascii', 'xmlcharrefreplace'))
    # d:href in d:response
    for response in dom.getElementsByTagName('d:response'):
        href = response.getElementsByTagName('d:href')[0].firstChild.data
        # oc:size in d:response/d:propstat/d:prop
        prop_stat = response.getElementsByTagName('d:propstat')[0]
        prop = prop_stat.getElementsByTagName('d:prop')[0]
        oc_size = prop.getElementsByTagName('oc:size')[0].firstChild.data
        # extract filename and file size
        file_name = urllib.parse.unquote(href[len(WEBDAV_URL_PATH):])
        if not file_name:
            file_name = '.'
        file_size = int(oc_size)
        # print result
        print('%10i  %s' % (file_size, file_name))
else:
    print('HTTP error (code %d)' % r.status_code)
