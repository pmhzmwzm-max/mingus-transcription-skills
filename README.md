# Mingus Transcription Skills

`mingus-transcription-skills` is a small Codex skill pack for turning short-form media into raw source text.

It currently includes:

- `mingus-video-transcription`
  - Turn local video/audio files or resolved direct media URLs into raw spoken transcripts with a local `faster-whisper-small` default
- `mingus-image-transcription`
  - Turn local images or resolved direct image URLs into raw OCR text, including ordered multi-image notes

These skills are designed for workflows where the user wants the original source text back out of media, not a summary.

## Best fit

Use this repo when you need one of these two jobs:

1. Extract a real spoken script from short-form video
2. Extract raw visible text from image posts, screenshots, slides, or long note images

For `xhs`-style flows, these skills start **after** media resolution.
That means:

- First resolve the real video URL or image URLs through a browser workflow
- Then pass the resolved media asset into the matching Mingus skill

Recommended fast path for repeat collection:

1. Resolve the real media assets once with a browser workflow
2. Feed video into `mingus-video-transcription/scripts/transcribe_media.py`
3. Feed note images into `mingus-image-transcription/scripts/ocr_images.py`
4. Keep raw output honest, then do cleanup downstream if needed

## Included skills

### `mingus-video-transcription`

Purpose:
- Recover a real spoken transcript from video/audio instead of relying on OCR

Input:
- Local `.mp4`, `.mov`, `.m4a`, `.mp3`, `.wav`
- Resolved public direct media URLs

Output:
- Raw ASR transcript text

Defaults:
- Local model path: `data/models/faster-whisper-small`
- Raw spoken transcript only
- Never use OCR as a silent replacement for ASR

### `mingus-image-transcription`

Purpose:
- Recover visible text from one image or an ordered set of images

Input:
- Local `.png`, `.jpg`, `.jpeg`, `.webp`, `.heic`
- Resolved public direct image URLs

Output:
- Raw OCR text
- Ordered multi-image OCR blocks for image-note workflows

Best practice:
- For multi-image note workflows, prefer the batch wrapper `ocr_images.py` over repeated one-by-one OCR calls

## Repository layout

```text
skills/
  mingus-video-transcription/
  mingus-image-transcription/
```

## Local install

Copy either skill directory into your Codex skills directory:

```bash
cp -R skills/mingus-video-transcription ~/.codex/skills/
cp -R skills/mingus-image-transcription ~/.codex/skills/
```

## Validation

Use Codex's built-in skill validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/mingus-video-transcription
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/mingus-image-transcription
```

## Design rules

- Keep transcripts and OCR output raw by default
- Do not silently replace ASR with OCR
- Do not use social post page URLs as direct inputs
- Preserve ordered image flow for multi-image notes
- Treat cleanup and paraphrase as separate downstream steps
- If ASR quality is clearly poor, mark it as low-quality raw ASR instead of presenting it as final-quality transcript

## Typical usage

### Video

```bash
python3 skills/mingus-video-transcription/scripts/transcribe_media.py /path/to/video.mp4
```

### One image

```bash
python3 skills/mingus-image-transcription/scripts/ocr_image.py /path/to/image.png
```

### Multiple ordered images

```bash
python3 skills/mingus-image-transcription/scripts/ocr_images.py /path/to/1.webp /path/to/2.webp /path/to/3.webp
```

## Notes

- These skills start from resolved media assets, not social post page URLs
- For `xhs` workflows, use a browser workflow first, then call the appropriate Mingus skill
