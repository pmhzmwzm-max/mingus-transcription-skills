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
    target = Path(tempfile.mkdtemp(prefix="mingus_imgs_")) / f"asset{suffix}"
    urllib.request.urlretrieve(url, target)
    return target


def resolve_input(value: str) -> Path:
    return download_to_temp(value) if is_url(value) else Path(value)


def run_ocr(image_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["swift", "scripts/apple_ocr.swift", str(image_path)],
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract raw OCR text from multiple local images or direct image URLs in order"
    )
    parser.add_argument("inputs", nargs="+")
    args = parser.parse_args()

    for index, raw_input in enumerate(args.inputs, start=1):
        image_path = resolve_input(raw_input)
        if not image_path.exists():
            print(f"image not found: {image_path}", file=sys.stderr)
            return 1

        result = run_ocr(image_path)
        if result.returncode != 0:
            sys.stderr.write(result.stderr)
            return result.returncode

        if index > 1:
            sys.stdout.write("\n\n")
        sys.stdout.write(f"## Image {index}\n")
        sys.stdout.write(result.stdout.strip())
        if result.stdout and not result.stdout.endswith("\n"):
            sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
