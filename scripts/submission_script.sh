#!/bin/bash\n'
#SBATCH --job-name=cancer_sims
#SBATCH --error=logs/slurm-%A-%a.err
#SBATCH --output=logs/slurm-%A-%a.out
#SBATCH --mem=10G
#SBATCH --time=03:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --array=1-100
