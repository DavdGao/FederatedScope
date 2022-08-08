#!/bin/bash

usage() {
  echo 'usage: ./run.sh [server | client client_id | shuffler]'
}

cd ../../../../

if [ $# -eq 0 ]
then
  usage
elif [ $1 == "server" ]
then
  python federatedscope/db/main.py --cfg federatedscope/db/demo/solh/server.yaml data.root federatedscope/db/demo/solh/data/server.csv
elif [ $1 == "client" ]
then
  if [ $# -ge 2 ]
  then
    python federatedscope/db/main.py --cfg federatedscope/db/demo/solh/client$2.yaml data.root federatedscope/db/demo/solh/data/client$2.csv
  else
    usage
  fi
elif [ $1 == "shuffler" ]
then
  python federatedscope/db/main.py --cfg federatedscope/db/demo/solh/shuffler.yaml data.root federatedscope/db/demo/solh/data/shuffler.csv
else
  usage
fi