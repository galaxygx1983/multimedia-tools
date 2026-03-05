#!/usr/bin/env python3
"""
Batch process videos using FFmpeg
Usage: python batch_process_video.py input_folder/ output_folder/ --operation convert --format mp4
       python batch_process_video.py input_folder/ output_folder/ --operation compress --preset web
"""

import subprocess
import json
import sys
import os
import glob

VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv"]


def batch_process(input_folder, output_folder, operation, **kwargs):
    """
    Batch process videos

    Args:
        input_folder: Path to input folder
        output_folder: Path to output folder
        operation: Operation to perform (convert, compress, resize, watermark)
        **kwargs: Operation-specific parameters
    """
    if not os.path.exists(input_folder):
        return {"status": "error", "message": f"Input folder not found: {input_folder}"}

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Find all video files
    video_files = []
    for ext in VIDEO_EXTENSIONS:
        video_files.extend(glob.glob(os.path.join(input_folder, f"*{ext}")))
        video_files.extend(glob.glob(os.path.join(input_folder, f"*{ext.upper()}")))

    if not video_files:
        return {"status": "error", "message": f"No video files found in {input_folder}"}

    results = []
    success_count = 0
    error_count = 0

    for input_file in video_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_folder, filename)

        result = process_single(input_file, output_file, operation, **kwargs)
        results.append({"input": input_file, "output": output_file, "result": result})

        if result["status"] == "success":
            success_count += 1
        else:
            error_count += 1

    return {
        "status": "completed",
        "operation": operation,
        "total_files": len(video_files),
        "success_count": success_count,
        "error_count": error_count,
        "results": results,
    }


def process_single(input_file, output_file, operation, **kwargs):
    """Process a single video file"""
    if operation == "convert":
        format_ext = kwargs.get("format", "mp4")
        output_file = os.path.splitext(output_file)[0] + f".{format_ext}"
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-y",
            output_file,
        ]
    elif operation == "compress":
        preset = kwargs.get("preset", "default")
        preset_config = {
            "web": {"crf": 28, "preset": "fast"},
            "archive": {"crf": 18, "preset": "slow"},
            "default": {"crf": 23, "preset": "medium"},
        }.get(preset, {"crf": 23, "preset": "medium"})
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-c:v",
            "libx264",
            "-crf",
            str(preset_config["crf"]),
            "-preset",
            preset_config["preset"],
            "-c:a",
            "aac",
            "-y",
            output_file,
        ]
    elif operation == "resize":
        width = kwargs.get("width", None)
        height = kwargs.get("height", None)
        scale_filter = (
            f"{width}:{height}"
            if width and height
            else f"{width}:-1"
            if width
            else f"-1:{height}"
        )
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-vf",
            f"scale={scale_filter}",
            "-c:a",
            "copy",
            "-y",
            output_file,
        ]
    elif operation == "watermark":
        watermark = kwargs.get("wm", None)
        if not watermark or not os.path.exists(watermark):
            return {
                "status": "error",
                "message": f"Watermark file not found: {watermark}",
            }
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-i",
            watermark,
            "-filter_complex",
            "[1:v]format=rgba,colorchannelmixer=aa=0.7[wm];[0:v][wm]overlay=main_w-overlay_w-10:main_h-overlay_h-10",
            "-c:a",
            "copy",
            "-y",
            output_file,
        ]
    else:
        return {"status": "error", "message": f"Unknown operation: {operation}"}

    try:
        subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)
        return {"status": "success", "output": output_file}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}


def main():
    if len(sys.argv) < 5:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: batch_process_video.py input/ output/ --operation <convert|compress|resize|watermark> [options]",
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
        elif arg == "--width" and i + 1 < len(sys.argv):
            kwargs["width"] = int(sys.argv[i + 1])
        elif arg == "--height" and i + 1 < len(sys.argv):
            kwargs["height"] = int(sys.argv[i + 1])
        elif arg == "--wm" and i + 1 < len(sys.argv):
            kwargs["wm"] = sys.argv[i + 1]

    if not operation:
        print(json.dumps({"status": "error", "message": "--operation is required"}))
        sys.exit(1)

    result = batch_process(input_folder, output_folder, operation, **kwargs)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
