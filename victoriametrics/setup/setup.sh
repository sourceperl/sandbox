#!/usr/bin/bash

# some const
VERSION_TARGET="v1.115.0"
ARCH="arm64"
#ARCH="amd64"

# abort on error
set -e

echo "create directories"
sudo mkdir /opt/vm/ && sudo chown pi:pi /opt/vm/
mkdir -p /opt/vm/bin
mkdir -p /opt/vm/data

echo "populate bin directory"
FILE="victoria-metrics-linux-${ARCH}-${VERSION_TARGET}.tar.gz"
URL="https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/${VERSION_TARGET}/${FILE}"
curl -L ${URL} | tar -xz -C /opt/vm/bin/

echo "add the vm startup script"
cp -v misc/run.sh /opt/vm/

echo "init supervisord"
sudo apt install -y supervisor
sudo cp -v misc/vm.conf /etc/supervisor/conf.d/
sudo supervisorctl update
