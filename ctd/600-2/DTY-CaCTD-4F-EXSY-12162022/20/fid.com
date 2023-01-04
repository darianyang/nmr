#!/bin/csh

bruk2pipe -in ./ser   -bad 0.0 -ext -aswap -AMX -decim 3936 -dspfvs 20 -grpdly 67.9842834472656    -xN              2048  -yN                32    -xT              1024  -yT                16    -xMODE        Complex  -yMODE        Complex    -xSW         5081.301  -ySW         1129.178    -xOBS         564.615  -yOBS         564.615    -xCAR        -125.540  -yCAR        -125.540    -xLAB            19Fx  -yLAB            19Fy    -ndim               2  -aq2D          States    -out ./test.fid -verb -ov

sleep 5
