#!/usr/bin/env python3

"""Check if current public IPv4 is in sync with no-ip DNS. If not, update no-ip DNS.
more info: https://www.noip.com/integrate/request
"""

from base64 import standard_b64encode
from ipaddress import IPv4Address
import logging
import socket
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError
from private_data import NOIP_USER, NOIP_PASS, NOIP_HOSTNAME


# some consts
MIN_UPTIME_S = 180


# logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(message)s', level=logging.INFO)

# wait until system uptime reach MIN_UPTIME_S seconds
uptime = float(open('/proc/uptime', 'r').readline().split()[0])
if uptime < MIN_UPTIME_S:
    wait_s = MIN_UPTIME_S - uptime
    logging.info(f'wait {wait_s} s to reach minimum system uptime ({MIN_UPTIME_S} s)')
    time.sleep(wait_s)

# log startup
logging.info('no-ip-updater-app started')

# update loop
while True:
    try:
        # current public IP of the host machine
        pub_ip_txt = urlopen('http://ip1.dynupdate.no-ip.com/', timeout=5.0).read().decode().strip()
        pub_ip = IPv4Address(pub_ip_txt)

        # get IP as seen by DNS server
        dns_ip = IPv4Address(socket.gethostbyname(NOIP_HOSTNAME))

        # log status
        logging.info(f'check DNS status for "{NOIP_HOSTNAME}": public IP = {pub_ip}, DNS record = {dns_ip}')

        # if current DNS record does not match public IP: update no-ip
        if pub_ip != dns_ip:
            logging.info(f'start no-ip update')
            # do HTTPs update request
            update_req = Request(f'https://dynupdate.no-ip.com/nic/update?hostname={NOIP_HOSTNAME}')
            auth_str = standard_b64encode(f'{NOIP_USER}:{NOIP_PASS}'.encode()).decode()
            update_req.add_header('Authorization', f'Basic {auth_str}')
            update_req.add_header('User-Agent', f'Python no-ip-updater/0.1 {NOIP_USER}')
            status_txt = urlopen(update_req, timeout=5.0).read().decode().strip()
            logging.info(f'no-ip update return "{status_txt}"')
    except (socket.error, URLError, ValueError) as e:
        logging.error(f'error "{e!r}" at line: {sys.exc_info()[-1].tb_lineno}')
    # wait for next loop
    time.sleep(1800)
