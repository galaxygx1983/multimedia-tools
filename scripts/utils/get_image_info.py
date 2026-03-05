#!/usr/bin/env python3
"""
Get image metadata using ImageMagick
Usage: python get_image_info.py photo.jpg
"""

import subprocess
import json
import sys
import os
import re


def get_image_info(input_file):
    """
    Extract metadata from image file

    Args:
        input_file: Path to image file
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"File not found: {input_file}"}

    # Get image information
    cmd = ["magick", "identify", "-verbose", input_file]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        # Parse the output
        info = {
            "status": "success",
            "file": input_file,
            "format": None,
            "width": None,
            "height": None,
            "depth": None,
            "size": os.path.getsize(input_file),
        }

        # Extract format
        format_match = re.search(r"Format:\s*(\S+)", output)
        if format_match:
            info["format"] = format_match.group(1)

        # Extract dimensions
        geometry_match = re.search(r"Geometry:\s*(\d+)x(\d+)", output)
        if geometry_match:
            info["width"] = int(geometry_match.group(1))
            info["height"] = int(geometry_match.group(2))

        # Extract depth
        depth_match = re.search(r"Depth:\s*(\d+)-bit", output)
        if depth_match:
            info["depth"] = int(depth_match.group(1))

        # Extract resolution (DPI)
        resolution_match = re.search(r"Reolution:\s*([\d.]+)x([\d.]+)", output)
        if resolution_match:
            info["resolution"] = {
                "x": float(resolution_match.group(1)),
                "y": float(resolution_match.group(2)),
            }

        # Extract color space
        colorspace_match = re.search(r"Colorspace:\s*(\S+)", output)
        if colorspace_match:
            info["colorspace"] = colorspace_match.group(1)

        # Extract compression quality (if available)
        quality_match = re.search(r"Quality:\s*(\d+)", output)
        if quality_match:
            info["quality"] = int(quality_match.group(1))

        # Check if transparency is present
        alpha_match = re.search(r"Alpha:\s*(\S+)", output)
        if alpha_match:
            info["has_transparency"] = alpha_match.group(1).lower() in ["yes", "true"]

        return info

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"status": "error", "message": "Usage: get_image_info.py image_file"}
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    result = get_image_info(input_file)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
