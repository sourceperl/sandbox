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
<d:prop>
  <d:getlastmodified/>
  <d:getcontentlength/>
</d:prop>
</d:propfind>'''

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='PROPFIND', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH + 'Documents',
              data=PROPFIND_REQUEST, headers={'Depth': '1'}, verify=False)

# check result
if r.status_code == HTTP_MULTI_STATUS:
    print('RAW XML: \n%s\n' % r.text)
    # parse XML
    dom = minidom.parseString(r.text.encode('ascii', 'xmlcharrefreplace'))
    # d:href in d:response
    for response in dom.getElementsByTagName('d:response'):
        href = response.getElementsByTagName('d:href')[0].firstChild.data
        # d:getlastmodified and oc:size in d:response/d:propstat/d:prop
        prop_stat = response.getElementsByTagName('d:propstat')[0]
        prop = prop_stat.getElementsByTagName('d:prop')[0]
        get_last_modified = prop.getElementsByTagName('d:getlastmodified')[0].firstChild.data
        try:
            content_length = int(prop.getElementsByTagName('d:getcontentlength')[0].firstChild.data)
        except IndexError:
            content_length = 0

        print('d:href = %s' % href)
        print('d:getlastmodified = %s' % dateutil.parser.parse(get_last_modified))
        print('d:getcontentlength = %i' % content_length)
else:
    print('HTTP error (code %d)' % r.status_code)
