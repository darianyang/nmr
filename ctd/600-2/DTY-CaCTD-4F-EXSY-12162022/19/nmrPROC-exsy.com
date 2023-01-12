#!/bin/csh

date
nmrPipe   -in  test.fid  | nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5  | nmrPipe -fn ZF -auto  | nmrPipe -fn EM -lb 40 | nmrPipe -fn FT -auto | nmrPipe -fn PS -p0 70 -p1 0.0 -verb -di | nmrPipe -fn POLY -auto -ord 1.5 | nmrPipe -fn TP | nmrPipe -fn SP -off 0.15 -end 0.99 -pow 1 -c 0.5 | nmrPipe -fn EM -lb 40 | nmrPipe -fn LP | nmrPipe -fn ZF -zf 4 | nmrPipe -fn FT -alt | nmrPipe -fn PS -p0 -32 -p1 55 -verb -di | nmrPipe -fn TP -out test.DAT -ov
