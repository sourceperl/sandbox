#!/usr/bin/bash

# some const
VERSION_TARGET="v1.118.0"

# abort on error
set -e

# show versions
APP_VERSION_METRIC=$(curl -s http://localhost:8428/metrics | grep '^vm_app_version')
VERSION_CURRENT=$(echo "${APP_VERSION_METRIC}" | sed -n 's/.*short_version="\([^"]*\)".*/\1/p')
echo -n "current version : "
echo ${VERSION_CURRENT}
echo -n "target version  : "
echo ${VERSION_TARGET}
# skip the upgrade if it is already up to date
if [ ${VERSION_CURRENT} = ${VERSION_TARGET} ]; then
    echo "error: current version is already ${VERSION_TARGET}, skip upgrade process"
    exit 2
fi

# automatically detect the target architecture
ARCH_STR=$(uname -m)
if [ ${ARCH_STR} = "x86_64" ]; then
    ARCH="amd64"
elif [ ${ARCH_STR} = "aarch64" ]; then
    ARCH="arm64"
else
    echo "error: architecture '${ARCH_STR}' is not supported"
    exit 1
fi

# download
echo "download new release to bin directory (for architecture '${ARCH}')"
FILE="victoria-metrics-linux-${ARCH}-${VERSION_TARGET}.tar.gz"
URL="https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/${VERSION_TARGET}/${FILE}"
curl -L ${URL} | tar -xz -C /opt/vm/bin/

# reload
echo "reload VictoriaMetrics"
sudo supervisorctl restart vm

# show version
echo -n "current version is : "
curl -s http://localhost:8428/metrics | grep '^vm_app_version' | sed -n 's/.*short_version="\([^"]*\)".*/\1/p'
