# FFmpeg Command Reference

This reference covers common FFmpeg commands and options used in the multimedia-tools skill.

## Basic Syntax

```
ffmpeg [global_options] -i input_file [input_options] output_file [output_options]
```

## Common Video Codecs

| Codec | Command | Use Case |
|-------|---------|----------|
| H.264 | `-c:v libx264` | Most compatible, widely supported |
| H.265 | `-c:v libx265` | Better compression, less compatible |
| VP9 | `-c:v libvpx-vp9` | WebM format, good for web |
| AV1 | `-c:v libaom-av1` | Newest, best compression, slow |

## Common Audio Codecs

| Codec | Command | Use Case |
|-------|---------|----------|
| AAC | `-c:a aac` | Most compatible |
| MP3 | `-c:a libmp3lame` | Widely supported |
| Opus | `-c:a libopus` | Web audio, good quality |

## Quality Control

### CRF (Constant Rate Factor)
Controls video quality (lower = better quality, larger file):

```bash
# Range: 0-51 (18-28 is typical)
-crf 18  # High quality (archive)
-crf 23  # Default (balanced)
-crf 28  # Web quality
```

### Preset (Encoding Speed)
Controls encoding speed vs compression efficiency:

```bash
-preset ultrafast  # Fastest, largest file
-preset veryfast
-preset fast
-preset medium     # Default
-preset slow
-preset slower
-preset veryslow   # Slowest, smallest file
```

## Resolution/Scaling

### Scale to width, maintain aspect ratio
```bash
-vf scale=1280:-1
```

### Scale to height, maintain aspect ratio
```bash
-vf scale=-1:720
```

### Force exact dimensions
```bash
-vf scale=1280:720
```

## Trimming

### By start and end time
```bash
-ss 00:00:30 -to 00:01:30
```

### By start time and duration
```bash
-ss 00:00:30 -t 60
```

### Using filter (more precise)
```bash
-filter:v trim=start=30:end=90,setpts=PTS-STARTPTS
```

## Audio Operations

### Extract audio only
```bash
-vn  # No video
```

### Copy audio without re-encoding
```bash
-c:a copy
```

### Change audio codec
```bash
-c:a aac -b:a 128k
```

### Extract to separate file
```bash
ffmpeg -i input.mp4 -vn -acodec libmp3lame output.mp3
```

## Watermarking

### Add image watermark
```bash
-filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[wm];[0:v][wm]overlay=10:10"
```

### Watermark positions
```
10:10                    # Top-left
main_w-overlay_w-10:10    # Top-right
10:main_h-overlay_h-10    # Bottom-left
main_w-overlay_w-10:main_h-overlay_h-10  # Bottom-right
(main_w-overlay_w)/2:(main_h-overlay_h)/2  # Center
```

## Optimization

### Fast start (for web streaming)
```bash
-movflags +faststart
```

### Two-pass encoding (better quality)
```bash
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -pass 1 -f mp4 /dev/null

# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -pass 2 output.mp4
```

### Strip metadata
```bash`
-map_metadata -1
```

## Container Formats

### MP4 (most common)
```bash
-f mp4
-c:v libx264
-c:a aac
```

### WebM (web-optimized)
```bash
-f webm
-c:v libvpx-vp9
-c:a libopus
```

### MOV (Apple)
```bash
-f mov
-c:v libx264
-c:a aac
```

## Common Filters

### Rotate video
```bash
# 90 degrees clockwise
-vf transpose=1

# 90 degrees counter-clockwise
-vf transpose=2

# 180 degrees
-vf transpose=1,transpose=1
```

### Flip
```bash
# Horizontal flip
-vf hflip

# Vertical flip
-vf vflip
```

### Add fade
```bash
# Fade in (first 30 frames)
-vf fade=t=in:st=0:d=1

# Fade out (last 30 frames)
-vf fade=t=out:st=29:d=1
```

## Batch Processing

### Process multiple files
```bash
for f in *.avi; do ffmpeg -i "$f" "${f%.avi}.mp4"; done
```

### Parallel processing
```bash
ls *.avi | parallel -j 4 ffmpeg -i {} {.}.mp4
```

## Useful ffprobe Commands

### Get video info
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

### Get resolution only
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
```

### Get duration
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

## Performance Tips

1. **Use hardware acceleration** (if available):
   ```bash
   -c:v h264_nvenc  # NVIDIA
   -c:v h264_qsv    # Intel
   -c:v h264_amf    # AMD
   ```

2. **Limit memory usage**:
   ```bash
   -threads 4
   ```

3. **Disable audio for faster processing** (when not needed):
   ```bash
   -an
   ```

4. **Use faster preset for testing**:
   ```bash
   -preset ultrafast
   ```

## Common Issues

### Audio sync issues
Use `-async 1` or `-vsync 2` to fix audio sync.

### File too large
Increase CRF value (e.g., `-crf 32`) or use two-pass encoding.

### Poor quality
Decrease CRF value (e.g., `-crf 18`) or use slower preset.

## Official Documentation
- FFmpeg: https://ffmpeg.org/documentation.html
- FFprobe: https://ffmpeg.org/ffprobe.html
