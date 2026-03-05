#!/usr/bin/env python3
"""
Apply scenario-based quality presets for multimedia processing
Usage: python apply_preset.py --type video --preset web
       python apply_preset.py --type image --preset print
"""

import json
import sys
import os

# Preset configurations
VIDEO_PRESETS = {
    "web": {
        "description": "Optimized for web streaming and social media",
        "codec": "libx264",
        "crf": 28,
        "preset": "fast",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
    },
    "archive": {
        "description": "High quality for long-term storage",
        "codec": "libx264",
        "crf": 18,
        "preset": "slow",
        "audio_codec": "aac",
        "audio_bitrate": "192k",
    },
    "default": {
        "description": "Balanced quality and file size",
        "codec": "libx264",
        "crf": 23,
        "preset": "medium",
        "audio_codec": "aac",
        "audio_bitrate": "128k",
    },
}

IMAGE_PRESETS = {
    "web": {
        "description": "Optimized for web loading",
        "quality": 85,
        "strip": True,
        "interlace": False,
    },
    "print": {
        "description": "High quality for printing",
        "quality": 95,
        "strip": False,
        "density": 300,
    },
    "thumbnail": {
        "description": "Small preview images",
        "quality": 75,
        "strip": True,
        "recommended_width": 200,
    },
    "default": {
        "description": "Balanced quality and file size",
        "quality": 85,
        "strip": True,
    },
}


def apply_preset(media_type, preset_name):
    """Apply scenario-based preset and return configuration"""
    if media_type == "video":
        presets = VIDEO_PRESETS
    elif media_type == "image":
        presets = IMAGE_PRESETS
    else:
        return {
            "status": "error",
            "message": f"Invalid media type: {media_type}. Use 'video' or 'image'.",
        }

    if preset_name not in presets:
        available = ", ".join(presets.keys())
        return {
            "status": "error",
            "message": f"Preset '{preset_name}' not found. Available presets: {available}",
        }

    return {
        "status": "success",
        "media_type": media_type,
        "preset": preset_name,
        "config": presets[preset_name],
    }


def main():
    if "--help" in sys.argv or len(sys.argv) < 5:
        print(__doc__)
        print("\nAvailable video presets:", ", ".join(VIDEO_PRESETS.keys()))
        print("Available image presets:", ", ".join(IMAGE_PRESETS.keys()))
        return 0

    # Parse arguments
    media_type = None
    preset_name = None

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--type" and i + 1 < len(sys.argv):
            media_type = sys.argv[i + 1].lower()
        elif arg == "--preset" and i + 1 < len(sys.argv):
            preset_name = sys.argv[i + 1].lower()

    if not media_type or not preset_name:
        print(
            json.dumps(
                {"status": "error", "message": "Both --type and --preset are required"}
            )
        )
        return 1

    result = apply_preset(media_type, preset_name)
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
