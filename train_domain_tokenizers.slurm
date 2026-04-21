#!/bin/bash
#SBATCH --job-name=train_domain
#SBATCH --output=logs/train_domain_%A_%a.log
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --array=1-100

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/ks2663/COLLAB/cos484-tokenizer-attack

python -m train_mixed_tokenizer \
    --output_dir experiments/mixed_domains/n_4/${SLURM_ARRAY_TASK_ID} \
    --num_categories 4 \
    --corpus_dir /scratch/network/ks2663/COLLAB/domain-corpus
