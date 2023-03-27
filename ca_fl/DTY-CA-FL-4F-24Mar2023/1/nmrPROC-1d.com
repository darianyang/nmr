#!/bin/csh

date
nmrPipe   -in  test.fid                         	\
#| nmrPipe -fn SOL                               	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn EM -lb 20                  \
| nmrPipe -fn FT -auto					\
| nmrPipe -fn PS -p0 -111.0 -p1 100.0  -verb  -di     	\
#| nmrPipe -fn EXT -left -sw          \
#| nmrPipe -fn POLY -auto -ord 1	                	\
-out test.DAT -ov
