This directory contains the following files for augmenting an ADP:
in.base:    Lammps input file for generating the atomic data
Ti2.eam.fs: Ti EAM potential used for Lammps reference calcs. Mendelev:10.1063/1.4964654
Ti.adp:     Ti adp potential. Created using Lammps data in Potfit 
in.param:   Parameter file called by in.base
in.pot:     Lammps file called by in.base which reruns the calculations using the ADP instead of the reference (EAM) potential
lammps.dat: File called by in.base containg the relevant data for the atomic system (atom type, number, location, etc.)
log.lammps: Standard Lammps log file. Changes with subsequent Lammps runs
eval.py:    Python script for post-processing data/ANN creation
in.testpy:  Test Lammps input file for debugging eval.py without having to rerun actual Lammps calcs
testenv.yml:Yaml file containg Miniconda virtual env params used
slurm:      Slurm file (not needed when running locally)
ecoh1000:   Directory with data generated from Lammps calc
adp1000:    Directory with data generated from Lammps calc
eam1000:    Directory with data generated from Lammps calc
