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
HTTP_NO_CONTENT = 204
FILE_CONTENT = 'this is an example'.encode('utf8')

# init request session
s = requests.Session()
s.auth = (WEBDAV_USER, WEBDAV_PASS)
r = s.request(method='PUT', url=WEBDAV_URL_HOST + WEBDAV_URL_PATH + 'example.txt',
              data=FILE_CONTENT, verify=False)

# check result
if r.status_code == HTTP_CREATED:
    print('HTTP create the file')
elif r.status_code == HTTP_NO_CONTENT:
    print('HTTP update the file')
else:
    print('HTTP error (code %d)' % r.status_code)
