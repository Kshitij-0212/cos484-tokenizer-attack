# download_oscar_limited.py
from datasets import load_dataset
import os

langs = ["zh", "en", "ja", "ko", "ar", "fr", "de", "es", "ru", "pt"]
corpus_dir = "oscar-corpus/processed"

for lang in langs:
    print(f"Downloading {lang}...")
    os.makedirs(f"{corpus_dir}/{lang}", exist_ok=True)
    
    ds = load_dataset("oscar-corpus/OSCAR-2301", lang,
                      split="train", streaming=True,
                      trust_remote_code=True)
    
    out_path = f"{corpus_dir}/{lang}/{lang}_text.txt"
    bytes_written = 0
    with open(out_path, "w") as f:
        for example in ds:
            f.write(example["text"] + "\n")
            bytes_written += len(example["text"].encode("utf-8"))
            if bytes_written >= 1e9:  # 1GB
                break
    print(f"Done {lang}: {bytes_written/1e9:.2f}GB")

print("All done!")