#!/usr/bin/env python3
import requests

# some consts
HTTP_OK = 200

# init request session
s = requests.Session()
s.auth = ('admin', 'admin')
r = s.request(method='GET', url='http://localhost:8080/remote.php/webdav/example.txt')

# check result
if r.status_code == HTTP_OK:
    print('HTTP return the file')
    print('Content is: "%s"' % r.text)
else:
    print('HTTP error (code %d)' % r.status_code)
