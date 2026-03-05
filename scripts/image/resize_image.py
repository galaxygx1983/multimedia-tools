#!/usr/bin/env python3
"""
Image resize using ImageMagick
Usage: python resize_image.py photo.jpg output.jpg --width 1920
       python resize_image.py photo.jpg output.jpg --scale 50
"""

import subprocess
import json
import sys
import os


def resize_image(input_file, output_file, width=None, height=None, scale=None):
    """
    Resize image to specified dimensions or scale

    Args:
        input_file: Path to input image
        output_file: Path to output image
        width: Target width (maintains aspect ratio if height not specified)
        height: Target height (maintains aspect ratio if width not specified)
        scale: Scale percentage (e.g., 50 for 50%)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    # Build resize geometry
    if scale:
        geometry = f"{scale}%"
    elif width and height:
        geometry = f"{width}x{height}!"
    elif width:
        geometry = f"{width}"
    elif height:
        geometry = f"x{height}"
    else:
        return {"status": "error", "message": "Specify --width, --height, or --scale"}

    cmd = ["magick", input_file, "-resize", geometry, output_file]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "resize",
            "width": width,
            "height": height,
            "scale": scale,
            "geometry": geometry,
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
                    "message": "Usage: resize_image.py input output [--width value] [--height value] [--scale value]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    width = None
    height = None
    scale = None

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--width" and i + 1 < len(sys.argv):
            width = int(sys.argv[i + 1])
        elif arg == "--height" and i + 1 < len(sys.argv):
            height = int(sys.argv[i + 1])
        elif arg == "--scale" and i + 1 < len(sys.argv):
            scale = int(sys.argv[i + 1])

    result = resize_image(input_file, output_file, width, height, scale)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
