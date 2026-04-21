from huggingface_hub import hf_hub_download, list_repo_tree
import os, json, zstandard as zstd

# Languages with >1GB in OSCAR (from paper Table 5)
langs = [
    "zh", "en", "ru", "es", "fr", "de", "it", "ja", "hu", "pl",
    "vi", "nl", "ar", "pt", "el", "fa", "th", "cs", "tr", "sv",
    "ro", "uk", "bg", "fi", "ko", "hi", "id", "sk", "da", "he",
    "ta", "ca", "lt", "sr", "lv", "ml", "mn", "gu", "ne", "hy",
    "mk", "mr", "te", "ur", "kk", "sl", "az", "my", "si", "no",
    "kn", "be", "bn", "et", "eu", "gl", "ka", "km", "ky", "ms",
    "nb", "pa", "sq", "tt", "uz"
]

corpus_dir = "/scratch/network/ks2663/COLLAB/oscar-corpus/processed"

for lang in langs:
    print(f"Downloading {lang}...", flush=True)
    os.makedirs(f"{corpus_dir}/{lang}", exist_ok=True)
    out_path = f"{corpus_dir}/{lang}/{lang}_text.txt"

    # Skip if already done
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1e8:
        print(f"Skipping {lang}, already exists", flush=True)
        continue

    try:
        items = list(list_repo_tree(
            "oscar-corpus/community-oscar",
            repo_type="dataset",
            path_in_repo=f"data/2024-38/{lang}_meta"
        ))
        data_files = [i.path for i in items if i.path.endswith('.jsonl.zst')]
        print(f"Found {len(data_files)} files for {lang}", flush=True)
    except Exception as e:
        print(f"Could not find files for {lang}: {e}", flush=True)
        continue

    bytes_written = 0
    with open(out_path, "w") as out_f:
        for file_path in data_files:
            if bytes_written >= 1e9:
                break
            local = hf_hub_download(
                "oscar-corpus/community-oscar",
                filename=file_path,
                repo_type="dataset"
            )
            with open(local, 'rb') as f:
                dctx = zstd.ZstdDecompressor()
                stream = dctx.stream_reader(f)
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
                            text = doc.get('content', '')
                            out_f.write(text + "\n")
                            bytes_written += len(text.encode('utf-8'))
                            if bytes_written >= 1e9:
                                break
                        except:
                            continue
                    if bytes_written >= 1e9:
                        break
    print(f"Done {lang}: {bytes_written/1e9:.2f}GB", flush=True)

print("All done!")
