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
    suffix = Path(url.split("?")[0]).suffix or ".img"
    target = Path(tempfile.mkdtemp(prefix="mingus_img_")) / f"asset{suffix}"
    urllib.request.urlretrieve(url, target)
    return target


def run_ocr(image_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["swift", "scripts/apple_ocr.swift", str(image_path)],
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract raw OCR text from one local image or direct image URL")
    parser.add_argument("input")
    args = parser.parse_args()

    image_path = download_to_temp(args.input) if is_url(args.input) else Path(args.input)
    if not image_path.exists():
        print(f"image not found: {image_path}", file=sys.stderr)
        return 1

    result = run_ocr(image_path)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode

    sys.stdout.write(result.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
