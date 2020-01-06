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
HTTP_NO_CONTENT = 204

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='DELETE', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH + 'example.txt', verify=False)

# check result
if r.status_code == HTTP_NO_CONTENT:
    print('HTTP delete the file')
else:
    print('HTTP error (code %d)' % r.status_code)
