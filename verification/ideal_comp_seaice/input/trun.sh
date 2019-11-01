#!/bin/bash
#SBATCH -J trun
#SBATCH -p smp
#SBATCH -n 10
#SBATCH --ntasks-per-node=32
#SBATCH -t 04:00:00
#SBATCH -e ./err_trun_ell.txt
#SBATCH -o ./out_trun_ell.txt
# #SBATCH --mail-user=damien.ringeisen@awi.de --mail-type=ALL
# list of hosts that you are running on
hostlist=$(scontrol show hostnames | tr '\n' ',' | rev | cut -c 2- | rev)
echo "hosts: $hostlist"
umask 022
#
# load your modules with "module load ..."

module purge # 
module load intel.compiler
module load intel.mpi 
module load netcdf/4.4.1.1_intel_mpi
export MPI_INC_DIR=${I_MPI_ROOT}/include64

# maximum possible stacksize
ulimit -s unlimited
# very important if you want to run on more than one node!!!
cd ${SLURM_SUBMIT_DIR}
srun  ../build/mitgcmuv

