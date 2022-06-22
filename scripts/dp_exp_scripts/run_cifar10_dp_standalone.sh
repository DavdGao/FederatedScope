set -e

cudaid=$1
outdir=exp_out/cifar10_nbafl

if [ ! -d ${outdir} ];then
  mkdir -p ${outdir}
fi

echo "HPO starts..."

lrs=(0.5 0.25 0.1 1.)
clips=(0.1 0.2 0.3)
epsilons=(1. 5. 10. 50. 100.)
mus=(0.01 0.1 1.)
constants=(1. 2. 3.)

for (( i=0; i<${#lrs[@]}; i++ ))
do
    for ((iw=0; iw<${#clips[@]}; iw++ ))
    do
        for ((ie=0; ie<${#epsilons[@]}; ie++ ))
        do
            for ((im=0; im<${#mus[@]}; im++ ))
            do
                for ((ic=0; ic<${#constants[@]}; ic++ ))
                do
                    log=${outdir}/convnet2_clip_${clips[$iw]}_eps_${epsilons[$ie]}_mu_${mus[$im]}_const_${constants[$ic]}.log
                    for k in {1..3}
                    do
                      python federatedscope/main.py --cfg federatedscope/cv/baseline/fedavg_convnet2_on_cifar10.yaml \
                      device ${cudaid} \
                      nbafl.use True \
                      data.root /mnt/gaodawei.gdw/data/ \
                      optimizer.lr ${lrs[$i]} \
                      nbafl.mu ${mus[$im]} \
                      nbafl.epsilon ${epsilons[$ie]} \
                      nbafl.constant ${constants[$ic]} \
                      nbafl.w_clip ${clips[$iw]} \
                      seed $k >>${log} 2>&1
                    done
                    python federatedscope/parse_ex_results.py --input ${log}
                done
            done
        done
    done
done

echo "Ends."

