"""
Skeleton: a threaded TCP server built on the standard library's socketserver.

This module demonstrates how to:
- run the server in blocking or non-blocking (background thread) mode.
- let the OS pick a free port (if port=0).
- stop cleanly, including client sessions, thanks to a shared Event.

Testing:
  You can test the server using netcat (nc).
  Example: $ nc localhost 7777
  Then type 'ping' to receive 'pong' or any other text to see it echoed back.
"""

import logging
import socket
from datetime import datetime, timezone
from enum import Enum, auto
from socketserver import BaseRequestHandler, ThreadingTCPServer
from threading import Event, Thread
from typing import Any, Optional, Tuple


class RunMode(Enum):
    BLOCK = auto()
    NO_BLOCK = auto()


class MyThreadingTCPServer(ThreadingTCPServer):
    """
    A threaded TCP server that allows external control over the lifecycle
    of active client sessions via a shared Event flag.
    """
    daemon_threads = True       # stop() does not wait for client sessions
    allow_reuse_address = True  # allow a quick restart on a fixed port
    request_queue_size = 128    # listen backlog (socketserver default is 5)
    _is_run_evt: Event          # set by the controller, read by the handlers
    logger: logging.Logger


class MyRequestHandler(BaseRequestHandler):
    """
    Handles individual client connections.
    Implements a basic ping-pong and echo mechanism.
    """
    server: MyThreadingTCPServer
    ping_response: str

    def setup(self) -> None:
        """Initialize some things for the current TCP session."""
        # set timeout on current socket
        self.request.settimeout(0.5)
        # format "ping" response
        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        self.ping_response = f"pong (TCP session begin at {now_iso})\n"

    def handle(self) -> None:
        """
        Processes the client request.
        Echoes received data back to the client or responds to 'ping'.
        """
        while self.server._is_run_evt.is_set():
            try:
                data = self.request.recv(1024)
            except socket.timeout:
                continue  # nothing received: test the stop event again
            except OSError:
                break     # broken connection -> exit

            if not data:
                break     # the client closed the connection -> exit

            # process receive data
            try:
                if data == b'ping\n':
                    self.server.logger.debug(f'receive a ping command from {self.request.getpeername()}')
                    self.request.sendall(self.ping_response.encode())
                else:
                    self.request.sendall(data)  # echo, as bytes: no decode()
            except OSError:
                break


class MyServerController:
    """
    Controller for managing the lifecycle of MyThreadingTCPServer.

    Provides high-level methods to start the server in either blocking
    or non-blocking mode and ensures a clean shutdown.
    """

    def __init__(self, host: str = "localhost", port: int = 7777, no_block: bool = True):
        # Args
        self.host = host
        self.port = port
        self.no_block = no_block
        # Internal variables
        self.logger = logging.getLogger(self.__class__.__name__)
        self.server: Optional[MyThreadingTCPServer] = None
        self.server_thread: Optional[Thread] = None
        self._is_blocking = False
        # (host, port) of the listening socket, set as soon as the server is bound (see bound_address)
        self._bound_address: Optional[Tuple[str, int]] = None
        # Shared "keep running" flag
        self._is_run_evt = Event()

    @property
    def bound_address(self) -> Optional[Tuple[str, int]]:
        """The (host, port) the server listens on, None if it isn't started.

        Set as soon as the server is bound, so it is available from another thread even in blocking mode.
        """
        return self._bound_address

    def start(self) -> None:
        """
        Start the TCP server.

        Raises:
            OSError: If the server cannot bind to the specified host and port.
        """
        if self.server is not None:
            self.logger.warning("The server is already running.")
            return

        # Create the server (use port=0 to let the OS choose a free port).
        self.server = MyThreadingTCPServer((self.host, self.port), MyRequestHandler)
        # share some vars with server
        self.server._is_run_evt = self._is_run_evt
        self.server.logger = self.logger
        self._is_run_evt.set()

        # Fix: server_address returns a tuple (address, port).
        # We cast address to str to satisfy Mypy's strict type checking.
        self._bound_address = (str(self.server.server_address[0]), int(self.server.server_address[1]))

        # save blocking status for this run
        self._is_blocking = not self.no_block

        if self._is_blocking:
            # Blocking mode
            try:
                # This method block until self.server.shutdown() is called or an execept is raise
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.logger.info("Interrupt detected...")
                self.stop()
        else:
            # Non-blocking mode: server started in the background
            self.server_thread = Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()

    def wait(self) -> None:
        """
        Block the main thread while the server is running in the background.

        This method allows the main thread to remain responsive to KeyboardInterrupt
        while waiting for the server thread to finish.
        """
        if self.server is None:
            self.logger.error("Cannot wait: the server is not started.")
            return

        if self._is_blocking or self.server_thread is None:
            self.logger.error("Cannot wait: the server is not running in the background.")
            return

        try:
            while self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=0.5)
        except KeyboardInterrupt:
            self.logger.info("Ctrl+C detected while waiting...")
            self.stop()

    def stop(self) -> None:
        """
        Stop the server cleanly and release all bound resources.
        """
        if self.server is None:
            self.logger.warning("The server is not started.")
            return

        self.logger.info("Stopping the server...")
        # 1. tell the client sessions to end gracefully
        self._is_run_evt.clear()

        try:
            # 2. stop accepting new connections (stops the serve_forever loop)
            self.server.shutdown()
        finally:
            # 3. close the listening socket
            self.server.server_close()

        if not self._is_blocking and self.server_thread:
            self.server_thread.join()

        self.server = None
        self.server_thread = None
        self._bound_address = None
        self.logger.info("Server stopped and port released.")

    def __enter__(self) -> "MyServerController":
        """Context manager entry: starts the server in non-blocking mode."""
        self.start()
        return self

    def __exit__(self, exc_type: Optional[Any], exc_val: Optional[Any], exc_tb: Optional[Any]) -> None:
        """Context manager exit: ensures the server is stopped."""
        self.stop()


if __name__ == "__main__":
    # Configure logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)-18s - %(levelname)s - %(message)s')

    # Choose mode to run
    RUN = RunMode.NO_BLOCK

    if RUN == RunMode.NO_BLOCK:
        # Non-blocking mode
        with MyServerController("localhost", port=7777) as server:
            logger.info("The main thread keeps running!")
            if server.bound_address is not None:
                logger.info(f"Use this port to connect your clients: {server.bound_address[1]}")
            logger.info("Press Ctrl+C to stop the server cleanly.")
            # block the main thread until Ctrl+C
            server.wait()

    if RUN == RunMode.BLOCK:
        # Blocking mode
        # - Don't launch another thread to run serve_forever() method.
        # - Unable to read the current TCP port in case of dynamic allocation (port=0).
        MyServerController("localhost", port=7777, no_block=False).start()

    logger.info("End of script.")
