#!/usr/bin/env python3

"""Camera web server.

Server paths:
  /
  |-- index.html [main page]
  |-- image.jpg [cam as static JPEG image]
  |-- stream.jpg [cam as MJPEG stream]
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from ipaddress import ip_address
import socket
from threading import Thread, Lock
import time
from typing import Any
from urllib.parse import urlparse, parse_qs
import cv2
from PIL import Image
import pantilthat


# some class
class ImgShare:
    """Image sharing class."""

    def __init__(self) -> None:
        self._img_lock = Lock()
        self._img = Image.new(mode='RGB', size=(100, 100), color='gray')

    def from_array(self, array, mode: str = 'RGB') -> None:
        """Load image from a numpy array."""
        with self._img_lock:
            self._img = Image.fromarray(array, mode=mode)

    def to_jpeg(self) -> bytes:
        """Get the image as jpeg encoded bytes."""
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
            return 'My camera server'

        # currently disable: remove "_" prefix to enable
        def _log_message(self, format: str, *args: Any) -> None:
            """Replace log_message to turn off log msg."""
            return None

        def do_GET(self):
            """Process HTTP GET request."""
            # catch socket errors
            try:
                # decode real path (without args) and optionals args
                p_result = urlparse(self.path)
                path = p_result.path
                args_d = parse_qs(p_result.query)
                # process every HTTP GET endpoints
                # endpoint: index.html (default one)
                if path == '/' or path == '/index.html':
                    # headers
                    self.send_response(200)
                    self.send_header('content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    # body
                    with open(f'index.html', 'rb') as f:
                        self.wfile.write(f.read())
                # endpoint: static directory
                elif path.startswith('/static/'):
                    try:
                        static_path = path[len('/static/'):]
                        with open(f'static/{static_path}', 'rb') as f:
                            data = f.read()
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(data)
                    except FileNotFoundError:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(b'not found')
                    except PermissionError:
                        self.send_response(403)
                        self.end_headers()
                        self.wfile.write(b'no permission')
                # endpoint: static JPEG image
                elif path == '/image.jpg':
                    # headers
                    self.send_response(200)
                    self.send_header('cache-control', 'no-cache')
                    self.send_header('content-type', 'image/jpeg')
                    self.end_headers()
                    # body
                    self.wfile.write(Shares.cam_img.to_jpeg())
                # endpoint: MJPEG stream
                elif path == '/stream.jpg':
                    # produce MJPEG stream
                    self.send_response(200)
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--new_frame')
                    self.end_headers()
                    # stream loop
                    while True:
                        # retrieve next frame
                        frame_jpg = Shares.cam_img.to_jpeg()
                        # headers
                        self.wfile.write(b'--new_frame\r\n')
                        self.send_header('Content-type', 'image/jpeg')
                        self.send_header('Content-length', f'{len(frame_jpg)}')
                        self.end_headers()
                        # body
                        self.wfile.write(frame_jpg)
                        time.sleep(0.05)
                # endpoint: action
                elif path == '/action':
                    # call action
                    try:
                        try:
                            action_id = args_d['id'][0]
                        except KeyError:
                            raise RuntimeError('no mandatory "id" field')
                        # call know actions
                        if action_id == 'left':
                            pantilthat.pan(pantilthat.get_pan() + 1)
                        elif action_id == 'up':
                            pantilthat.tilt(pantilthat.get_tilt() - 1)
                        elif action_id == 'down':
                            pantilthat.tilt(pantilthat.get_tilt() + 1)
                        elif action_id == 'right':
                            pantilthat.pan(pantilthat.get_pan() - 1)
                        else:
                            raise RuntimeError('this action id is invalid')
                        # HTTP: report success
                        # headers
                        self.send_response(200)
                        self.end_headers()
                        # body
                        self.wfile.write(b'ok')
                    except RuntimeError as e:
                        # HTTP: report error
                        # headers
                        self.send_response(500)
                        self.end_headers()
                        # body
                        self.wfile.write(f'{e}'.encode())
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
        # flush cv2 images buffer
        for _ in range(4):
            cam.read()
        # read current image
        read_ok, cam_img = cam.read()
        if not read_ok:
            break
        # rotate of 180 degree and convert color to RGB
        cam_img = cv2.rotate(cam_img, cv2.ROTATE_180)
        rgb_img = cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)
        Shares.cam_img.from_array(rgb_img, mode='RGB')
        time.sleep(0.5)
    cam.release()
