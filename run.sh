#!/bin/bash

if [ ! -s chr21.fa.fai ]
then
	echo "Index .fai not found. Indexing chr21.fa"
	samtools faidx /data/hg38.fa
fi

for f in $(ls /data/*.bam); do
	echo "cd /opt/reditools2.0/src/cineca && python reditools.py -f /data/$f -r /data/hg38.fa -o $f-output.csv &> $f_std_out.txt"
	cd /opt/reditools2.0/src/cineca && python reditools.py -f /data/$f -r /data/hg38.fa -o $f-output.csv &> $f_std_out.txt &
done;
