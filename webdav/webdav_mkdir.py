#!/usr/bin/env python3

import urllib3
import requests

# configure package (disable warning for self-signed certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# some consts
WEBDAV_URL_HOST = 'http://localhost:8080'
WEBDAV_URL_PATH = '/remote.php/webdav/'
WEBDAV_USER = 'admin'
WEBDAV_PASS = 'admin'
HTTP_CREATED = 201

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='MKCOL', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH + 'Example_dir', verify=False)

# check result
if r.status_code == HTTP_CREATED:
    print('HTTP create OK')
else:
    print('HTTP error (code %d)' % r.status_code)
