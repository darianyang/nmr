#!/bin/csh

nmrPipe -in test.fid \
#| nmrPipe -fn POLY -auto    \
| nmrPipe -fn SP -off 0.02 -end 0.98 -pow 1 -c 0.7         \
| nmrPipe -fn EM -lb 20.0     \
| nmrPipe -fn FT -auto         \
| nmrPipe -fn PS -p0 -40.0 -p1 -30.0 -di         \
#| nmrPipe -fn EXT -x1 12.6ppm -xn 5.5ppm -sw -round   \
| nmrPipe -fn TP          \
| nmrPipe -fn ZF -auto         \
| nmrPipe -fn SP -off 0.3 -end 0.98 -pow 1 -c 0.5         \
| nmrPipe -fn FT -real         \
| nmrPipe -fn PS -p0 -72.0 -p1 149.0           \
| nmrPipe -fn REV -di  \
| nmrPipe -fn CS -rs 10.1ppm  \
| nmrPipe -fn REV -di   \
#| nmrPipe -fn TP     \
#| nmrPipe -fn POLY -auto  \
| nmrPipe -out test.DAT -ov -verb
