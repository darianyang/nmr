#!/bin/bash
# parses through a topspin experiment dir
# makes readme of all sub directories/experiment titles
# assumes that current path is within the desired topspin exp dir


# begin readme string
CMD="###$(pwd)  \n\n"
CMD="$CMD README Created: $(date) \n\n"

# loop all directories (e.g. expno 1/2/3/...)
for I in */ ; do
    CMD="$CMD EXP $I \n"
    # loop sub experiments
    for J in ${I}pdata/*/ ; do
        # if the title file exists
        if [ -f ${J}title ] ; then
            title=$(cat ${J}title)
            CMD="$CMD \t SUBEXP $J \n\t$title \n\n"
        fi
    done
done

echo -e $CMD > README.txt
