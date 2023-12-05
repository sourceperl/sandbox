# API endpoints

## List all available metrics

```bash
curl -s http://127.0.0.1:8428/api/v1/label/__name__/values | jq
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

To avoird to add field part to metric name, we can use "unnamed metric" like in line ",tag1=value1,tag2=value2 my_metric=1.0"

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