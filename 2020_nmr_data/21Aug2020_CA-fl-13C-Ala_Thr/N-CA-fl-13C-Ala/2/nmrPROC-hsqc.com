#!/bin/csh

date
nmrPipe   -in  test.fid                         	\
| nmrPipe -fn SOL                               	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 2 -c 0.5	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn FT -verb					\
| nmrPipe -fn PS -p0 80 -p1 0.0  -verb  -di     	\
| nmrPipe  -fn EXT -left -sw          \
| nmrPipe -fn POLY -auto -ord 2	                	\
| nmrPipe -fn TP                                	\
| nmrPipe -fn SP -off 0.45 -end 1.0 -pow 2 -c 1.0       \
| nmrPipe -fn ZF -size 1024	                        	\
| nmrPipe -fn FT -verb                          	\
| nmrPipe -fn PS -p0 86.4 -p1 0.0 -verb -di    		\
| nmrPipe -fn POLY -auto -ord 1			\
| nmrPipe -fn TP                                	\
-out test.DAT -ov
