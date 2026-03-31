---
name: mingus-video-transcription
description: Transcribe spoken audio from local video or audio files, or resolved public media file URLs, into raw spoken-script text using a local faster-whisper model. Use when Codex needs a real 口播稿/逐字稿 from short-form video, screen recordings, downloaded mp4 files, or direct mp4/mov/m4a/mp3/wav URLs. Especially useful when OCR is not enough and the user wants the spoken words rather than on-screen text. If the user only has a social post page URL, first resolve the real media URL or local file through a separate browser workflow; this skill starts from the media file itself.
---

# Mingus Video Transcription

## Overview

Use this skill to turn a local media file or a resolved direct media URL into raw spoken-script text with local `faster-whisper`.

This skill is for **audio transcription**, not page scraping. If the input is a social post page URL, first obtain the actual media file URL or download the media locally, then use the scripts here.

## Workflow

### 1. Check the input shape

Use this skill when the input is one of:

- A local file such as `.mp4`, `.mov`, `.m4a`, `.mp3`, `.wav`
- A resolved public direct media URL that points to a real file

Do **not** use this skill directly on a Xiaohongshu/TikTok/Instagram post page URL. Those page URLs need a separate browser/media-resolution step first.

### 2. Prepare the local whisper model

Run this once if `data/models/faster-whisper-tiny/model.bin` does not exist:

```bash
python3 scripts/download_faster_whisper_model.py
```

The downloader uses resumable chunked downloads because large model files can reset mid-transfer.

### 3. Transcribe the media

Use the one-shot wrapper for the common case:

```bash
python3 scripts/transcribe_media.py /path/to/video.mp4
python3 scripts/transcribe_media.py 'https://example.com/video.mp4'
```

This wrapper:

- Downloads the model if it is missing
- Downloads the media to a temp file if the input is a URL
- Runs local `faster-whisper`
- Prints raw spoken transcript text to stdout

If the caller already has a resolved social-media video URL or a downloaded local file, this is the preferred entrypoint.

If you already have the model and want the lowest-level call:

```bash
python3 scripts/faster_whisper_asr.py /path/to/video.mp4
```

## Output Rules

- Treat the transcript as **raw ASR output**, not polished copy
- Keep obvious recognition noise unless the user explicitly asks for cleanup
- If the user wants a cleaner version, produce it **separately** from the raw transcript
- If there is no useful spoken audio, report that honestly instead of filling gaps with OCR
- If the media is short-form educational content, prefer preserving pauses and colloquial filler rather than summarizing

## Failure Handling

- If model download fails partway, rerun `download_faster_whisper_model.py`; it resumes
- If the input is a social page URL instead of a direct media URL, stop and switch to a browser/media-resolution workflow
- If the transcript is empty, report that the media likely has no usable speech or the audio is too noisy
- If macOS system ASR is blocked or inconsistent, stay on `faster-whisper`; do not silently fall back to OCR

## Resources

### `scripts/download_faster_whisper_model.py`

Downloads `Systran/faster-whisper-tiny` into `data/models/faster-whisper-tiny` with resumable chunk downloads.

### `scripts/faster_whisper_asr.py`

Runs local `faster-whisper` against an existing local media file and prints raw transcript text.

### `scripts/transcribe_media.py`

Convenience wrapper for local files and public media URLs.

### `references/troubleshooting.md`

Read this when model download, media resolution, or ASR quality becomes the bottleneck.
