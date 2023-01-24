#!/bin/csh

date
nmrPipe   -in  test.fid  \
| nmrPipe -fn SP -off 0.55 -end 0.99 -pow 1 -c 0.5  \
| nmrPipe -fn EM -lb 30 \
| nmrPipe -fn LP \
| nmrPipe -fn ZF -auto  \
| nmrPipe -fn FT -auto \
| nmrPipe -fn PS -p0 65 -p1 0.0 -verb -di \
#| nmrPipe -fn POLY -auto -ord 2 \
| nmrPipe -fn TP \
| nmrPipe -fn SP -off 0.15 -end 0.99 -pow 1 -c 0.5 \
| nmrPipe -fn EM -lb 30 \
| nmrPipe -fn LP \
| nmrPipe -fn ZF -zf 4 \
| nmrPipe -fn FT -alt \
| nmrPipe -fn PS -p0 -2 -p1 -45 -verb -di \
#| nmrPipe -fn POLY -auto -ord 0 \
| nmrPipe -fn TP \
-out test.DAT -ov
