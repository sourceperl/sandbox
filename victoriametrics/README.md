# API endpoints

## Setup for API test

```bash
# install curl and json parser "jq"
sudo apt install curl jq 
```

## Request instant metric value

```bash
# query for my_metric last value until 15 minutes ago from now
curl -s 'http://127.0.0.1:8428/api/v1/query' -d 'query=my_metric{}' -d 'step=15m' | jq .data.result
```

## Request range metric values

```bash
# query values for my_metric from last hour with steps of 1 minute
curl -s 'http://127.0.0.1:8428/api/v1/query_range' -d 'query=my_metric{}' -d 'start=-1h' -d 'end=now' -d 'step=1m' | jq .data.result
```

## List all available metrics

```bash
curl -s http://127.0.0.1:8428/api/v1/label/__name__/values | jq .data
```

## Push metrics with Prometheus exposition format

Prometheus exposition format: "metric_name{label_name="label_value"} value timestamp_ms"

```bash
# push metric value
curl -s 'http://127.0.0.1:8428/api/v1/import/prometheus' -d "my_metric{tag=\"foo\"} 42.0 `date +%s%3N`"
# push metric value (use current VM DB host time)
curl -s 'http://127.0.0.1:8428/api/v1/import/prometheus' -d 'my_metric{tag="foo"} 42.0'
```

## Push metrics with influxdb line protocol

On VM line protocol "my_metric,tag1=value1,tag2=value2 field1=1.0,field2=2.0"

publish:
- my_metric_field1{tag1="value1", tag2="value2"} 1.0
- my_metric_field2{tag1="value1", tag2="value2"} 2.0

```bash
# write
curl -d 'my_metric,tag1=value1,tag2=value2 field1=1.0,field2=2.0' -X POST 'http://127.0.0.1:8428/write'
# read
curl -s 'http://127.0.0.1:8428/api/v1/query?query=my_metric_field1' | jq
curl -s 'http://127.0.0.1:8428/api/v1/query?query=my_metric_field2' | jq
```

To avoid adding field part to metric name, we can use "unnamed metric" like in line ",tag1=value1,tag2=value2 my_metric=1.0"

publish:
- my_metric{tag1="value1", tag2="value2"} 1.0

```bash
# write
curl -d ',tag1=value1,tag2=value2 my_metric=1.0' -X POST 'http://127.0.0.1:8428/write'
# read
curl -s 'http://127.0.0.1:8428/api/v1/query?query=my_metric' | jq
```

## Push metrics like graphite agents (lighter than HTTP)

Run VictoriaMetics with graphite socket turn on.

```bash
/path/to/victoria-metrics-prod -graphiteListenAddr=:2003
```

Publish a metric :

```bash
# with date
echo "my_metric;tag1=value1;tag2=value2 123 `date +%s`" | nc -N localhost 2003
# or without
echo "my_metric;tag1=value1 123" | nc -N localhost 2003
```

## Export and import

### As a json list

```bash
# export a specific metric
curl -s http://127.0.0.1:8428/api/v1/export -d 'match[]=my_metric' > my_metric.jsonl
# export all with gzip compression
curl -s http://127.0.0.1:8428/api/v1/export -d 'match[]={__name__!=""}' | gzip > vm_full.jsonl.gz
# import
curl -s http://127.0.0.1:8428/api/v1/import -T my_metric.jsonl
# import a gzipped file
curl -s -X POST -H 'Content-Encoding: gzip' http://127.0.0.1:8428/api/v1/import -T vm_full.jsonl.gz
```

## Delete a metric

```bash
curl -s http://127.0.0.1:8428/api/v1/admin/tsdb/delete_series -d 'match[]=my_metric'
```
