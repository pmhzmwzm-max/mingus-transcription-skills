# Mingus Image Transcription Troubleshooting

## Wrong input type

This skill expects a local image file or a direct public image URL.

- Good: `https://.../note-1.webp`
- Bad: `https://www.xhs-style-post-page.com/explore/...`

If you only have a social post page URL, first resolve the real image URLs through a browser workflow.

## OCR text is empty or very weak

Common reasons:

- The image is decorative rather than text-heavy
- Contrast is low
- The image is very compressed
- The text is tiny compared with the full canvas

Do not invent missing text. Return the raw OCR and note the likely quality issue.

## OCR contains noise

That is expected for screenshots, posters, and long note images.

- Keep the raw OCR as the primary output
- If the user wants cleanup, produce a separate cleaned version
- Do not overwrite the raw OCR with paraphrases

## Multi-image order matters

If one note contains multiple images, OCR them in the original image order and keep that order explicit in the output.

Use:

```bash
python3 scripts/ocr_images.py image1.webp image2.webp image3.webp
```

## Long image notes

Try normal OCR first. Only split long images externally if OCR repeatedly fails or drops large sections.
