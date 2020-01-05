#!/usr/bin/env python3
from xml.dom import minidom
import requests
import dateutil.parser

# some consts
HTTP_MULTI_STATUS = 207
PROPFIND_REQUEST = '''<?xml version="1.0" encoding="utf-8" ?>
<d:propfind xmlns:d="DAV:">
<d:prop xmlns:oc="http://owncloud.org/ns">
  <d:getlastmodified/>
  <oc:size/>
</d:prop>
</d:propfind>'''

# init request session
s = requests.Session()
s.auth = ('admin', 'admin')
r = s.request(method='PROPFIND', url='http://localhost:8080/remote.php/webdav/Documents',
              data=PROPFIND_REQUEST, headers={'Depth': '1'})

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
        oc_size = prop.getElementsByTagName('oc:size')[0].firstChild.data

        print('d:href = %s' % href)
        print('d:getlastmodified = %s' % dateutil.parser.parse(get_last_modified))
        print('oc:size = %s' % oc_size)
