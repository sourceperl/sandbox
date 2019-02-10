#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# connect to mediawiki server and export all pages from a category to PDF files
#
# setup to use this script
#   sudo pip3 install mwclient
#   sudo apt-get install wkhtmltopdf

# WARN: wkhtmltopdf need an X server running, so if need, we use xvfb (virtual X server)
#   sudo apt-get install xvfb
# wrap call of wkhtmltopdf to add xvfb
#   cat <<EOF | sudo tee /usr/bin/wkhtmltopdf.sh
#   #!/bin/bash
#   xvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*
#   EOF
#   sudo chmod a+x /usr/bin/wkhtmltopdf.sh
#   sudo ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

# test with:
#   wkhtmltopdf http://www.google.com google.pdf

import mwclient
import subprocess
from urllib import parse

site = mwclient.Site("en.wikipedia.org")

for page in site.Categories["Arduino"]:
    # build pdf
    url = "https://en.wikipedia.org/wiki/%s" % parse.quote(page.name)
    pdf_file = "%s.pdf" % page.name
    pdf_build_status = subprocess.call(["wkhtmltopdf", url, pdf_file])
    # print build status
    if pdf_build_status == 0:
        print("render of %s to %s OK" % (url, pdf_file))
    else:
        print("render of %s to %s error" % (url, pdf_file))
