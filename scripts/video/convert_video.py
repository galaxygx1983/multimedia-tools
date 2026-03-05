#!/usr/bin/env python3
"""
Video format conversion using FFmpeg
Usage: python convert_video.py input.mov output.mp4
       python convert_video.py input.avi output.webm --codec libx265
"""

import subprocess
import json
import sys
import os


def convert_video(input_file, output_file, codec="libx264", crf=23, preset="medium"):
    """
    Convert video to specified format

    Args:
        input_file: Path to input video
        output_file: Path to output video
        codec: Video codec (default: libx264)
        crf: Quality (0-51, lower is better, default: 23)
        preset: Encoding speed (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        codec,
        "-crf",
        str(crf),
        "-preset",
        preset,
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",  # Enable fast start for web
        "-y",  # Overwrite output
        output_file,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

        # Get file sizes
        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "convert",
            "codec": codec,
            "crf": crf,
            "preset": preset,
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
                    "message": "Usage: convert_video.py input output [--codec codec] [--crf value] [--preset preset]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    codec = "libx264"
    crf = 23
    preset = "medium"

    # Parse optional arguments
    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--codec" and i + 1 < len(sys.argv):
            codec = sys.argv[i + 1]
        elif arg == "--crf" and i + 1 < len(sys.argv):
            crf = int(sys.argv[i + 1])
        elif arg == "--preset" and i + 1 < len(sys.argv):
            preset = sys.argv[i + 1]

    result = convert_video(input_file, output_file, codec, crf, preset)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
