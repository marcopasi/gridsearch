#!/bin/bash
#PBS -S /bin/bash
#PBS -N test2olivier
#PBS -P lbpa
#PBS -o outputJob.txt
#PBS -e errorJob.txt
#PBS -j oe
#PBS -q defaultq
#PBS -l walltime=03:00:00
#PBS -l select=1:ncpus=1
#PBS -M olivier.mauffret@lbpa.ens-cachan.fr
#PBS -m abe

pwd 

module purge
module load anaconda2/5.3
source activate chemex

cd $PBS_O_WORKDIR
pwd

python gridsearch.py
