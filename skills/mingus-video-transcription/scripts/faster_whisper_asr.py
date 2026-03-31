from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 scripts/faster_whisper_asr.py /path/to/video-or-audio [model_dir]", file=sys.stderr)
        return 1

    media_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) >= 3 else "data/models/faster-whisper-tiny"

    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        print(f"faster-whisper import failed: {exc}", file=sys.stderr)
        return 1

    try:
        model = WhisperModel(model_path, device="cpu", compute_type="int8", local_files_only=True)
        segments, _ = model.transcribe(
            media_path,
            beam_size=1,
            vad_filter=True,
            language="zh",
        )
        transcript = "".join(segment.text.strip() for segment in segments if segment.text.strip()).strip()
        if not transcript:
            print("empty transcript", file=sys.stderr)
            return 1
        print(transcript)
        return 0
    except Exception as exc:
        print(f"faster-whisper transcription failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
