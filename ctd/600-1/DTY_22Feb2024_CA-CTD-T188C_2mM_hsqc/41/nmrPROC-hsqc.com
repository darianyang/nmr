#!/bin/csh

date
nmrPipe   -in  test.fid                         	\
| nmrPipe -fn SOL                               	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn FT -auto					\
| nmrPipe -fn PS -p0 -101 -p1 0.0  -verb  -di     	\
| nmrPipe -fn EXT -left -sw          \
| nmrPipe -fn POLY -auto -ord 1	                	\
| nmrPipe -fn TP                                	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5       \
| nmrPipe -fn ZF -auto	                        	\
#| nmrPipe -fn FT -alt                          	\
| nmrPipe -fn FT -auto                          	\
| nmrPipe -fn PS -p0 -89 -p1 0.0 -verb -di    		\
| nmrPipe -fn POLY -auto -ord 1			\
#| nmrPipe -fn CS -ls 18.1ppm			\
-out test.DAT -ov -verb
