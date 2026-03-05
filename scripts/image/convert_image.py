#!/usr/bin/env python3
"""
Image format conversion using ImageMagick
Usage: python convert_image.py photo.jpg photo.png
       python convert_image.py image.png image.webp --quality 85
"""

import subprocess
import json
import sys
import os


def convert_image(input_file, output_file, quality=85):
    """
    Convert image to specified format

    Args:
        input_file: Path to input image
        output_file: Path to output image
        quality: Quality (1-100, higher is better, default: 85)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    cmd = ["magick", input_file, "-quality", str(quality), output_file]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "convert",
            "quality": quality,
            "original_size": original_size,
            "output_size": output_size,
            "size_change": f"{output_size / original_size * 100:.1f}%"
            if original_size > 0
            else "0%",
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}


def main():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: convert_image.py input output [--quality value]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    quality = 85

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--quality" and i + 1 < len(sys.argv):
            quality = int(sys.argv[i + 1])

    if not 1 <= quality <= 100:
        print(
            json.dumps(
                {"status": "error", "message": "Quality must be between 1 and 100"}
            )
        )
        sys.exit(1)

    result = convert_image(input_file, output_file, quality)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
