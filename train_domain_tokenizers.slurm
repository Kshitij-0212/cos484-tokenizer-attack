#!/bin/bash
#SBATCH --job-name=train_domain
#SBATCH --output=/scratch/network/cam19/cos484-tokenizer-attack/logs/train_domain_%A_%a.log
#SBATCH --time=8:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --array=1-100%5
module load anaconda3/2025.12
conda activate tokenizer-attack
cd /scratch/network/cam19/cos484-tokenizer-attack
python -m train_mixed_tokenizer \
    --output_dir experiments/mixed_domains/n_4/${SLURM_ARRAY_TASK_ID} \
    --num_categories 4 \
    --corpus_dir /scratch/network/ks2663/COLLAB/domain-corpus
