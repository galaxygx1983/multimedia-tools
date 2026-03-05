#!/usr/bin/env python3
"""
Extract audio from video using FFmpeg
Usage: python extract_audio.py input.mp4 output.mp3
       python extract_audio.py input.mov output.wav --codec pcm_s16le
"""

import subprocess
import json
import sys
import os


def extract_audio(input_file, output_file, codec=None):
    """
    Extract audio track from video

    Args:
        input_file: Path to input video
        output_file: Path to output audio
        codec: Audio codec (auto-detected from output extension if not specified)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    # Auto-detect codec from output extension if not specified
    if not codec:
        ext = os.path.splitext(output_file)[1].lower()
        codec_map = {
            ".mp3": "libmp3lame",
            ".aac": "aac",
            ".wav": "pcm_s16le",
            ".flac": "flac",
            ".m4a": "aac",
            ".ogg": "libvorbis",
            ".opus": "libopus",
        }
        codec = codec_map.get(ext, "libmp3lame")

    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vn",  # No video
        "-acodec",
        codec,
        "-y",
        output_file,
    ]

    try:
        subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "extract_audio",
            "codec": codec,
            "original_size": original_size,
            "output_size": output_size,
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}


def main():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: extract_audio.py input output [--codec codec]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    codec = None

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--codec" and i + 1 < len(sys.argv):
            codec = sys.argv[i + 1]

    result = extract_audio(input_file, output_file, codec)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
