#!/bin/bash
# analyze multiple mixing time exsy experiments

# mixing times and respective data directories
TIMES=(2 5 10 15 25 35 50 75 100 200 600)
DIRS=(1 2 3 4 5 6 7 8 9 10 11)

#####################################
### loop each mixing time and dir ###
#####################################
for I in {0..10} ; do
#for I in {0..0} ; do
# go into appropriate directory
cd ${DIRS[$I]}

# convert topspin to nmrpipe format
cat << EOF > fid.com
#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 3936 -dspfvs 20 -grpdly 67.9842834472656  \
  -xN              2048  -yN                32  \
  -xT              1024  -yT                16  \
  -xMODE            DQD  -yMODE        Complex  \
  -xSW         5081.301  -ySW         1129.178  \
  -xOBS         564.611  -yOBS         564.611  \
  -xCAR        -133.870  -yCAR        -133.870  \
  -xLAB            19Fx  -yLAB            19Fy  \
  -ndim               2  -aq2D          States  \
  -out ./test.fid -verb -ov

sleep 1
EOF
csh fid.com

# process 2D exsy dataset in nmrpipe
cat << EOF > nmrPROC-exsy.com
#!/bin/csh

date
nmrPipe   -in  test.fid  \\
| nmrPipe -fn SP -off 0.55 -end 0.99 -pow 1 -c 0.5  \\
| nmrPipe -fn EM -lb 30 \\
| nmrPipe -fn LP \\
| nmrPipe -fn ZF -auto  \\
| nmrPipe -fn FT -auto \\
| nmrPipe -fn PS -p0 65 -p1 0.0 -verb -di \\
#| nmrPipe -fn POLY -auto -ord 2 \\
| nmrPipe -fn TP \\
| nmrPipe -fn SP -off 0.15 -end 0.99 -pow 1 -c 0.5 \\
| nmrPipe -fn EM -lb 30 \\
| nmrPipe -fn LP \\
| nmrPipe -fn ZF -zf 4 \\
| nmrPipe -fn FT -alt \\
| nmrPipe -fn PS -p0 -2 -p1 -45 -verb -di \\
#| nmrPipe -fn POLY -auto -ord 0 \\
| nmrPipe -fn TP \\
-out test.DAT -ov
EOF
csh nmrPROC-exsy.com

# convert processed spectrum to ucsf format for use in sparky or ccpnmr
pipe2ucsf test.DAT ${TIMES[$I]}ms_7F_exsy.ucsf

# return to parent directory
cd ..
######################
### finishing loop ###
######################
done
