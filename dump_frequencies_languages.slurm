#!/bin/bash
#SBATCH --job-name=dump_freq_lang
#SBATCH --output=logs/dump_freq_lang_%A_%a.log
#SBATCH --time=2:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --array=1-111

module load anaconda3/2024.6
conda activate /scratch/network/ks2663/COLLAB/envs/tokenizer-attack

cd /scratch/network/ks2663/COLLAB/cos484-tokenizer-attack

LANGS=(af am ar as az ba be bg bn bo bpy br ca ce ceb ckb cs cv cy da de dv el en eo es et eu fa fi fr fy ga gl gom gu he hi hr hu hy id is it ja jbo ka kk km kn ko ky la lb lo lt lv mg mhr min mk ml mn mr ms mt my nds ne new nl nn no oc or os pa pl pms pnb ps pt ro ru sa sah sd sh si sk sl sq sr sv ta te tg th tk tl tr tt ug uk ur uz vi vo xmf yi zh)

LANG=${LANGS[$SLURM_ARRAY_TASK_ID-1]}
CORPUS_DIR=/scratch/network/ks2663/COLLAB/oscar-corpus/processed

for n in 5 10 30 111; do
    for test_id in $(ls experiments/mixed_languages/n_${n}/); do
        experiment_dir=experiments/mixed_languages/n_${n}/${test_id}
        if [ ! -f "${experiment_dir}/${LANG}/all_pair_counts.json" ]; then
            python -m dump_frequencies \
                --experiment_dir $experiment_dir \
                --lang_code $LANG \
                --corpus_dir $CORPUS_DIR
        fi
    done
done
