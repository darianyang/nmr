#!/bin/csh


bruk2pipe -in ./fid \
  -bad 0.0 -ext -aswap -AMX -decim 704 -dspfvs 20 -grpdly 67.9838562011719  \
  -xN             16384  \
  -xT              8192  \
  -xMODE        Complex  \
  -xSW        28409.091  \
  -xOBS         564.617  \
  -xCAR        -123.000  \
  -xLAB             19F  \
  -ndim               1  \
  -out ./test.fid -verb -ov\




sleep 2
