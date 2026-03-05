# Troubleshooting Guide

This guide helps you diagnose and resolve common issues when using multimedia-tools.

## Installation Issues

### FFmpeg Not Found

**Symptom**:
```
ffmpeg: command not found
```

**Solution**:
1. Install FFmpeg from https://ffmpeg.org/download.html
2. Add FFmpeg to your PATH
3. Verify installation:
   ```bash
   ffmpeg -version
   ```

**Windows**:
- Download build from https://www.gyan.dev/ffmpeg/builds/
- Extract and add `bin` folder to PATH
- Restart terminal

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

### ImageMagick Not Found

**Symptom**:
```
magick: command not found
```

**Solution**:
1. Install ImageMagick from https://imagemagick.org/script/download.php
2. Verify installation:
   ```bash
   magick -version
   ```

**Windows**:
- Download installer from ImageMagick website
- Run installer and check "Install legacy utilities" option
- Restart terminal

**macOS**:
```bash
brew install imagemagick
```

**Linux**:
```bash
sudo apt install imagemagick  # Ubuntu/Debian
sudo yum install imagemagick  # CentOS/RHEL
```

### Check All Dependencies

Run the dependency check script:
```bash
python scripts/utils/check_dependencies.py
```

## Video Processing Issues

### Video Not Playing After Conversion

**Possible Causes**:
1. Codec not supported by player
2. Container format issue
3. Audio codec issue

**Solutions**:
```bash
# Use more compatible codec
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -c:a aac output.mp4

# Check what codecs your file uses
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 input.mp4
```

### Audio Out of Sync

**Symptom**: Video and audio don't match after processing

**Solutions**:
```bash
# Fix audio sync
ffmpeg -i input.mp4 -async 1 output.mp4

# Use more stable sync method
ffmpeg -i input.mp4 -vsync 2 output.mp4
```

### Poor Video Quality

**Symptom**: Compressed video looks blocky or blurry

**Solutions**:
1. Lower CRF value (better quality):
   ```bash
   python scripts/video/compress_video.py input.mp4 output.mp4 --preset default  # CRF 23
   # Or manually with lower CRF
   ffmpeg -i input.mp4 -crf 18 output.mp4
   ```

2. Use slower preset (better compression):
   ```bash
   ffmpeg -i input.mp4 -preset slow output.mp4
   ```

3. Use two-pass encoding:
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -pass 1 -f mp4 /dev/null
   ffmpeg -i input.mp4 -c:v libx264 -pass 2 output.mp4
   ```

### File Size Too Large

**Symptom**: Compressed file is still too big

**Solutions**:
1. Increase CRF value:
   ```bash
   ffmpeg -i input.mp4 -crf 30 output.mp4
   ```

2. Reduce resolution:
   ```bash
   python scripts/video/resize_video.py input.mp4 output.mp4 --width 1280
   ```

3. Reduce audio bitrate:
   ```bash
   ffmpeg -i input.mp4 -b:a 96k output.mp4
   ```

### Processing Too Slow

**Symptom**: Encoding takes too long

**Solutions**:
1. Use faster preset:
   ```bash
   ffmpeg -i input.mp4 -preset fast output.mp4
   ```

2. Use hardware acceleration (if available):
   ```bash
   # NVIDIA
   ffmpeg -i input.mp4 -c:v h264_nvenc output.mp4

   # Intel
   ffmpeg -i input.mp4 -c:v h264_qsv output.mp4

   # AMD
   ffmpeg -i input.mp4 -c:v h264_amf output.mp4
   ```

3. Limit threads:
   ```bash
   ffmpeg -i input.mp4 -threads 4 output.mp4
   ```

## Image Processing Issues

### Image Quality Loss

**Symptom**: Compressed image looks pixelated or has artifacts

**Solutions**:
1. Increase quality value:
   ```bash
   python scripts/image/compress_image.py input.jpg output.jpg --quality 90
   ```

2. Use better quality format:
   ```bash
   magick input.jpg -quality 95 output.png
   ```

3. Disable interlacing:
   ```bash
   magick input.jpg -interlace none output.jpg
   ```

### File Size Too Large

**Symptom**: Image file is too large for web

**Solutions**:
1. Reduce quality:
   ```bash
   python scripts/image/compress_image.py input.jpg output.jpg --quality 75
   ```

2. Strip metadata:
   ```bash
   python scripts/image/compress_image.py input.jpg output.jpg --preset web
   ```

3. Resize image:
   ```bash
   python scripts/image/resize_image.py input.jpg output.jpg --width 1920
   ```

4. Convert to WebP (better compression):
   ```bash
   magick input.jpg output.webp -quality 85
   ```

### Transparency Lost After Conversion

**Symptom**: PNG with transparency converted to JPEG loses transparency

**Solution**: Use PNG or WebP format instead:
```bash
magick input.png output.png  # Keep PNG format
magick input.png output.webp  # Or use WebP
```

### Colors Appear Different

**Symptom**: Image colors don't match after conversion

**Solutions**:
1. Maintain colorspace:
   ```bash
   magick input.jpg -colorspace sRGB output.jpg
   ```

2. Disable profile conversion:
   ```bash
   magick input.jpg -profile "*" output.jpg
   ```

3. Use correct color profile:
   ```bash
   magick input.jpg -profile sRGB.icc output.jpg
   ```

## Batch Processing Issues

### Some Files Failed to Process

**Symptom**: Batch processing reports errors for some files

**Solutions**:
1. Check file permissions
2. Verify file formats are supported
3. Check for corrupted files:
   ```bash
   ffmpeg -v error -i input.mp4 -f null -
   magick identify -verbose input.jpg
   ```

4. Process files individually to identify issue:
   ```bash
   for file in *.mp4; do
     echo "Processing $file"
     python scripts/video/compress_video.py "$file" "compressed_$file"
   done
   ```

### Out of Memory During Batch Processing

**Symptom**: System runs out of memory during batch operations

**Solutions**:
1. Process smaller batches:
   ```bash
   # Process first 10 files
   ls *.jpg | head -10 | while read f; do
     magick "$f" -resize 1920 "resized_$f"
   done
   ```

2. Limit memory usage (ImageMagick):
   ```bash
   magick input.jpg -limit memory 512MB -limit map 1GB output.jpg
   ```

3. Use parallel processing with fewer threads:
   ```bash
   ls *.jpg | parallel -j 2 magick {} -resize 1920 resized_{}
   ```

### Output Files in Wrong Location

**Symptom**: Processed files not in expected directory

**Solutions**:
1. Verify output directory exists:
   ```bash
   mkdir -p output_directory
   ```

2. Use absolute paths:
   ```bash
   python scripts/image/batch_process_image.py /full/path/input/ /full/path/output/ --operation resize --width 1920
   ```

3. Check directory permissions

## Watermarking Issues

### Watermark Not Visible

**Symptom**: Watermark added but not visible in output

**Solutions**:
1. Check opacity value:
   ```bash
   # Increase opacity
   python scripts/image/add_watermark.py photo.jpg wm.png output.jpg --opacity 100
   ```

2. Check position (might be off-screen):
   ```bash
   # Try different position
   python scripts/image/add_watermark.py photo.jpg wm.png output.jpg --position center
   ```

3. Check watermark file size:
   ```bash
   magick identify wm.png
   ```

### Watermark Distorted

**Symptom**: Watermark appears stretched or distorted

**Solutions**:
1. Maintain aspect ratio when resizing watermark
2. Use proper scaling:
   ```bash
   magick wm.png -resize 300x wm_resized.png
   ```

3. Use original watermark without forced dimensions

## Performance Issues

### Script Hangs or Freezes

**Symptom**: Script stops responding during processing

**Solutions**:
1. Check system resources (CPU, memory, disk)
2. Try processing a smaller file
3. Run with timeout:
   ```bash
   timeout 300 python scripts/video/compress_video.py input.mp4 output.mp4
   ```

4. Check for file locks or permissions

### Slow Performance on Large Files

**Symptom**: Large files take extremely long to process

**Solutions**:
1. Use faster preset
2. Reduce resolution first, then compress
3. Process in chunks (for videos)
4. Consider using hardware acceleration

## Debugging Tips

### Enable Verbose Output

**FFmpeg**:
```bash
ffmpeg -v verbose -i input.mp4 output.mp4
```

**ImageMagick**:
```bash
magick input.jpg -verbose output.jpg
```

### Check File Information

**Video**:
```bash
python scripts/utils/get_video_info.py input.mp4
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

**Image**:
```bash
python scripts/utils/get_image_info.py input.jpg
magick identify -verbose input.jpg
```

### Test with Simple Commands

Start with basic operations to isolate the issue:
```bash
# Test FFmpeg basic conversion
ffmpeg -i input.mp4 test.mp4

# Test ImageMagick basic conversion
magick input.jpg test.jpg
```

## Getting Help

### Useful Resources

1. **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
2. **ImageMagick Documentation**: https://imagemagick.org/Usage/
3. **FFmpeg Wiki**: https://trac.ffmpeg.org/wiki
4. **Stack Overflow**: Search for specific error messages

### Collect Information for Support

When reporting issues, include:

1. Command used
2. Error message
3. File information:
   ```bash
   ffprobe input.mp4
   magick identify input.jpg
   ```
4. System information:
   ```bash
   ffmpeg -version
   magick -version
   python --version
   ```
5. Sample file (if possible and non-sensitive)
