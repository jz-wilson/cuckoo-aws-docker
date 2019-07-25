#!/usr/bin/env bash

set -e

setDefaults() {
  export ES_HOST=${ES_HOST:="$(env | grep ELASTIC.*PORT_9200_TCP_ADDR= | sed -e 's|.*=||')"}
  export ES_PORT=${ES_PORT:="$(env | grep ELASTIC.*PORT_9200_TCP_PORT= | sed -e 's|.*=||')"}
  export MONGO_HOST=${MONGO_HOST:="$(env | grep MONGO.*PORT_.*_TCP_ADDR= | sed -e 's|.*=||')"}
  export MONGO_TCP_PORT=${MONGO_TCP_PORT:="$(env | grep MONGO.*PORT_.*_TCP_PORT= | sed -e 's|.*=||')"}
  export POSTGRES_HOST=${POSTGRES_HOST:="$(env | grep POSTGRES.*PORT_.*_TCP_ADDR= | sed -e 's|.*=||')"}
  export POSTGRES_TCP_PORT=${POSTGRES_TCP_PORT:="$(env | grep POSTGRES.*PORT_.*_TCP_PORT= | sed -e 's|.*=||')"}
  env | grep -E "^ES.*|^MONGO_HOST|^MONGO_TCP_PORT|^POSTGRES.*|^RESULTSERVER" | sort -n
}

# Wait for. Params: host, port, service
waitFor() {
    echo -n "===> Waiting for ${3}(${1}:${2}) to start..."
    i=1
    while [[ ${i} -le 20 ]]; do
        if nc -vz ${1} ${2} 2>/dev/null; then
            echo "${3} is ready!"
            return 0
        fi

        echo -n '.'
        sleep 1
        i=$((i+1))
    done

    echo
    echo >&2 "${3} is not available"
    echo >&2 "Address: ${1}:${2}"
}

setUpCuckoo(){
  echo "===> Use default ports and hosts if not specified..."
  #setDefaults
  echo
  echo "===> Update /cuckoo/conf/ if needed..."
  python "/update_conf.py"
  echo
  # Wait until all services are started
  if [[ ! "$ES_HOST" == "" ]]; then
  	waitForElasticsearch
  fi
  echo
  if [[ ! "$MONGO_HOST" == "" ]]; then
  	waitFor ${MONGO_HOST} ${MONGO_TCP_PORT} MongoDB
  fi
  echo
  if [[ ! "$POSTGRES_HOST" == "" ]]; then
  	waitFor ${POSTGRES_HOST} ${POSTGRES_TCP_PORT} Postgres
  fi
}

setUpCuckoo

exec cuckoo "$@"