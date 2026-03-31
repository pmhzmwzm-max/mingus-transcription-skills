from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def download_to_temp(url: str) -> Path:
    suffix = Path(url.split("?")[0]).suffix or ".mp4"
    target = Path(tempfile.mkdtemp(prefix="mingus_media_")) / f"asset{suffix}"
    urllib.request.urlretrieve(url, target)
    return target


def ensure_model(model_dir: str) -> None:
    model_bin = Path(model_dir) / "model.bin"
    if model_bin.exists() and model_bin.stat().st_size > 0:
        return
    subprocess.run(
        ["python3", "scripts/download_faster_whisper_model.py", "--output-dir", model_dir],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe local media file or public media URL")
    parser.add_argument("input")
    parser.add_argument("--model-dir", default="data/models/faster-whisper-tiny")
    args = parser.parse_args()

    ensure_model(args.model_dir)
    media_path = download_to_temp(args.input) if is_url(args.input) else Path(args.input)
    if not media_path.exists():
        print(f"media not found: {media_path}", file=sys.stderr)
        return 1

    result = subprocess.run(
        ["python3", "scripts/faster_whisper_asr.py", str(media_path), args.model_dir],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    sys.stdout.write(result.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
