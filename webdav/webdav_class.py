#!/usr/bin/env python3

from urllib.parse import urljoin, urlparse, quote, unquote
from xml.dom import minidom
import dateutil.parser
import requests
import urllib3

# configure package (disable warning for self-signed certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# some consts
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_MULTI_STATUS = 207
HTTP_UNAUTHORIZED = 401

# config
webdav_url = 'http://localhost:8080/remote.php/webdav/'
webdav_user = 'admin'
webdav_pass = 'admin'


class WebDAVError(Exception):
    pass


class WebDAV:
    def __init__(self, url, username='', password='', timeout=5.0):
        # public
        self.last_http_code = 0
        self.timeout = timeout
        # private
        self._url = url if url.endswith('/') else url + '/'
        self._url_path = urlparse(self._url).path
        self._session = requests.Session()
        # auth
        if username:
            self._session.auth = (username, password)

    def _url_with_path(self, path=''):
        return urljoin(self._url, quote(path))

    def upload(self, file_path, content=b''):
        # do request
        r = self._session.request(method='PUT', url=self._url_with_path(file_path),
                                  data=content, timeout=self.timeout, verify=False)
        self.last_http_code = r.status_code
        # return status (True if upload ok)
        # HTTP_CREATED => create file, HTTP_NO_CONTENT => update an existing file
        if not (r.status_code == HTTP_CREATED or r.status_code == HTTP_NO_CONTENT):
            raise WebDAVError('Error during upload of file "%s" (HTTP code is %i)' % (file_path,
                                                                                      self.last_http_code))

    def download(self, file_path):
        # do request
        r = self._session.request(method='GET', url=self._url_with_path(file_path),
                                  timeout=self.timeout, verify=False)
        self.last_http_code = r.status_code
        # return file content if request ok, None if error
        if r.status_code == HTTP_OK:
            return r.content
        else:
            raise WebDAVError('Error during download of file "%s" (HTTP code is %i)' % (file_path,
                                                                                        self.last_http_code))

    def delete(self, file_path):
        # do request
        r = self._session.request(method='DELETE', url=self._url_with_path(file_path),
                                  timeout=self.timeout, verify=False)
        self.last_http_code = r.status_code
        # return status (True if file delete is ok)
        if r.status_code != HTTP_NO_CONTENT:
            raise WebDAVError('Error during deletion of file "%s" (HTTP code is %i)' % (file_path,
                                                                                        self.last_http_code))

    def mkdir(self, dir_path):
        # do request
        r = self._session.request(method='MKCOL', url=self._url_with_path(dir_path),
                                  timeout=self.timeout, verify=False)
        self.last_http_code = r.status_code
        # return status (True if directory is created)
        if r.status_code != HTTP_CREATED:
            raise WebDAVError('Error during creation of dir "%s" (HTTP code is %i)' % (dir_path,
                                                                                       self.last_http_code))

    def ls(self, path='', depth=1):
        # build xml message
        propfind_request = '<?xml version="1.0" encoding="utf-8" ?>' \
                           '<d:propfind xmlns:d="DAV:">' \
                           '<d:prop><d:getlastmodified/><d:getcontentlength/></d:prop> ' \
                           '</d:propfind>'
        # do request
        r = self._session.request(method='PROPFIND',
                                  url=self._url_with_path(path),
                                  data=propfind_request, headers={'Depth': '%i' % depth},
                                  timeout=self.timeout, verify=False)
        self.last_http_code = r.status_code
        # check result
        if self.last_http_code == HTTP_MULTI_STATUS:
            # return a list of dict
            results_l = []
            # parse XML
            dom = minidom.parseString(r.text.encode('ascii', 'xmlcharrefreplace'))
            # for every d:response
            for response in dom.getElementsByTagName('d:response'):
                # in d:response/d:propstat/d:prop
                prop_stat = response.getElementsByTagName('d:propstat')[0]
                prop = prop_stat.getElementsByTagName('d:prop')[0]
                # d:getlastmodified
                get_last_modified = prop.getElementsByTagName('d:getlastmodified')[0].firstChild.data
                dt_last_modified = dateutil.parser.parse(get_last_modified)
                # d:getcontentlength
                try:
                    content_length = int(prop.getElementsByTagName('d:getcontentlength')[0].firstChild.data)
                except IndexError:
                    content_length = 0
                # href at d:response level
                href = response.getElementsByTagName('d:href')[0].firstChild.data
                # convert href to file path
                if href.startswith(self._url):
                    href = href[len(self._url):]
                elif href.startswith(self._url_path):
                    href = href[len(self._url_path):]
                file_path = unquote(href)
                file_path = file_path[len(path):]
                # feed result list
                results_l.append(dict(file_path=file_path, content_length=content_length,
                                      dt_last_modified=dt_last_modified))
            return results_l
        else:
            raise WebDAVError("Error during PROPFIND (ls) request (HTTP code is %i)" % self.last_http_code)


# main
if __name__ == '__main__':
    # first create webdav client
    w = WebDAV(webdav_url, username=webdav_user, password=webdav_pass)

    try:
        # list root directory contents
        print('\n%s %35s %s\n' % ('#' * 16, 'webdav ls (PROPFIND) example'.center(35), '#' * 16))
        for f in w.ls(path=''):
            print('%12s  %10s  %s' % (f['content_length'], f['dt_last_modified'], f['file_path']))

        # upload
        print('\n%s %35s %s\n' % ('#' * 16, 'webdav upload example'.center(35), '#' * 16))
        w.upload('__example.txt', 'this is a sample content'.encode('utf8'))
        # w.upload('__example.txt', open('__example.txt', 'rb').read())
        print('DONE')

        # download
        print('\n%s %35s %s\n' % ('#' * 16, 'webdav download example'.center(35), '#' * 16))
        data = w.download('__example.txt')
        if data:
            print('DONE')
            print('content of file is "%s"' % data.decode('utf8'))
            # open('__example.txt', 'wb').write(data)

        # delete
        print('\n%s %35s %s\n' % ('#' * 16, 'webdav delete example'.center(35), '#' * 16))
        w.delete('__example.txt')
        print('DONE')
    except WebDAVError as e:
        print('webdav error (%s)' % e)
