#!/bin/bash

usage() {
  echo 'usage: ./run.sh [server | client client_id]'
}

cd ../../../../

if [ $# -eq 0 ]
then
  usage
elif [ $1 == "server" ]
then
  python federatedscope/db/main.py --cfg federatedscope/db/demo/mda/server.yaml data.root federatedscope/db/demo/mda/data/server.csv
elif [ $1 == "client" ]
then
  if [ $# -ge 2 ]
  then
    python federatedscope/db/main.py --cfg federatedscope/db/demo/mda/client$2.yaml data.root federatedscope/db/demo/mda/data/client$2.csv
  else
    usage
  fi
else
  usage
fi