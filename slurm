#!/bin/bash
# Set job parameters
#SBATCH -p Lewis
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1  # used for MPI codes, otherwise leave at '1'
#SBATCH -J  lammps
#SBATCH -o  b.o%J
#SBATCH -e  b.e%J
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sjokdd@mail.umkc.edu
##DISABLED
#SBATCH --mem-per-cpu=5G

# Start MPI job
#module load mpich/mpich-3.2-intel
 # CHANGE THIS!!!!!
module purge
module load rss/rss-2020
module load lammps/lammps-31Mar17
srun lmp_g++_openmpi <in.energy >>lammps.out
