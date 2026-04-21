#!/bin/bash
#SBATCH --job-name=retrain_17
#SBATCH --output=logs/retrain_17.log
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/ks2663/COLLAB/cos484-tokenizer-attack

python -m train_mixed_tokenizer \
    --output_dir experiments/mixed_languages/n_111/17 \
    --num_categories 111 \
    --corpus_dir /scratch/network/ks2663/COLLAB/oscar-corpus/processed
