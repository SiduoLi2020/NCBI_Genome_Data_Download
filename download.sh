#!/bin/bash
case "$1" in
    -h|--help|?)
    echo "Usage:"
    echo "1st arg: IDtable file from NCBI Assembly"
    echo "2st arg: output file folder name" 
    echo "3st arg: Database(GenBank--GB, Refseq--Ref)"
    echo "Example: bash download.sh IDtable_Mycobacteroides_abscessus.txt Mycobacteroides_abscessus Ref"
    exit 0 
;;
esac

if [ ! -n "$1" ]; then
    echo "pls input 1st arg"
    exit
fi


if [ ! -n "$2" ]; then
    echo "pls input 2st arg"
    exit
fi

if [ ! -n "$3" ]; then
    echo "pls input 3st arg"
    exit
fi


python3 NCBIGenomeDownload.py -i $1 -n $2 -t $3

sleep 1s
echo download data from NCBI

while read line
do 
    rsync --copy-links --recursive --times --verbose $line $2_$3/
done < $2_$3_Context.txt