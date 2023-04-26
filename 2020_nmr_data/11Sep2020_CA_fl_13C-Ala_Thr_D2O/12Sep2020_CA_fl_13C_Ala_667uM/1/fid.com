#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -noaswap -AMX -decim 16 -dspfvs 12 -grpdly -1  \
  -xN              1024  -yN               160  \
  -xT               512  -yT                80  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         9765.625  -ySW        12330.456  \
  -xOBS         700.113  -yOBS         176.046  \
  -xCAR           4.773  -yCAR          20.740  \
  -xLAB              1H  -yLAB             13C  \
  -ndim               2  -aq2D         Complex  \
  -out ./test.fid -verb -ov

sleep 5
