#!/usr/bin/bash

# Utiliser curl pour récupérer les informations de la dernière version
LATEST=$(curl -s https://api.github.com/repos/VictoriaMetrics/VictoriaMetrics/releases/latest | jq -r .tag_name)

# Extraire le tag_name qui contient la version
echo "the latest available version of VictoriaMetrics is ${LATEST}"
