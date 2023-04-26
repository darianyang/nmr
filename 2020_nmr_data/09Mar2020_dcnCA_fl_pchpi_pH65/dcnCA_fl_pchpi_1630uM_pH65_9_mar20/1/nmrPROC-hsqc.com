#!/bin/csh

date
nmrPipe   -in  test.fid                         	\
| nmrPipe -fn SOL                               	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5	\
| nmrPipe -fn ZF -auto					\
| nmrPipe -fn FT -verb					\
| nmrPipe -fn PS -p0 -31 -p1 0.0  -verb  -di     	\
| nmrPipe -fn EXT -left -sw           		        \
| nmrPipe -fn POLY -auto -ord 2	                	\
| nmrPipe -fn TP                                	\
| nmrPipe -fn SP -off 0.45 -end 0.99 -pow 1 -c 0.5      \
| nmrPipe -fn ZF -size -auto	                       	\
| nmrPipe -fn FT -verb                          	\
| nmrPipe -fn PS -p0 0 -p1 0.0 -verb -di    		\
| nmrPipe -fn POLY -auto -ord 1	           		\
| nmrPipe -fn CS -ls 33.1ppm				\
| nmrPipe -fn TP                                	\
-out test.DAT -ov -verb
