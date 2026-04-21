#!/bin/bash
#SBATCH --job-name=train_tok
#SBATCH --output=logs/train_tok_%A_%a.log
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --array=1-100

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/ks2663/COLLAB/cos484-tokenizer-attack

for n in 5 10 30 111; do
    python -m train_mixed_tokenizer \
        --output_dir experiments/mixed_languages/n_${n}/${SLURM_ARRAY_TASK_ID} \
        --num_categories $n \
        --corpus_dir /scratch/network/ks2663/COLLAB/oscar-corpus/processed
done
