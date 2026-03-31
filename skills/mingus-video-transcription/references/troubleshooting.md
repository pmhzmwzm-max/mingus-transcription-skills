# Troubleshooting

## When the input is a social media page URL

This skill does not resolve page URLs like Xiaohongshu post links.

Use a browser workflow first to obtain:

- A local `.mp4`/`.mov`/`.m4a` file, or
- A public direct media URL

Then run `scripts/transcribe_media.py`.

## When the model download fails

- Rerun `scripts/download_faster_whisper_model.py`
- The downloader resumes `model.bin` with HTTP range requests
- Small config files download directly; the large binary is the only part expected to retry

## When the transcript quality is rough

This is raw ASR output. Expect:

- Missing punctuation
- Confused proper nouns
- Misrecognized English tokens such as `HTML`, `DeepSeek`, or brand names

If the user wants a cleaner draft, keep the raw transcript and produce a second cleaned version separately.

## When there is no useful transcript

Likely causes:

- The media contains little or no speech
- The audio is heavily mixed with music/noise
- The URL points to a page or preview asset rather than the real media file
