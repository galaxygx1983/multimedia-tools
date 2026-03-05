#!/usr/bin/env python3
"""
Get video metadata using ffprobe
Usage: python get_video_info.py video.mp4
"""

import subprocess
import json
import sys
import os


def get_video_info(input_file):
    """
    Extract metadata from video file

    Args:
        input_file: Path to video file
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"File not found: {input_file}"}

    # Get format information
    format_cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        input_file,
    ]

    # Get stream information
    stream_cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        input_file,
    ]

    try:
        format_result = subprocess.run(
            format_cmd, capture_output=True, encoding="utf-8", check=True
        )
        stream_result = subprocess.run(
            stream_cmd, capture_output=True, encoding="utf-8", check=True
        )

        format_data = json.loads(format_result.stdout)
        stream_data = json.loads(stream_result.stdout)

        # Extract video stream info
        video_stream = None
        audio_stream = None

        for stream in stream_data.get("streams", []):
            if stream["codec_type"] == "video":
                video_stream = stream
            elif stream["codec_type"] == "audio":
                audio_stream = stream

        # Build response
        info = {
            "status": "success",
            "file": input_file,
            "format": {
                "format_name": format_data.get("format", {}).get("format_name"),
                "duration": float(format_data.get("format", {}).get("duration", 0)),
                "size": int(format_data.get("format", {}).get("size", 0)),
                "bit_rate": int(format_data.get("format", {}).get("bit_rate", 0)),
            },
        }

        if video_stream:
            info["video"] = {
                "codec": video_stream.get("codec_name"),
                "width": video_stream.get("width"),
                "height": video_stream.get("height"),
                "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                "bit_rate": int(video_stream.get("bit_rate", 0)),
            }

        if audio_stream:
            info["audio"] = {
                "codec": audio_stream.get("codec_name"),
                "sample_rate": int(audio_stream.get("sample_rate", 0)),
                "channels": audio_stream.get("channels"),
                "bit_rate": int(audio_stream.get("bit_rate", 0)),
            }

        return info

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"status": "error", "message": "Usage: get_video_info.py video_file"}
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    result = get_video_info(input_file)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
