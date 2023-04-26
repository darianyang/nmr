#!/bin/bash

nl=$'\n'

# make conversion script from topspin to nmrpipe
cat << EOF > fid.com
#!/bin/csh
$nl
bruk2pipe -in ./fid \\
  -bad 0.0 -ext -aswap -AMX -decim 704 -dspfvs 20 -grpdly 67.9838562011719  \\
  -xN             16384  \\
  -xT              8192  \\
  -xMODE        Complex  \\
  -xSW        28409.091  \\
  -xOBS         564.617  \\
  -xCAR        -123.000  \\
  -xLAB             19F  \\
  -ndim               1  \\
  -out ./test.fid -verb -ov\\
$nl
$nl
sleep 2
EOF
# run conversion script
csh fid.com

# make script to process 1D using nmrpipe
cat << EOF > nmrPROC-1D.com
#!/bin/csh
$nl
date$nl
nmrPipe   -in  test.fid                         	\\
#| nmrPipe -fn SOL                               	\\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5	\\
| nmrPipe -fn ZF -auto					\\
| nmrPipe -fn EM -lb 20                  \\
| nmrPipe -fn FT -auto					\\
| nmrPipe -fn PS -p0 -175.0 -p1 240.0  -verb  -di     	\\
#| nmrPipe -fn PS -p0 -111.0 -p1 100.0  -verb  -di     	\\
#| nmrPipe -fn PS -p0 -180.0 -p1 239.0  -verb  -di     	\\
| nmrPipe -fn POLY -auto -ord 3	                	\\
-out test.DAT -ov\\
$nl
EOF

# run proc script
csh nmrPROC-1D.com
