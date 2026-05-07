"""
Merge-Order Shuffle Defense

Perturbs BPE merge order within a frequency-similarity window of size epsilon,
introducing noise that degrades the LP attack's ability to recover true mixture.
"""

import json
import random
import copy
from pathlib import Path
import numpy as np


def load_merges(merges_file):
    """Load merges from merges.txt"""
    merges = []
    with open(merges_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                merges.append(tuple(parts))
    return merges


def shuffle_within_window(merges, epsilon):
    """
    Shuffle merges within a window of size epsilon.
    For each merge, it can be swapped with any merge within epsilon positions.
    """
    n = len(merges)
    shuffled = list(merges)
    
    for i in range(n):
        # Find window bounds
        low = max(0, i - epsilon)
        high = min(n - 1, i + epsilon)
        # Swap with random position in window
        j = random.randint(low, high)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    
    return shuffled


def save_merges(merges, output_file):
    """Save merges to merges.txt format"""
    with open(output_file, 'w') as f:
        f.write('#version: 0.2\n')
        for m in merges:
            f.write(f'{m[0]} {m[1]}\n')


def create_shuffled_tokenizer(experiment_dir, epsilon, output_dir):
    """
    Create a shuffled version of a tokenizer with window size epsilon.
    Copies all files from experiment_dir, replacing merges.txt with shuffled version.
    Also updates tokenizer.json to reflect the shuffled merge order.
    """
    import shutil, json
    experiment_dir = Path(experiment_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files except merges.txt and tokenizer.json
    for f in experiment_dir.iterdir():
        if f.name not in ['merges.txt', 'tokenizer.json'] and f.is_file():
            shutil.copy2(f, output_dir / f.name)
    
    # Load, shuffle, and save merges
    merges = load_merges(experiment_dir / 'merges.txt')
    shuffled = shuffle_within_window(merges, epsilon)
    save_merges(shuffled, output_dir / 'merges.txt')
    
    # Update tokenizer.json with shuffled merges
    tok_file = experiment_dir / 'tokenizer.json'
    if tok_file.exists():
        with open(tok_file) as f:
            tok = json.load(f)
        tok['model']['merges'] = [f'{m[0]} {m[1]}' for m in shuffled]
        with open(output_dir / 'tokenizer.json', 'w') as f:
            json.dump(tok, f)
    
    return output_dir


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_dir', type=str, required=True)
    parser.add_argument('--epsilon', type=int, required=True, 
                        help='Window size for shuffle')
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    create_shuffled_tokenizer(args.experiment_dir, args.epsilon, args.output_dir)
    print(f'Created shuffled tokenizer with epsilon={args.epsilon} at {args.output_dir}')


def update_tokenizer_json(experiment_dir, shuffled_merges):
    """Update the merges inside tokenizer.json to match shuffled merges.txt"""
    import json
    tok_file = Path(experiment_dir) / 'tokenizer.json'
    if not tok_file.exists():
        return
    with open(tok_file) as f:
        tok = json.load(f)
    # Update merges in tokenizer.json
    tok['model']['merges'] = [f'{m[0]} {m[1]}' for m in shuffled_merges]
    with open(tok_file, 'w') as f:
        json.dump(tok, f)
