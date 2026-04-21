import os
import json
from pathlib import Path
from tqdm import tqdm

data_dir = Path('/scratch/network/ks2663/COLLAB/redpajama-corpus/arxiv')
output_dir = Path('/scratch/network/ks2663/COLLAB/redpajama-corpus/processed/arxiv')
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / 'arxiv_text.txt'
bytes_written = 0

with open(output_file, 'w') as fo:
    for f in tqdm(os.listdir(data_dir)):
        if not f.endswith('.jsonl'):
            continue
        with open(data_dir / f) as fin:
            for line in fin:
                try:
                    doc = json.loads(line)
                    text = doc.get('text', '')
                    fo.write(text + '\n\n')
                    bytes_written += len(text.encode('utf-8'))
                except:
                    continue

print(f'Done! Written {bytes_written/1e9:.2f}GB to {output_file}')
