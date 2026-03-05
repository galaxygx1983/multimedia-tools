#!/usr/bin/env python3
"""
Batch process images using ImageMagick
Usage: python batch_process_image.py input_folder/ output_folder/ --operation convert --format png
       python batch_process_image.py input_folder/ output_folder/ --operation compress --preset web
"""

import subprocess
import json
import sys
import os
import glob

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp"]


def batch_process(input_folder, output_folder, operation, **kwargs):
    """
    Batch process images

    Args:
        input_folder: Path to input folder
        output_folder: Path to output folder
        operation: Operation to perform (convert, compress, resize, crop, watermark)
        **kwargs: Operation-specific parameters
    """
    if not os.path.exists(input_folder):
        return {"status": "error", "message": f"Input folder not found: {input_folder}"}

    os.makedirs(output_folder, exist_ok=True)

    # Find all image files
    image_files = []
    for ext in IMAGE_EXTENSIONS:
        image_files.extend(glob.glob(os.path.join(input_folder, f"*{ext}")))
        image_files.extend(glob.glob(os.path.join(input_folder, f"*{ext.upper()}")))

    if not image_files:
        return {"status": "error", "message": f"No image files found in {input_folder}"}

    results = []
    success_count = 0
    error_count = 0

    for input_file in image_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_folder, filename)

        # Modify output extension for convert operation
        if operation == "convert":
            format_ext = kwargs.get("format", "png")
            output_file = os.path.splitext(output_file)[0] + f".{format_ext}"

        result = process_single(input_file, output_file, operation, **kwargs)
        results.append({"input": input_file, "output": output_file, "result": result})

        if result["status"] == "success":
            success_count += 1
        else:
            error_count += 1

    return {
        "status": "completed",
        "operation": operation,
        "total_files": len(image_files),
        "success_count": success_count,
        "error_count": error_count,
        "results": results,
    }


def process_single(input_file, output_file, operation, **kwargs):
    """Process a single image file"""
    if operation == "convert":
        quality = kwargs.get("quality", 85)
        cmd = ["magick", input_file, "-quality", str(quality), output_file]
    elif operation == "compress":
        preset = kwargs.get("preset", "default")
        preset_config = {
            "web": {"quality": 85, "strip": True},
            "print": {"quality": 95, "strip": False},
            "thumbnail": {"quality": 75, "strip": True},
            "default": {"quality": 85, "strip": True},
        }.get(preset, {"quality": 85, "strip": True})
        cmd = ["magick", input_file]
        if preset_config["strip"]:
            cmd.append("-strip")
        cmd.extend(["-quality", str(preset_config["quality"]), output_file])
    elif operation == "resize":
        width = kwargs.get("width", None)
        height = kwargs.get("height", None)
        scale = kwargs.get("scale", None)
        if scale:
            geometry = f"{scale}%"
        elif width and height:
            geometry = f"{width}x{height}!"
        elif width:
            geometry = f"{width}"
        elif height:
            geometry = f"x{height}"
        else:
            return {
                "status": "error",
                "message": "Specify --width, --height, or --scale",
            }
        cmd = ["magick", input_file, "-resize", geometry, output_file]
    elif operation == "crop":
        width = kwargs.get("width", None)
        height = kwargs.get("height", None)
        center = kwargs.get("center", False)
        x = kwargs.get("x", 0 if not center else None)
        y = kwargs.get("y", 0 if not center else None)
        if not width or not height:
            return {
                "status": "error",
                "message": "Both --width and --height are required",
            }
        gravity = "center" if center else "northwest"
        geometry = (
            f"{width}x{height}+{x}+{y}" if not center else f"{width}x{height}+0+0"
        )
        cmd = [
            "magick",
            input_file,
            "-gravity",
            gravity,
            "-crop",
            geometry,
            "+repage",
            output_file,
        ]
    elif operation == "watermark":
        watermark = kwargs.get("wm", None)
        position = kwargs.get("position", "southeast")
        opacity = kwargs.get("opacity", 80)
        if not watermark or not os.path.exists(watermark):
            return {
                "status": "error",
                "message": f"Watermark file not found: {watermark}",
            }
        gravity = {
            "northwest": "NorthWest",
            "north": "North",
            "northeast": "NorthEast",
            "west": "West",
            "center": "Center",
            "east": "East",
            "southwest": "SouthWest",
            "south": "South",
            "southeast": "SouthEast",
        }.get(position.lower(), "SouthEast")
        cmd = [
            "magick",
            input_file,
            f"({watermark} -alpha set -channel A -evaluate multiply {opacity / 100}% +channel)",
            "-gravity",
            gravity,
            "-composite",
            output_file,
        ]
    else:
        return {"status": "error", "message": f"Unknown operation: {operation}"}

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"status": "success", "output": output_file}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}


def main():
    if len(sys.argv) < 5:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: batch_process_image.py input/ output/ --operation <convert|compress|resize|crop|watermark> [options]",
                }
            )
        )
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    operation = None
    kwargs = {}

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--operation" and i + 1 < len(sys.argv):
            operation = sys.argv[i + 1]
        elif arg == "--format" and i + 1 < len(sys.argv):
            kwargs["format"] = sys.argv[i + 1]
        elif arg == "--preset" and i + 1 < len(sys.argv):
            kwargs["preset"] = sys.argv[i + 1]
        elif arg == "--quality" and i + 1 < len(sys.argv):
            kwargs["quality"] = int(sys.argv[i + 1])
        elif arg == "--width" and i + 1 < len(sys.argv):
            kwargs["width"] = int(sys.argv[i + 1])
        elif arg == "--height" and i + 1 < len(sys.argv):
            kwargs["height"] = int(sys.argv[i + 1])
        elif arg == "--scale" and i + 1 < len(sys.argv):
            kwargs["scale"] = int(sys.argv[i + 1])
        elif arg == "--center":
            kwargs["center"] = True
        elif arg == "--x" and i + 1 < len(sys.argv):
            kwargs["x"] = int(sys.argv[i + 1])
        elif arg == "--y" and i + 1 < len(sys.argv):
            kwargs["y"] = int(sys.argv[i + 1])
        elif arg == "--wm" and i + 1 < len(sys.argv):
            kwargs["wm"] = sys.argv[i + 1]
        elif arg == "--position" and i + 1 < len(sys.argv):
            kwargs["position"] = sys.argv[i + 1]
        elif arg == "--opacity" and i + 1 < len(sys.argv):
            kwargs["opacity"] = int(sys.argv[i + 1])

    if not operation:
        print(json.dumps({"status": "error", "message": "--operation is required"}))
        sys.exit(1)

    result = batch_process(input_folder, output_folder, operation, **kwargs)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
