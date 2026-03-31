from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
import urllib.request
from urllib.error import URLError


MODEL_REPO = "https://huggingface.co/Systran/faster-whisper-tiny"
FILES = ("config.json", "model.bin", "tokenizer.json", "vocabulary.txt")


def get_model_file_urls() -> dict[str, str]:
    with urllib.request.urlopen(f"{MODEL_REPO}/resolve/main/model.bin", timeout=60) as response:
        resolved_model_url = response.geturl()
    return {
        "config.json": f"{MODEL_REPO}/resolve/main/config.json",
        "tokenizer.json": f"{MODEL_REPO}/resolve/main/tokenizer.json",
        "vocabulary.txt": f"{MODEL_REPO}/resolve/main/vocabulary.txt",
        "model.bin": resolved_model_url,
    }


def download_small_file(url: str, target: Path) -> None:
    urllib.request.urlretrieve(url, target)


def chunk_download(url: str, target: Path, chunk_size: int = 1024 * 1024) -> None:
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as response:
        total_size = int(response.headers["Content-Length"])

    downloaded = target.stat().st_size if target.exists() else 0
    mode = "ab" if downloaded else "wb"
    with target.open(mode) as handle:
        while downloaded < total_size:
            end = min(downloaded + chunk_size - 1, total_size - 1)
            chunk_req = urllib.request.Request(url, headers={"Range": f"bytes={downloaded}-{end}"})
            for attempt in range(5):
                try:
                    with urllib.request.urlopen(chunk_req, timeout=60) as response:
                        handle.write(response.read())
                    break
                except URLError:
                    if attempt == 4:
                        raise
                    time.sleep(2 * (attempt + 1))
            downloaded = target.stat().st_size
            print(json.dumps({"file": target.name, "downloaded": downloaded, "total": total_size}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Download local faster-whisper tiny model")
    parser.add_argument("--output-dir", default="data/models/faster-whisper-tiny")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    urls = get_model_file_urls()

    for name in FILES:
        target = output_dir / name
        if name != "model.bin" and target.exists() and target.stat().st_size > 0:
            continue
        if name == "model.bin":
            chunk_download(urls[name], target)
        else:
            download_small_file(urls[name], target)
            print(json.dumps({"file": target.name, "downloaded": target.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
