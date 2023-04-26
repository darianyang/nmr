#!/bin/csh

nmrPipe -in test.fid \
| nmrPipe -fn POLY -auto \
| nmrPipe -fn SP -off 0.45 -end 0.98 -pow 2 -c 0.5 \
| nmrPipe -fn FT -auto        \
#| nmrPipe -fn ZF -size 256    \
| nmrPipe -fn PS -p0 -25.0 -p1 0.0 -di  \
#| nmrPipe -fn EXT -x1  -1ppm  -xn  4ppm  -sw  \
| nmrPipe -fn TP         \
#| nmrPipe -fn ZF -zf 2   \
| nmrPipe -fn SP -off 0.45 -end 1.0 -pow 2 -c 1.0 \
| nmrPipe -fn FT -real   \
#| nmrPipe -fn LP -after -ord 8 -pred 30  \
| nmrPipe -fn PS -p0 89  -p1 0.0  \
| nmrPipe -fn CS -rs 10.1ppm  \
#| nmrPipe -fn REV -di    \
#| nmrPipe -fn EXT -x1  16ppm  -xn  22ppm  -sw  \
| nmrPipe -fn POLY -auto \
| nmrPipe -out test.DAT -ov -verb
