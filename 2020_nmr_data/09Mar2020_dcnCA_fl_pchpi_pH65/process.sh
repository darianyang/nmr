#!/bin/bash
# process all conc for dcnCA_fl_pchpi_XuM_pH65_9_mar20
# process.sh

conc=(6.96 12.7 51 102 306 815 1630)

wd="$HOME/NMR_Data_AMG"

for i in ${conc[@]}; do

	cd $wd/dcnCA_fl_pchpi_${i}uM_pH65_9_mar20/1
	cp -v $wd/dcnCA_fl_pchpi_6.96uM_pH65_9_mar20/1/{fid.com,nmrPROC-hsqc.com} . &&
	fid.com && nmrPROC-hsqc.com &&
	#nmrDraw test.DAT &&
	pipe2ucsf test.DAT hsqc-CA-fl-${i}uM-pH65.ucsf

done
