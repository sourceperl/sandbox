#!/usr/bin/bash

# use exec to ensure vm replace the bash process
# PID used by supervisord for start/stop operations will point to vm and not on bash process
exec /opt/vm/bin/victoria-metrics-prod -storageDataPath="/opt/vm/data/" \
                                       -httpListenAddr="127.0.0.1:8428" \
                                       -graphiteListenAddr="127.0.0.1:2003" \
                                       -search.latencyOffset="2s" \
                                       -retentionPeriod="24w"
