cd ../../../../

role=${1}

python federatedscope/db/main.py --cfg federatedscope/db/demo/mda/${role}.yaml data.root federatedscope/db/demo/mda/data/${role}.csv
