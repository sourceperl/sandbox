#!/usr/bin/env python3

""" Send email with SMTP protocol. """

from dataclasses import dataclass
import logging
import re
import smtplib
from typing import Sequence, Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from private_data import SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_TO


# some class
@dataclass
class FileAttachment:
    """File attachment container"""
    name: str
    content: bytes = b''


# some function
def is_html(text: str) -> bool:
    """Check if text contain HTML code."""
    pattern = re.compile(r'<\w*?>')
    return pattern.search(text) is not None


def send_mail(to_addrs: Union[str, Sequence[str]], subject: str = '', body: str = '',
              atts: Union[FileAttachment, Sequence[FileAttachment]] = None):
    """Send an email with SMTP SSL."""
    # params
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]
    if atts is None:
        atts = []
    elif isinstance(atts, FileAttachment):
        atts = [atts]
    # connect and login
    smtp = smtplib.SMTP_SSL(host='smtp.free.fr', port=465, timeout=30.0)
    smtp.login(SMTP_USER, SMTP_PASS)
    # format mail
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = ', '.join(to_addrs)
    # add body (auto-detect html type)
    msg.attach(MIMEText(body, 'html' if is_html(body) else 'plain'))
    # add attachments
    for file in atts:
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
    my_atts = FileAttachment('readme.txt', b'file content')
    # send mail
    send_mail(to_addrs=SMTP_TO, subject='My file', body='See file attached.', atts=my_atts)
