#!/usr/bin/bash

/opt/vm/bin/victoria-metrics-prod -storageDataPath="/opt/vm/data/" \
                                  -httpListenAddr="127.0.0.1:8428" \
                                  -graphiteListenAddr="127.0.0.1:2003" \
                                  -retentionPeriod="24w"
