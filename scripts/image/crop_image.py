#!/usr/bin/env python3
"""
Crop image using ImageMagick
Usage: python crop_image.py photo.jpg output.jpg --width 800 --height 600 --x 100 --y 50
       python crop_image.py photo.jpg output.jpg --width 800 --height 600 --center
"""

import subprocess
import json
import sys
import os


def crop_image(input_file, output_file, width, height, x=None, y=None, center=False):
    """
    Crop image to specified dimensions

    Args:
        input_file: Path to input image
        output_file: Path to output image
        width: Crop width in pixels
        height: Crop height in pixels
        x: X offset (pixels from left)
        y: Y offset (pixels from top)
        center: Center crop if True
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    # Build crop geometry
    if center:
        geometry = f"{width}x{height}+0+0"
        gravity = "center"
    else:
        if x is None or y is None:
            return {
                "status": "error",
                "message": "Either specify --x and --y or use --center",
            }
        geometry = f"{width}x{height}+{x}+{y}"
        gravity = "northwest"

    cmd = [
        "magick",
        input_file,
        "-gravity",
        gravity,
        "-crop",
        geometry,
        "+repage",  # Reset page geometry
        output_file,
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "crop",
            "width": width,
            "height": height,
            "x": x,
            "y": y,
            "center": center,
            "geometry": geometry,
            "gravity": gravity,
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
                    "message": "Usage: crop_image.py input output --width W --height H [--x X --y Y | --center]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    width = None
    height = None
    x = None
    y = None
    center = False

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--width" and i + 1 < len(sys.argv):
            width = int(sys.argv[i + 1])
        elif arg == "--height" and i + 1 < len(sys.argv):
            height = int(sys.argv[i + 1])
        elif arg == "--x" and i + 1 < len(sys.argv):
            x = int(sys.argv[i + 1])
        elif arg == "--y" and i + 1 < len(sys.argv):
            y = int(sys.argv[i + 1])
        elif arg == "--center":
            center = True

    if not width or not height:
        print(
            json.dumps(
                {"status": "error", "message": "Both --width and --height are required"}
            )
        )
        sys.exit(1)

    if center and (x is not None or y is not None):
        print(
            json.dumps(
                {"status": "error", "message": "Cannot use --center with --x and --y"}
            )
        )
        sys.exit(1)

    result = crop_image(input_file, output_file, width, height, x, y, center)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
