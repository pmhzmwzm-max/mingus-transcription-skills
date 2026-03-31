---
name: mingus-image-transcription
description: Use when Codex needs raw visible text from local images or resolved direct image URLs, especially for note-style image posts, screenshots, posters, slides, or multi-image sequences where the goal is to capture image text rather than spoken audio. If the user only has a social post page URL, first resolve the real image URLs or save the images locally through a separate browser workflow; this skill starts from the image file itself.
---

# Mingus Image Transcription

## Overview

Use this skill to turn one or more local images, or direct image URLs, into raw OCR text with Apple Vision on macOS.

This skill is for **image OCR**, not page scraping. If the user only has a Xiaohongshu/TikTok/Instagram post page URL, first resolve the actual image URLs or download the images locally, then use the scripts here.

Default fast path for note collection:

- Resolve the full ordered image list once in a browser workflow
- Run `scripts/ocr_images.py` on the whole ordered set
- Preserve image order in output
- Keep OCR raw; do cleanup downstream if needed

## Workflow

### 1. Check the input shape

Use this skill when the input is one of:

- A local file such as `.png`, `.jpg`, `.jpeg`, `.webp`, `.heic`
- A resolved public direct image URL that points to a real image file
- A small ordered set of note images that should be OCR'd in sequence

Do **not** use this skill directly on a social post page URL. Resolve the real image URLs first.

### 2. Run OCR on one image

For the common case:

```bash
python3 scripts/ocr_image.py /path/to/image.png
python3 scripts/ocr_image.py 'https://example.com/note-image.webp'
```

This wrapper:

- Downloads the input to a temp file if the input is a URL
- Runs Apple Vision OCR through `swift scripts/apple_ocr.swift`
- Prints raw OCR text to stdout

### 3. Run OCR on multiple ordered images

If the user has multiple ordered images from one note, keep the original order:

```bash
python3 scripts/ocr_images.py /path/to/1.png /path/to/2.png /path/to/3.png
python3 scripts/ocr_images.py 'https://example.com/1.webp' 'https://example.com/2.webp'
```

The batch wrapper prints numbered sections so the caller can preserve page order.

For note collection, this is the preferred entrypoint. Do not loop `ocr_image.py` manually unless there is only one image.

### 4. Handle output correctly

- Treat OCR text as **raw image text**, not a cleaned summary
- Keep recognition noise unless the user explicitly asks for cleanup
- If the user wants a cleaner version, produce it **separately** from the raw OCR
- If multiple images belong to one note, keep the image order explicit
- If OCR is partial because the images were incomplete, report that the source set is incomplete instead of pretending the note is fully covered

## Failure Handling

- If the input is a social page URL instead of a direct image URL, stop and switch to a browser/media-resolution workflow
- If OCR text is empty, report that the image may be low-contrast, decorative, or too noisy
- If the image is very long, split it externally only when necessary; prefer trying OCR first
- If the user needs OCR from many images in one note, use `ocr_images.py` rather than repeating single-image calls manually

## Resources

### `scripts/apple_ocr.swift`

Runs Apple Vision OCR against one local image and prints raw recognized text.

### `scripts/ocr_image.py`

Convenience wrapper for one local image or one direct image URL.

### `scripts/ocr_images.py`

Batch wrapper for multiple ordered images.

### `references/troubleshooting.md`

Read this when OCR quality, URL resolution, or image ordering becomes the bottleneck.
