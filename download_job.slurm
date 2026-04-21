#!/bin/bash
#SBATCH --job-name=oscar_download
#SBATCH --output=download_%j.log
#SBATCH --time=12:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/ks2663/COLLAB/cos484-tokenizer-attack
python download_oscar.py
