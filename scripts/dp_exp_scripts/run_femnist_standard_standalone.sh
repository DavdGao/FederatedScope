set -e

cudaid=$1
outdir=exp_out/per_client_dp

if [ ! -d ${outdir} ];then
  mkdir -p ${outdir}
fi

echo "HPO starts..."


for i in {0..100..5}
do
  python federatedscope/main.py --cfg federatedscope/cv/baseline/fedavg_convnet2_on_femnist.yaml \
  --client_cfg_file scripts/dp_exp_scripts/per_client_yaml/${i}_clients.yaml

done

echo "HPO Ends."

