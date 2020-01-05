#!/usr/bin/env python3
import requests

# some consts
HTTP_NO_CONTENT = 204

# init request session
s = requests.Session()
s.auth = ('admin', 'admin')
r = s.request(method='DELETE', url='http://localhost:8080/remote.php/webdav/example.txt')

# check result
if r.status_code == HTTP_NO_CONTENT:
    print('HTTP delete the file')
else:
    print('HTTP error (code %d)' % r.status_code)
