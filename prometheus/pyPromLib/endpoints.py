"""This module implement pyPromLib endpoints class."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
import socket
from threading import Thread, Lock
from typing import Any
from .metrics import Metric


class MetricsHttpSrv:
    """A multi-threaded HTTP server for shares metrics with Prometheus."""

    class HandleRequests(BaseHTTPRequestHandler):
        """Custom HTTP handler"""

        def version_string(self) -> str:
            """Replace default server banner."""
            return 'self-service here ;-)'

        def log_message(self, format: str, *args: Any) -> None:
            """Replace log_message to turn off log msg."""
            return None

        def do_GET(self):
            """Process HTTP GET request."""
            # catch socket errors
            try:
                # for prometheus scrap endpoint
                if self.path == '/metrics':
                    # headers
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    # body
                    self.wfile.write(self.server.metrics_srv.as_text().encode('utf-8'))
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
        self._th_lock = Lock()
        self._metrics_l = list()
        self._http_srv = None
        self._http_srv_th = None
        self._http_srv_run = False

    def add(self, metric: Metric):
        """Add metric to server share list."""
        with self._th_lock:
            self._metrics_l.append(metric)

    def remove(self, metric: Metric):
        """Remove metric from server share list."""
        with self._th_lock:
            self._metrics_l.remove(metric)

    def as_text(self) -> str:
        """Export metrics as Prometheus scrap file."""
        txt = ''
        with self._th_lock:
            for metric in self._metrics_l:
                txt += metric.as_text()
        return txt

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
        # pass metrics_srv to HandleRequests (available at HandleRequests.server.metrics_server)
        self._http_srv.metrics_srv = self
        # start server in a separate thread
        self._http_srv_th = Thread(target=self._http_srv.serve_forever, daemon=True)
        self._http_srv_th.start()

    def stop(self):
        """Stop HTTP server thread."""
        self._http_srv.shutdown()
        self._http_srv.server_close()
