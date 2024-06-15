#!/bin/bash
#
#SBATCH --partition=gpu_a100
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --output=jobname_%J_stdout.txt
#SBATCH --error=jobname_%J_stderr.txt
#SBATCH --time=30:00
#SBATCH --job-name=mjb-fifi
#SBATCH --mail-user=mjbeattie@ou.edu
#SBATCH --mail-type=ALL
#SBATCH --chdir=/scratch/mjbeattie/fifi-project/seattle-service-requests

module load Python/3.10.8-GCCcore-12.2.0
module load cuDNN/8.6.0.163-CUDA-11.8.0
source $HOME/fifiproj/fifivenv/bin/activate
python fifi_reclass_torch.py --blocknum=0 --startrow=0 --endrow=5000

deactivate
module purge
