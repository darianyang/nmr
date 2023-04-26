#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 2376 -dspfvs 20 -grpdly 67.9872589111328  \
  -xN              1024  -yN               128  \
  -xT               512  -yT                64  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         8417.508  -ySW         5279.831  \
  -xOBS         600.233  -yOBS         150.931  \
  -xCAR           4.773  -yCAR          20.737  \
  -xLAB              1H  -yLAB             13C  \
  -ndim               2  -aq2D         Complex  \
  -out ./test.fid -verb -ov

sleep 5
