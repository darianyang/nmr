#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -ext -aswap -AMX -decim 1848 -dspfvs 20 -grpdly 67.9869537353516  \
  -xN              2048  -yN               128  \
  -xT              1024  -yT                64  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW        10822.511  -ySW         2190.101  \
  -xOBS         600.233  -yOBS          60.828  \
  -xCAR           4.773  -yCAR         118.584  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D         Complex  \
  -out ./test.fid -verb -ov

sleep 5
