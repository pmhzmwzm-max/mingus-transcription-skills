# Mingus Transcription Skills

Two Codex skills for turning short-form media into raw source text.

## Included skills

- `mingus-video-transcription`
  - Input: local video/audio files or resolved public direct media URLs
  - Output: raw spoken transcript text
- `mingus-image-transcription`
  - Input: local images or resolved public direct image URLs
  - Output: raw OCR text, including ordered multi-image notes

## Repository layout

```text
skills/
  mingus-video-transcription/
  mingus-image-transcription/
```

## Install locally

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

## Notes

- These skills start from resolved media assets, not social post page URLs.
- For Xiaohongshu-style flows, first use a browser workflow to resolve the real media/image URL, then call the appropriate Mingus skill.
