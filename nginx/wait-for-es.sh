#!/bin/bash

set -e

host1="$1"
host2="$2"
shift
cmd='nginx -g "daemon off;"'

until curl -XGET $host1:5636; do
  >&2 echo "Evebox is unavailable - sleeping"
  sleep 1
done

>&2 echo "Evebox is up - executing command"
until curl -XGET $host2:5601; do
  >&2 echo "Kibana is unavailable - sleeping"
  sleep 1
done

>&2 echo "Kiban is up - executing command"
exec nginx -g "daemon off;"
