#!/bin/bash

for I in {100..106}; do
    cd $I
    bash ../proc_1d.sh &&
    cd ..
done
