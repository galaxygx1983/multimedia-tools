#!/usr/bin/env python3
"""
Add custom watermark to images using ImageMagick
Usage: python add_watermark.py photo.jpg watermark.png output.jpg
       python add_watermark.py photo.jpg watermark.png output.jpg --position Center --opacity 50
"""

import subprocess
import json
import sys
import os

GRAVITY = {
    "northwest": "NorthWest",
    "north": "North",
    "northeast": "NorthEast",
    "west": "West",
    "center": "Center",
    "east": "East",
    "southwest": "SouthWest",
    "south": "South",
    "southeast": "SouthEast",
}


def add_watermark(
    input_file, watermark_file, output_file, position="southeast", opacity=80
):
    """
    Add watermark to image

    Args:
        input_file: Path to input image
        watermark_file: Path to watermark image
        output_file: Path to output image
        position: Watermark position (northwest, north, northeast, west, center, east, southwest, south, southeast)
        opacity: Opacity value (0-100)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input image not found: {input_file}"}
    if not os.path.exists(watermark_file):
        return {
            "status": "error",
            "message": f"Watermark file not found: {watermark_file}",
        }

    gravity = GRAVITY.get(position.lower(), GRAVITY["southeast"])

    # Apply opacity and composite - cross-platform compatible
    # Use tempfile for watermark with opacity applied
    opacity_value = opacity / 100.0

    cmd = [
        "magick",
        input_file,
        "(",
        watermark_file,
        "-alpha",
        "set",
        "-channel",
        "A",
        "-evaluate",
        "multiply",
        f"{opacity_value}",
        "+channel",
        ")",
        "-gravity",
        gravity,
        "-composite",
        output_file,
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

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
    position = "southeast"
    opacity = 80

    for i, arg in enumerate(sys.argv[4:], 4):
        if arg == "--position" and i + 1 < len(sys.argv):
            position = sys.argv[i + 1].lower()
        elif arg == "--opacity" and i + 1 < len(sys.argv):
            opacity = int(sys.argv[i + 1])

    if not 0 <= opacity <= 100:
        print(
            json.dumps(
                {"status": "error", "message": "Opacity must be between 0 and 100"}
            )
        )
        sys.exit(1)

    result = add_watermark(input_file, watermark_file, output_file, position, opacity)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
