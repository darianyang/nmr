#!/bin/csh

nmrPipe -in test.fid \
| nmrPipe -fn POLY -time \
| nmrPipe -fn SP -off 0.45 -end 0.97 -pow 2 -c 0.5  \
| nmrPipe -fn ZF -zf 1   \
| nmrPipe -fn FT -auto  \
| nmrPipe -fn PS -p0 -42 -p1 0  -di  \
#| nmrPipe -fn EXT -x1  -1ppm  -xn  4ppm  -sw  \
| nmrPipe -fn TP  \
| nmrPipe -fn POLY -auto  \
| nmrPipe -fn LP -after -ord 8 -pred 30  \
| nmrPipe -fn SP -off 0.35 -end 1 -pow 2 -c 1.0   \
| nmrPipe -fn ZF -zf 2   \
| nmrPipe -fn FT -auto \
| nmrPipe -fn PS -p0 0 -p1 0 -di \
| nmrPipe -fn CS -rs 10.1ppm  \
| nmrPipe -fn EXT -x1  14ppm  -xn  24ppm  -sw  \
| nmrPipe -out test.DAT -ov -verb
