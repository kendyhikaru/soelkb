#!/bin/bash

set -e

host="$1"
shift
cmd="kibana --log-file /var/log/kibana/kibana.log"

until curl -XGET $host:9200; do
  >&2 echo "Elastic is unavailable - sleeping"
  sleep 1
done

>&2 echo "Elastic is up - executing command"
check=$(head -n 1 /frist_boot)
if [ "$check" == "0" ]; then
	echo "Frist boot"
	/KTS/load.sh http://$host:9200
	echo 1 > /frist_boot
fi
exec $cmd
