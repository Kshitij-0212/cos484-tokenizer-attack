import os
import json
import zstandard as zstd
from pathlib import Path
from tqdm import tqdm

data_dir = Path('/scratch/network/ks2663/COLLAB/redpajama-corpus/common_crawl')
output_dir = Path('/scratch/network/ks2663/COLLAB/redpajama-corpus/processed/web')
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / 'web_text.txt'
progress_file = output_dir / 'progress.txt'

# Load already processed files
processed = set()
if progress_file.exists():
    with open(progress_file) as f:
        processed = set(f.read().splitlines())
    print(f'Resuming: {len(processed)} files already processed', flush=True)

# Find all zst files
all_files = sorted([
    str(p) for p in Path(data_dir).rglob('*.zst')
])
print(f'Found {len(all_files)} files total, {len(all_files) - len(processed)} remaining', flush=True)

bytes_written = 0
mode = 'a' if processed else 'w'

with open(output_file, mode) as fo:
    for filepath in tqdm(all_files):
        if filepath in processed:
            print(f'Skipping already processed: {filepath}', flush=True)
            continue

        print(f'Processing {filepath}...', flush=True)
        try:
            with open(filepath, 'rb') as fin:
                dctx = zstd.ZstdDecompressor()
                stream = dctx.stream_reader(fin)
                buffer = b""
                while True:
                    chunk = stream.read(65536)
                    if not chunk:
                        break
                    buffer += chunk
                    lines = buffer.split(b'\n')
                    buffer = lines[-1]
                    for line in lines[:-1]:
                        if not line.strip():
                            continue
                        try:
                            doc = json.loads(line)
                            text = doc.get('text', '')
                            fo.write(text + '\n\n')
                            bytes_written += len(text.encode('utf-8'))
                        except:
                            continue

            # Mark as processed and delete raw file
            with open(progress_file, 'a') as pf:
                pf.write(filepath + '\n')
            os.remove(filepath)
            print(f'Done {filepath}, total so far: {bytes_written/1e9:.2f}GB', flush=True)

        except Exception as e:
            print(f'ERROR on {filepath}: {e}', flush=True)
            continue

print(f'All done! Written {bytes_written/1e9:.2f}GB to {output_file}')
