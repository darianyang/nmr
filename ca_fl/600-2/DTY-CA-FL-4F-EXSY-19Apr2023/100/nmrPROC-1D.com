#!/bin/csh


date

nmrPipe   -in  test.fid                         	\
#| nmrPipe -fn SOL                               	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn EM -lb 20                  \
| nmrPipe -fn FT -auto					\
| nmrPipe -fn PS -p0 -175.0 -p1 240.0  -verb  -di     	\
#| nmrPipe -fn PS -p0 -111.0 -p1 100.0  -verb  -di     	\
#| nmrPipe -fn PS -p0 -180.0 -p1 239.0  -verb  -di     	\
| nmrPipe -fn POLY -auto -ord 3	                	\
-out test.DAT -ov\


