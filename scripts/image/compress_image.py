#!/usr/bin/env python3
"""
Image compression using ImageMagick with scenario-based presets
Usage: python compress_image.py photo.jpg output.jpg --preset web
       python compress_image.py photo.png output.png --preset print
"""

import subprocess
import json
import sys
import os

IMAGE_PRESETS = {
    "web": {"quality": 85, "strip": True},
    "print": {"quality": 95, "strip": False, "density": 300},
    "thumbnail": {"quality": 75, "strip": True, "recommended_width": 200},
    "default": {"quality": 85, "strip": True},
}


def compress_image(input_file, output_file, preset="default"):
    """
    Compress image with scenario-based preset

    Args:
        input_file: Path to input image
        output_file: Path to output image
        preset: Quality preset (web, print, thumbnail, default)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    if preset not in IMAGE_PRESETS:
        available = ", ".join(IMAGE_PRESETS.keys())
        return {
            "status": "error",
            "message": f"Invalid preset: {preset}. Available: {available}",
        }

    config = IMAGE_PRESETS[preset]

    # Build command
    cmd = ["magick", input_file]

    if config.get("strip"):
        cmd.append("-strip")

    if "density" in config:
        cmd.extend(["-density", str(config["density"])])

    cmd.extend(["-quality", str(config["quality"]), output_file])

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0

        return {
            "status": "success",
            "output": output_file,
            "operation": "compress",
            "preset_used": preset,
            "quality": config["quality"],
            "strip_metadata": config.get("strip", False),
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
                    "message": "Usage: compress_image.py input output [--preset web|print|thumbnail|default]",
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

    result = compress_image(input_file, output_file, preset)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
