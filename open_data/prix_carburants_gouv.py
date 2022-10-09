#!/usr/bin/env python3

"""Retrieve current gasoline price at specific station."""

from io import BytesIO
import urllib.error
from urllib.request import urlopen
from zipfile import ZipFile
# sudo apt install python3-defusedxml
import defusedxml.ElementTree as ET


# some const
DATA_URL='https://donnees.roulez-eco.fr/opendata/instantane'
XML_FILE = 'PrixCarburants_instantane.xml'

try:
    # request zip archive from web server
    resp = urlopen(DATA_URL, timeout=4.0)
    # extract xml data from zip archive
    xml_b = None
    zf = ZipFile(BytesIO(resp.read()), mode='r')
    for zi in zf.infolist():
        if zi.filename == XML_FILE:
            xml_b = zf.read(zi)
            break
    # test the availablity of XML data
    if not xml_b:
        raise ValueError(f'"{XML_FILE}" missing in zip archive')
    # parse XML
    root = ET.fromstring(xml_b)
    for pdv in root.findall('pdv'):
        if pdv.attrib.get('id') == '59320001':
            for prix in pdv.findall('prix'):
                print(f'{prix.attrib["nom"]:8s} {prix.attrib["valeur"]} EUR  ({prix.attrib["maj"]})')
except (urllib.error.URLError, ValueError) as e:
    print(f'error occur: {e!r}')
