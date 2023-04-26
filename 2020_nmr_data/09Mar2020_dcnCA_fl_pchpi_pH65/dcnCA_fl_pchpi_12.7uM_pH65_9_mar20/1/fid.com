#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 1232 -dspfvs 20 -grpdly 67.9882507324219  \
  -xN              2048  -yN               160  \
  -xT              1024  -yT                80  \
  -xMODE            DQD  -yMODE        Complex  \
  -xSW        16233.766  -ySW         2000.000  \
  -xOBS         900.224  -yOBS          91.229  \
  -xCAR           4.773  -yCAR         118.265  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D         Complex  \
  -out ./test.fid -verb -ov

sleep 5
