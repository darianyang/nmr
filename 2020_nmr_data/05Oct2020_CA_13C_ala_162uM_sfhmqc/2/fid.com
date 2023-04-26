#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2773.33333333333 -dspfvs 20 -grpdly 67.9858856201172  \
  -xN              1024  -yN                80  \
  -xT               512  -yT                40  \
  -xMODE            DQD  -yMODE        Complex  \
  -xSW         7211.538  -ySW         1509.206  \
  -xOBS         600.231  -yOBS         150.931  \
  -xCAR           1.390  -yCAR          16.400  \
  -xLAB              1H  -yLAB             13C  \
  -ndim               2  -aq2D         Complex  \
  -out ./test.fid -verb -ov

sleep 5
