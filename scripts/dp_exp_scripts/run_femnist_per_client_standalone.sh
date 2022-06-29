set -e

cudaid=$1
start=$2
end=$3
increment=$4

outdir=exp_out/per_client_dp

if [ ! -d ${outdir} ];then
  mkdir -p ${outdir}
fi

echo "HPO starts..."


for i in $(seq ${start} ${increment} ${end})
do
  id=`echo ${i}|awk '{printf("%03d\n",$0)}'`
  log=${outdir}/${id}_clients.log
  echo ${log}
  python federatedscope/main.py --cfg federatedscope/cv/baseline/fedavg_convnet2_on_femnist.yaml \
  --client_cfg scripts/dp_exp_scripts/per_client_yaml/${id}_clients.yaml \
  data.root /mnt/gaodawei.gdw/data/ \
  device ${cudaid} \
  federate.sample_client_rate 0.5 \
  >>${log} 2>&1
  python federatedscope/parse_exp_results.py --input ${log}
done

echo "HPO Ends."
