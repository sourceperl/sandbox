#!/usr/bin/bash

# some const
VERSION_TARGET="v1.115.0"
ARCH="arm64"
#ARCH="amd64"

# abort on error
set -e

# show versions
echo -n "current version is : "
curl -s http://localhost:8428/metrics | grep '^vm_app_version' | sed -n 's/.*short_version="\([^"]*\)".*/\1/p'
echo -n "target version is  : "
echo ${VERSION_TARGET}

# download
echo "download new release to bin directory"
FILE="victoria-metrics-linux-${ARCH}-${VERSION_TARGET}.tar.gz"
URL="https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/${VERSION_TARGET}/${FILE}"
curl -L ${URL} | tar -xz -C /opt/vm/bin/

# reload
echo "reload VictoriaMetrics"
sudo supervisorctl restart vm

# show version
echo -n "current version is : "
curl -s http://localhost:8428/metrics | grep '^vm_app_version' | sed -n 's/.*short_version="\([^"]*\)".*/\1/p'
