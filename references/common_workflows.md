# Common Workflows

This guide provides step-by-step workflows for common multimedia processing tasks.

## Video Workflows

### Prepare Video for Web

Optimize video for web streaming and social media:

```bash
# Compress with web preset
python scripts/video/compress_video.py input.mp4 output.mp4 --preset web

# Resize to 1080p
python scripts/video/resize_video.py input.mp4 output.mp4 --width 1920

# Add watermark
python scripts/video/add_watermark.py output.mp4 watermark.png final.mp4 --opacity 0.3
```

### Create Video Archive

High-quality compression for long-term storage:

```bash
# Compress with archive preset
python scripts/video/compress_video.py input.mp4 archive.mp4 --preset archive

# Verify quality
python scripts/utils/get_video_info.py archive.mp4
```

### Extract Audio for Podcast

Extract and convert audio from video:

```bash
# Extract to MP3
python scripts/video/extract_audio.py video.mp4 audio.mp3

# Extract to WAV (for editing)
python scripts/video/extract_audio.py video.mp4 audio.wav --codec pcm_s16le
```

### Create Video Compilation

Combine multiple video clips:

```bash
# Using FFmpeg concat
# First, create file list:
# file 'clip1.mp4'
# file 'clip2.mp4'
# file 'clip3.mp4'

ffmpeg -f concat -i filelist.txt -c copy output.mp4
```

### Extract Frames for Analysis

Extract video frames as images:

```bash
# Extract one frame per second
ffmpeg -i video.mp4 -vf fps=1 out%d.png

# Extract specific frame
ffmpeg -i video.mp4 -vf "select='eq(n,100)'" -vsync vfr frame100.png
```

## Image Workflows

### Prepare Images for Website

Optimize images for web:

```bash
# Resize and compress
python scripts/image/resize_image.py photo.jpg web.jpg --width 1920
python scripts/image/compress_image.py web.jpg web_opt.jpg --preset web

# Convert to WebP
python scripts/image/convert_image.py web_opt.jpg web_opt.webp --quality 85
```

### Create Thumbnail Gallery

Generate multiple thumbnail sizes:

```bash
# Small thumbnail (200px)
python scripts/image/resize_image.py photo.jpg thumb_small.jpg --width 200

# Medium thumbnail (400px)
python scripts/image/resize_image.py photo.jpg thumb_medium.jpg --width 400

# Large thumbnail (800px)
python scripts/image/resize_image.py photo.jpg thumb_large.jpg --width 800
```

### Prepare Images for Print

Optimize images for printing:

```bash
# Compress with print preset (300 DPI, 95% quality)
python scripts/image/compress_image.py photo.jpg print.jpg --preset print

# Verify dimensions
python scripts/utils/get_image_info.py print.jpg
```

### Batch Optimize Photo Library

Process entire photo directory:

```bash
# Convert to JPEG and compress
python scripts/image/batch_process_image.py photos/ optimized/ --operation compress --preset web

# Resize to standard width
python scripts/image/batch_process_image.py photos/ resized/ --operation resize --width 1920
```

### Add Watermark to Photo Library

Batch watermarking:

```bash
python scripts/image/batch_process_image.py photos/ watermarked/ --operation watermark --wm logo.png --position southeast --opacity 60
```

### Create Contact Sheet

Generate image grid for preview:

```bash
magick montage -tile 4x3 -geometry 200x200+5+5 -background white photos/*.jpg contact_sheet.jpg
```

## Multi-Format Workflows

### Convert Video Thumbnails

Generate thumbnail from video:

```bash
# Extract frame at 30 seconds
ffmpeg -i video.mp4 -ss 00:00:30 -vframes 1 thumbnail.jpg

# Create animated GIF preview
ffmpeg -i video.mp4 -vf scale=320:-1 -t 5 preview.gif
```

### Create Social Media Content

Generate content for different platforms:

```bash
# Instagram Reels (9:16)
python scripts/video/resize_video.py video.mp4 reel.mp4 --width 1080 --height 1920

# YouTube (16:9)
python scripts/video/resize_video.py video.mp4 youtube.mp4 --width 1920 --height 1080

# Instagram Post (1:1)
python scripts/image/resize_image.py photo.jpg square.jpg --width 1080 --height 1080
```

### Create Video with Image Sequence

Convert image sequence to video:

```bash
ffmpeg -framerate 30 -i img%04d.jpg -c:v libx264 -preset medium -crf 23 output.mp4
```

### Create GIF from Video

Create animated GIF from video:

```bash
# Extract frames and create GIF
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1" -c:v gif output.gif

# Better quality with palette
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Quality Control Workflows

### Compare Video Quality

Compare different compression settings:

```bash
# Compress at different CRF values
python scripts/video/compress_video.py input.mp4 crf18.mp4 --preset archive
python scripts/video/compress_video.py input.mp4 crf23.mp4 --preset default
python scripts/video/compress_video.py input.mp4 crf28.mp4 --preset web

# Compare file sizes
ls -lh crf*.mp4
```

### Compare Image Quality

Compare different quality settings:

```bash
# Test quality levels
magick input.jpg -quality 75 test75.jpg
magick input.jpg -quality 85 test85.jpg
magick input.jpg -quality 95 test95.jpg

# Side-by-side comparison
magick test75.jpg test85.jpg test95.jpg +append comparison.jpg
```

### Validate Batch Processing

Check batch processing results:

```bash
# Run batch processing
python scripts/image/batch_process_image.py input/ output/ --operation convert --format png

# Check results
ls -l output/

# Verify a few outputs
python scripts/utils/get_image_info.py output/file1.png
python scripts/utils/get_image_info.py output/file2.png
```

## Cleanup and Optimization

### Remove Metadata

Strip sensitive or unnecessary metadata:

```bash
# Video
ffmpeg -i input.mp4 -map_metadata -1 output.mp4

# Images
python scripts/image/compress_image.py input.jpg output.jpg --preset web  # Automatically strips
```

### Optimize File Structure

Organize processed files:

```bash
# Create organized directory structure
mkdir -p originals/{videos,images}
mkdir -p processed/{videos,images}/{web,archive,print}
mkdir -p thumbnails/{videos,images}
```

### Backup Before Processing

Always backup originals:

```bash
# Create backup
cp -r originals/ originals_backup_$(date +%Y%m%d)

# Process from backup
python scripts/video/batch_process_video.py originals_backup/videos/ processed/videos/ --operation compress --preset web
```

## Automation Scripts

### Daily Media Processing

Automate daily processing tasks:

```bash
#!/bin/bash
# daily_process.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="backup_$DATE"
PROCESSED_DIR="processed_$DATE"

# Backup
mkdir -p "$BACKUP_DIR"
cp -r originals/* "$BACKUP_DIR/"

# Process
python scripts/video/batch_process_video.py "$BACKUP_DIR/videos/" "$PROCESSED_DIR/videos/" --operation compress --preset web
python scripts/image/batch_process_image.py "$BACKUP_DIR/images/" "$PROCESSED_DIR/images/" --operation compress --preset web

echo "Processing complete: $PROCESSED_DIR"
```

### Weekly Archive

Weekly high-quality archiving:

```bash
#!/bin/bash
# weekly_archive.sh

WEEK=$(date +%Y%V)
ARCHIVE_DIR="archive_week_$WEEK"

mkdir -p "$ARCHIVE_DIR"

# Archive videos
python scripts/video/batch_process_video.py originals/videos/ "$ARCHIVE_DIR/videos/" --operation compress --preset archive

# Archive images
python scripts/image/batch_process_image.py originals/images/ "$ARCHIVE_DIR/images/" --operation compress --preset print
```

## Troubleshooting Workflows

### Test Processing on Small Sample

Before processing large batches:

```bash
# Create test directory
mkdir -p test/{input,output}

# Copy sample files
cp originals/videos/sample1.mp4 test/input/
cp originals/images/photo1.jpg test/input/

# Test processing
python scripts/video/compress_video.py test/input/sample1.mp4 test/output/sample1.mp4 --preset web
python scripts/image/compress_image.py test/input/photo1.jpg test/output/photo1.jpg --preset web

# Verify results
python scripts/utils/get_video_info.py test/output/sample1.mp4
python scripts/utils/get_image_info.py test/output/photo1.jpg
```

### Diagnose Issues

Get detailed information about problematic files:

```bash
# Video info
python scripts/utils/get_video_info.py problem_video.mp4

# Image info
python scripts/utils/get_image_info.py problem_image.jpg

# Check dependencies
python scripts/utils/check_dependencies.py
```
