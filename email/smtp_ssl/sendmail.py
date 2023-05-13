#!/usr/bin/env python3

""" Send email with SMTP protocol. """

from dataclasses import dataclass
import logging
import re
import smtplib
from typing import List, Sequence, Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from private_data import SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_TO


# some class
@dataclass
class FileAttachment:
    name: str
    content: bytes = b''


# some function
def is_html(text: str) -> bool:
    """Check if text contain HTML code."""
    pattern = re.compile(r'<\w*?>')
    return pattern.search(text) is not None


def send_mail(to_addrs: Union[str, Sequence[str]], subject: str = '', body: str = '', attachs: List[FileAttachment] = None):
    """Send an email with SMTP SSL."""
    # params
    addr_l = []
    if isinstance(to_addrs, str):
        addr_l.append(to_addrs)
    elif isinstance(to_addrs, (list, tuple)):
        addr_l = list(to_addrs)
    if attachs is None:
        attachs = []
    # connect and login
    smtp = smtplib.SMTP_SSL(host='smtp.free.fr', port=465, timeout=30.0)
    smtp.login(SMTP_USER, SMTP_PASS)
    # format mail
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = ', '.join(addr_l)
    # add body (auto-detect html type)
    msg.attach(MIMEText(body, 'html' if is_html(body) else 'plain'))
    # add attachments
    for file in attachs:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file.name}')
        msg.attach(part)
    # send
    send_status = smtp.sendmail(SMTP_FROM, to_addrs, msg.as_string())
    logging.debug(f'SMTP status: {send_status}')
    smtp.quit()


if __name__ == '__main__':
    # logging setup
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    # email attachments
    attachs = (FileAttachment('readme.txt', b'my text'), )
    # send mail
    send_mail(to_addrs=SMTP_TO, subject='My file', body='See file attached.', attachs=attachs)
