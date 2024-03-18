#!/bin/bash
# run multiple dir proc

#EXPS=(1 2 3 4 5 6 10)
EXPS=(2 3 4 5 6 10)

for EXP in ${EXPS[@]} ; do
    cd $EXP

    cp ../fid.com . &&
    ./fid.com

    cp ../nmrPROC-hsqc.com . &&
    ./nmrPROC-hsqc.com

    cd ../
done
