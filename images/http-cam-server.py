#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from ipaddress import ip_address
import socket
from threading import Thread, Lock
import time
from typing import Any
import cv2
from PIL import Image


# some class
class ImgShare:
    """Image sharing class."""

    def __init__(self) -> None:
        self._img_lock = Lock()
        self._img = Image.new(mode='RGB', size=(100,100), color=(255,255,255))

    def from_array(self, value, mode='RGB'):
        with self._img_lock:
            self._img = Image.fromarray(value, mode=mode) 

    def to_jpeg(self):
        io_img = BytesIO()
        with self._img_lock:
            self._img.save(io_img, format='JPEG')
        return io_img.getvalue()


class Shares:
    """Container class for global shares."""
    cam_img = ImgShare()


class HttpSrv:
    """A multi-threaded HTTP server for share camera image."""

    class HandleRequests(BaseHTTPRequestHandler):
        """Custom HTTP handler"""

        def version_string(self) -> str:
            """Replace default server banner."""
            return 'pi-camera server'

        def log_message(self, format: str, *args: Any) -> None:
            """Replace log_message to turn off log msg."""
            return None

        def do_GET(self):
            """Process HTTP GET request."""
            # catch socket errors
            try:
                # process every HTTP GET endpoints
                if self.path == '/test':
                    # headers
                    self.send_response(200)
                    self.send_header('content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    # body
                    self.wfile.write(f'current timestamp: {time.time()}'.encode('utf-8'))
                elif self.path == '/image.jpg':
                    # headers
                    self.send_response(200)
                    self.send_header('cache-control', 'no-cache')
                    self.send_header('content-type', 'image/jpeg')
                    self.end_headers()
                    # body
                    self.wfile.write(Shares.cam_img.to_jpeg())
                # on other path, nothing for you here
                else:
                    # return HTTP 404 page not found
                    self.send_response(404)
                    self.end_headers()
            except socket.error:
                pass

    @property
    def is_run(self):
        """Check if server currently processing requests."""
        return self._http_srv_run

    def __init__(self, port: int = 8080, bind: str = 'localhost'):
        # public
        self.port = port
        self.bind = bind
        # private
        self._http_srv = None
        self._http_srv_th = None
        self._http_srv_run = False

    def start(self):
        """Start HTTP server as a thread."""
        # autodetect IPv6 address
        try:
            ipv6 = ip_address(self.bind).version == 6
        except ValueError:
            ipv6 = False
        # add IPv6 support to ThreadingHTTPServer if needed
        if ipv6:
            ThreadingHTTPServer.address_family = socket.AF_INET6
        #  init HTTP server
        ThreadingHTTPServer.allow_reuse_address = True
        self._http_srv = ThreadingHTTPServer((self.bind, self.port), self.HandleRequests)
        # pass a_thing to HandleRequests (available at HandleRequests.server.a_thing)
        # self._http_srv.a_thing = self.a_thing
        # start server in a separate thread
        self._http_srv_th = Thread(target=self._http_srv.serve_forever, daemon=True)
        self._http_srv_th.start()

    def stop(self):
        """Stop HTTP server thread."""
        self._http_srv.shutdown()
        self._http_srv.server_close()


# main program
if __name__ == '__main__':
    # init camera
    cam = cv2.VideoCapture(0)
    # init and start HTTP server
    srv = HttpSrv(bind='0.0.0.0')
    srv.start()
    # main loop
    while True:
        # read 5 time to flush images buffer
        for _ in range(5):
            read_ok, cam_img = cam.read()
        if not read_ok:
            break
        # format image
        # cam_img = cv2.rotate(cam_img, cv2.ROTATE_180)
        rgb_img = cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)
        Shares.cam_img.from_array(rgb_img, mode='RGB')
        time.sleep(0.5)
    cam.release()
