set -e

cudaid=$1
outdir=exp_out/100_femnist_dp

if [ ! -d ${outdir} ];then
  mkdir -p ${outdir}
fi

echo "HPO starts..."

clips=(0.1)
epsilons=(0.1 0.5 10.)
mus=(0.1)
constants=(1. 2. 3.)

for ((iw=0; iw<${#clips[@]}; iw++ ))
do
  for ((ic=0; ic<${#constants[@]}; ic++ ))
  do
    for ((im=0; im<${#mus[@]}; im++ ))
    do
      for ((ie=0; ie<${#epsilons[@]}; ie++ ))
      do
        log=${outdir}/femnist_mu-${mus[$im]}_eps-${epsilons[$ie]}_const-${constants[$ic]}_wclip-${clips[$iw]}.log
        echo ${log}
        python federatedscope/main.py --cfg federatedscope/cv/baseline/fedavg_convnet2_on_femnist.yaml \
        device ${cudaid} \
        data.root /mnt/gaodawei.gdw/data/ \
        federate.sample_client_rate 0.5 \
        nbafl.use True \
        nbafl.mu ${mus[$im]} \
        nbafl.epsilon ${epsilons[$ie]} \
        nbafl.constant ${constants[$ic]} \
        nbafl.w_clip ${clips[$iw]} \
        >>${log} 2>&1
        python federatedscope/parse_exp_results.py --input ${log}
      done
    done
  done
done

echo "HPO Ends."
