#!/bin/csh

nmrPipe -in test.fid \
| nmrPipe -fn poly -time \
| nmrPipe -fn SP -off 0.5 -end 0.97 -pow 2 -c 0.5  \
| nmrPipe -fn ZF -auto   \
| nmrPipe -fn FT -auto  \
| nmrPipe -fn PS -p0 102 -p1 0  -di  \
| nmrPipe -fn EXT -x1  -1ppm  -xn  4ppm  -sw  \
| nmrPipe -fn TP  \
| nmrPipe -fn LP -after -ord 8 -pred 30  \
| nmrPipe -fn SP -off 0.45 -end 1 -pow 2 -c 1.0   \
| nmrPipe -fn ZF -auto   \
| nmrPipe -fn FT -auto \
| nmrPipe -fn PS -p0 -117 -p1 0  -di  \
| nmrPipe -fn CS -rs 30.1ppm  \
| nmrPipe -fn REV -sw  \
| nmrPipe -out test.DAT -ov -verb
