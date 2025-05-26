#!/usr/bin/bash


LATEST=$(curl -s https://api.github.com/repos/VictoriaMetrics/VictoriaMetrics/releases/latest | jq -r .tag_name)
echo "the latest available version of VictoriaMetrics is ${LATEST}"
