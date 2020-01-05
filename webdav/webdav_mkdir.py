#!/usr/bin/env python3
import requests

# some consts
HTTP_CREATED = 201

# init request session
s = requests.Session()
s.auth = ('admin', 'admin')
r = s.request(method='MKCOL', url='http://localhost:8080/remote.php/webdav/Example_dir')

# check result
if r.status_code == HTTP_CREATED:
    print('HTTP create OK')
else:
    print('HTTP error (code %d)' % r.status_code)
