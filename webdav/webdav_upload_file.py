#!/usr/bin/env python3
import requests

# some consts
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
FILE_CONTENT = 'this is an example'.encode('utf8')

# init request session
s = requests.Session()
s.auth = ('admin', 'admin')
r = s.request(method='PUT', url='http://localhost:8080/remote.php/webdav/example.txt',
              data=FILE_CONTENT)

# check result
if r.status_code == HTTP_CREATED:
    print('HTTP create the file')
elif r.status_code == HTTP_NO_CONTENT:
    print('HTTP update the file')
