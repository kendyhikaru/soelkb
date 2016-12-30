#!/bin/bash

set -e

host="$1"
shift
cmd="logstash -f /etc/logstash/conf.d -l /var/log/logstash/ --log.level info"

until curl -XGET $host:9200; do
  >&2 echo "Elastic is unavailable - sleeping"
  sleep 1
done

>&2 echo "Elastic is up - executing command"
exec $cmd
