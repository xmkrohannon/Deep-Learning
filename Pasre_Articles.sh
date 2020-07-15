#!/bin/bash
#PBS -k o
#PBS -l nodes=1:ppn=16,walltime=12:00:00,vmem=100gb
#PBS -M amkrug@iu.edu
#PBS -m e
#PBS -N PubMed Parse
#PBS -j oe

cd /N/dc2/projects/MAMMALEXP/Deep_Learn/

module unload python
module load python/3.6.8

python Article_Parser.py
