#!/usr/bin/env python3
"""
Trim video by time range using FFmpeg
Usage: python trim_video.py input.mp4 output.mp4 --start 00:00:30 --end 00:01:30
       python trim_video.py input.mp4 output.mp4 --start 00:00:00 --duration 00:00:30
"""

import subprocess
import json
import sys
import os


def parse_time_to_seconds(time_str):
    """Convert time string (HH:MM:SS or seconds) to seconds"""
    if time_str is None:
        return 0
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    return int(time_str)


def trim_video(input_file, output_file, start=None, end=None, duration=None):
    """
    Trim video by time range

    Args:
        input_file: Path to input video
        output_file: Path to output video
        start: Start time (HH:MM:SS or MM:SS or seconds)
        end: End time (HH:MM:SS or MM:SS or seconds)
        duration: Duration in seconds (alternative to end)
    """
    if not os.path.exists(input_file):
        return {"status": "error", "message": f"Input file not found: {input_file}"}

    if not start:
        return {"status": "error", "message": "--start is required"}

    if not end and not duration:
        return {"status": "error", "message": "Either --end or --duration is required"}

    # Convert time format to seconds
    start_sec = parse_time_to_seconds(start)

    # Build time filter
    if duration:
        duration_sec = parse_time_to_seconds(duration)
        # Video-only filter
        time_filter = f"[0:v]trim=start={start_sec}:duration={duration_sec},setpts=PTS-STARTPTS[v]"
        cmd_base = ["-filter_complex", time_filter, "-map", "[v]"]
    else:
        end_sec = parse_time_to_seconds(end)
        # Video-only filter
        time_filter = (
            f"[0:v]trim=start={start_sec}:end={end_sec},setpts=PTS-STARTPTS[v]"
        )
        cmd_base = ["-filter_complex", time_filter, "-map", "[v]"]

    cmd = (
        [
            "ffmpeg",
            "-i",
            input_file,
        ]
        + cmd_base
        + [
            "-c:v",
            "libx264",
            "-an",  # No audio
            "-y",
            output_file,
        ]
    )

    try:
        subprocess.run(cmd, capture_output=True, encoding="utf-8", check=True)

        return {
            "status": "success",
            "output": output_file,
            "operation": "trim",
            "start": start,
            "end": end,
            "duration": duration,
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr, "error_code": e.returncode}


def main():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": "Usage: trim_video.py input output --start TIME [--end TIME | --duration SECONDS]",
                }
            )
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    start = None
    end = None
    duration = None

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--start" and i + 1 < len(sys.argv):
            start = sys.argv[i + 1]
        elif arg == "--end" and i + 1 < len(sys.argv):
            end = sys.argv[i + 1]
        elif arg == "--duration" and i + 1 < len(sys.argv):
            duration = sys.argv[i + 1]

    result = trim_video(input_file, output_file, start, end, duration)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
