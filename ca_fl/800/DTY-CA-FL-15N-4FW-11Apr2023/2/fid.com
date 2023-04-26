#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 1560 -dspfvs 20 -grpdly 67.9867858886719  \
  -xN              2048  -yN               128  \
  -xT              1024  -yT                64  \
  -xMODE        Complex  -yMODE        Complex  \
  -xSW        12820.513  -ySW         2920.561  \
  -xOBS         800.304  -yOBS          81.103  \
  -xCAR           4.773  -yCAR         118.582  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D          States  \
  -out ./test.fid -verb -ov

sleep 5
