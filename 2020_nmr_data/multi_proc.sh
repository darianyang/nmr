#!/bin/bash
# process multiple experiments
# takes 2 args
# 1 = target dir to copy and proc into
# 2 = conc of target dir, for naming scheme ucsf

# source scripts
source=$HOME/Data/nmr_data/03Oct2020_CA_13C_ala_20.2uM_sfhmqc/31

# target directory is arg 1
target = $1

# move proc files
cp -v $source/{nmrPROC-sfhmqc.com,fid.com} $1 &&

# go to target dir
cd $1

# run proc and make final ucsf
./fid.com &&
./nmrPROC-sfhmqc.com &&

# for ucsf file name, arg 2 is 
pipe2ucsf test.DAT CA_13C_ala_${2}uM_sfhmqc_VF.ucsf &&

# return to parent dir
cd $HOME/Data/nmr_data
