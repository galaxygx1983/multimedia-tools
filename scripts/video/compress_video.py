#!/usr/bin/env python3
"""
Video compression using FFmpeg with scenario-based presets
Usage: python compress_video.py input.mp4 output.mp4 --preset web
       python compress_video.py input.mp4 output.mp4 --preset archive
"""

import subprocess
import json
import sys
import os

VIDEO_PRESETS = {
    "web": {"crf": 28, "preset": "fast", "audio_bitrate": "128k"},
    "archive": {"crf": 18, "preset": "slow", "audio_bitrate": "192k"},
    "default": {"crf": 23, "preset": "medium", "audio_bitrate": "128k"},
}


def compress_video(input_file, output_file, preset="default"):
    """
    Compress video with scenario-based preset

    Args:
        input_file: Path to input video
        output_file: Path to output video
        preset: Quality preset (web, archive, default)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    if preset not in VIDEO_PRESETS:
        available = ", ".join(VIDEO_PRESETS.keys())
        return {
            "status": "error",
            "message": f"Invalid preset: {preset}. Available: {available}",
        }

    config = VIDEO_PRESETS[preset]

    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-crf",
        str(config["crf"]),
        "-preset",
        config["preset"],
        "-c:a",
        "aac",
        "-b:a",
        config["audio_bitrate"],
        "-movflags",
        "+faststart",
        "-y",
        output_file,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "compress",
            "preset_used": preset,
            "crf": config["crf"],
            "encoding_preset": config["preset"],
            "original_size": original_size,
            "output_size": output_size,
            "compression_ratio": round((1 - output_size / original_size) * 100, 2)
            if original_size > 0
            else 0,
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}


def main():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: compress_video.py input output [--preset web|archive|default]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    preset = "default"

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--preset" and i + 1 < len(sys.argv):
            preset = sys.argv[i + 1].lower()

    result = compress_video(input_file, output_file, preset)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
