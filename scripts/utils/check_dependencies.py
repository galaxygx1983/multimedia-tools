#!/usr/bin/env python3
"""
Check dependencies for multimedia-tools
Verifies FFmpeg and ImageMagick installation
Usage: python check_dependencies.py
"""

import subprocess
import json
import sys
import os


def check_command(command, name):
    """Check if a command is available"""
    try:
        result = subprocess.run(
            [command, "-version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            return {"status": "installed", "version": version_line}
        return {"status": "not_installed", "version": None}
    except FileNotFoundError:
        return {"status": "not_installed", "version": None}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "version": None}
    except Exception as e:
        return {"status": "error", "version": str(e)}


def main():
    results = {}

    # Check FFmpeg
    results["ffmpeg"] = check_command("ffmpeg", "FFmpeg")

    # Check ImageMagick
    results["imagemagick"] = check_command("magick", "ImageMagick")

    # Check ffprobe (optional but useful)
    results["ffprobe"] = check_command("ffprobe", "FFprobe")

    # Determine overall status
    all_installed = all(
        r["status"] == "installed" for r in [results["ffmpeg"], results["imagemagick"]]
    )

    output = {
        "overall_status": "ready" if all_installed else "missing_dependencies",
        "dependencies": results,
    }

    if all_installed:
        output["message"] = "All dependencies installed and ready to use"
    else:
        missing = [k for k, v in results.items() if v["status"] != "installed"]
        output["message"] = f"Missing dependencies: {', '.join(missing)}"
        output["install_instructions"] = {
            "ffmpeg": "Install from https://ffmpeg.org/download.html",
            "imagemagick": "Install from https://imagemagick.org/script/download.php",
        }

    print(json.dumps(output, indent=2))

    # Return exit code based on status
    return 0 if all_installed else 1


if __name__ == "__main__":
    sys.exit(main())
