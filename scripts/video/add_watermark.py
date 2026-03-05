#!/usr/bin/env python3
"""
Add custom watermark to videos using FFmpeg
Usage: python add_watermark.py input.mp4 watermark.png output.mp4
       python add_watermark.py input.mp4 watermark.png output.mp4 --position top-left --opacity 0.7
"""

import subprocess
import json
import sys
import os

POSITIONS = {
    "top-left": "10:10",
    "top-right": "main_w-overlay_w-10:10",
    "bottom-left": "10:main_h-overlay_h-10",
    "bottom-right": "main_w-overlay_w-10:main_h-overlay_h-10",
    "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2",
}


def add_watermark(
    input_file, watermark_file, output_file, position="bottom-right", opacity=1.0
):
    """
    Add watermark to video

    Args:
        input_file: Path to input video
        watermark_file: Path to watermark image
        output_file: Path to output video
        position: Watermark position (top-left, top-right, bottom-left, bottom-right, center)
        opacity: Opacity value (0.0 to 1.0)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input video not found: {input_file}"}
    if not os.path.exists(watermark_file):
        return {
            "status": "error",
            "message": f"Watermark file not found: {watermark_file}",
        }

    pos = POSITIONS.get(position.lower(), POSITIONS["bottom-right"])

    # Apply opacity and overlay - cross-platform compatible
    filter_complex = (
        f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[wm];[0:v][wm]overlay={pos}]"
    )

    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-i",
        watermark_file,
        "-filter_complex",
        filter_complex,
        "-c:a",
        "copy",  # Copy audio stream
        "-y",
        output_file,
    ]

    try:
        subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

        return {
            "status": "success",
            "output": output_file,
            "operation": "watermark",
            "position": position,
            "opacity": opacity,
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}


def main():
    if len(sys.argv) < 4:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: add_watermark.py input watermark output [--position pos] [--opacity value]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    watermark_file = sys.argv[2]
    output_file = sys.argv[3]
    position = "bottom-right"
    opacity = 1.0

    for i, arg in enumerate(sys.argv[4:], 4):
        if arg == "--position" and i + 1 < len(sys.argv):
            position = sys.argv[i + 1].lower()
        elif arg == "--opacity" and i + 1 < len(sys.argv):
            opacity = float(sys.argv[i + 1])

    if not 0 <= opacity <= 1:
        print(
            json.dumps(
                {"status": "error", "message": "Opacity must be between 0.0 and 1.0"}
            )
        )
        sys.exit(1)

    result = add_watermark(input_file, watermark_file, output_file, position, opacity)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
