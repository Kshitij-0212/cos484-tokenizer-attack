#!/bin/bash
#SBATCH --job-name=dump_freq_domain
#SBATCH --output=/scratch/network/cam19/cos484-tokenizer-attack/logs/dump_freq_domain_%A_%a.log
#SBATCH --time=8:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4
#SBATCH --array=1-4

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/cam19/cos484-tokenizer-attack

CATEGORIES=(academic code web wikipedia)
CATEGORY=${CATEGORIES[$SLURM_ARRAY_TASK_ID-1]}
CORPUS_DIR=/scratch/network/ks2663/COLLAB/domain-corpus

for test_id in $(ls /scratch/network/cam19/cos484-tokenizer-attack/experiments/mixed_domains/n_4/); do
    experiment_dir=/scratch/network/cam19/cos484-tokenizer-attack/experiments/mixed_domains/n_4/${test_id}
    if [ ! -f "${experiment_dir}/${CATEGORY}/all_pair_counts.json" ]; then
        python -m dump_frequencies \
            --experiment_dir $experiment_dir \
            --lang_code $CATEGORY \
            --corpus_dir $CORPUS_DIR
    fi
done