#!/usr/bin/env python3
"""
Video resize using FFmpeg
Usage: python resize_video.py input.mp4 output.mp4 --width 1280
       python resize_video.py input.mp4 output.mp4 --width 1280 --height 720
"""

import subprocess
import json
import sys
import os


def resize_video(input_file, output_file, width=None, height=None):
    """
    Resize video to specified dimensions

    Args:
        input_file: Path to input video
        output_file: Path to output video
        width: Target width (maintains aspect ratio if height not specified)
        height: Target height (maintains aspect ratio if width not specified)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    if not width and not height:
        return {
            "status": "error",
            "message": "At least --width or --height must be specified",
        }

    # Build scale filter - ensure dimensions are divisible by 2 for H.264 compatibility
    if width and height:
        # Ensure both dimensions are even
        width = width if width % 2 == 0 else width - 1
        height = height if height % 2 == 0 else height - 1
        scale_filter = f"{width}:{height}"
    elif width:
        scale_filter = f"{width}:-2"  # Maintain aspect ratio with even height
    else:
        scale_filter = f"-2:{height}"  # Maintain aspect ratio with even width

    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-vf",
        f"scale={scale_filter}",
        "-c:a",
        "copy",  # Copy audio stream
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
            "operation": "resize",
            "width": width,
            "height": height,
            "scale_filter": scale_filter,
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
                    "message": "Usage: resize_video.py input output [--width value] [--height value]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    width = None
    height = None

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--width" and i + 1 < len(sys.argv):
            width = int(sys.argv[i + 1])
        elif arg == "--height" and i + 1 < len(sys.argv):
            height = int(sys.argv[i + 1])

    result = resize_video(input_file, output_file, width, height)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
