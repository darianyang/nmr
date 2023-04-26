#!/bin/csh

nmrPipe -in test.fid \
#| nmrPipe -fn poly -time \
| nmrPipe -fn SP -off 0.5 -end 0.97 -pow 2 -c 0.5  \
#| nmrPipe -fn EM -lb 20.0     \
| nmrPipe -fn ZF -auto   \
| nmrPipe -fn FT -auto  \
| nmrPipe -fn PS -p0 67 -p1 0  -di  \
| nmrPipe -fn EXT -x1  0.5ppm  -xn  2ppm  -sw  \
| nmrPipe -fn TP  \
#| nmrPipe -fn POLY -auto -ord 0   \
#| nmrPipe -fn LP -after -ord 8 -pred 30  \
| nmrPipe -fn SP -off 0.38 -end 1 -pow 2 -c 1.0   \
| nmrPipe -fn ZF -auto   \
| nmrPipe -fn FT -auto \
| nmrPipe -fn PS -p0 -4 -p1 0 -di  \
| nmrPipe -fn CS -rs 4.95ppm  \
#| nmrPipe -fn REV -sw  \
#| nmrPipe -fn EXT -x1  17ppm  -xn  26ppm  -sw  \
| nmrPipe -out test.DAT -ov -verb
