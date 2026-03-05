# ImageMagick Command Reference

This reference covers common ImageMagick commands and options used in the multimedia-tools skill.

## Basic Syntax

```
magick input_file [options] output_file
```

Note: Older versions use `convert` instead of `magick`.

## Format Conversion

### Convert between formats
```bash
magick input.jpg output.png
magick input.png output.webp
magick input.tiff output.jpg
```

### Convert with quality control
```bash
magick input.jpg -quality 85 output.jpg
```

## Resizing

### Resize to width (maintain aspect ratio)
```bash
magick input.jpg -resize 1920 output.jpg
```

### Resize to height (maintain aspect ratio)
```bash
magick input.jpg -resize x1080 output.jpg
```

### Resize to specific dimensions
```bash
magick input.jpg -resize 1920x1080! output.jpg  # Force exact dimensions
magick input.jpg -resize 1920x1080 output.jpg    # Maintain aspect ratio
```

### Resize by percentage
```bash
magick input.jpg -resize 50% output.jpg
magick input.jpg -resize 200% output.jpg
```

### Resize with limits
```bash
# Never larger than 1920x1080
magick input.jpg -resize 1920x1080> output.jpg

# Never smaller than 800x600
magick input.jpg -resize 800x600< output.jpg
```

## Cropping

### Crop to specific dimensions
```bash
magick input.jpg -crop 800x600+100+50 output.jpg
# Width: 800, Height: 600, X offset: 100, Y offset: 50
```

### Center crop
```bash
magick input.jpg -gravity center -crop 800x600+0+0 output.jpg
```

### Crop with gravity
```bash
# Top-left
magick input.jpg -gravity northwest -crop 800x600+0+0 output.jpg

# Bottom-right
magick input.jpg -gravity southeast -crop 800x600+0+0 output.jpg
```

### Reset page geometry after crop
```bash
magick input.jpg -crop 800x600+100+50 +repage output.jpg
```

## Quality Optimization

### Set JPEG quality
```bash
magick input.jpg -quality 85 output.jpg
```

### Strip metadata
```bash
magick input.jpg -strip output.jpg
```

### Optimize for web
```bash
magick input.jpg -strip -quality 85 -interlace none output.jpg
```

### Print quality
```bash
magick input.jpg -quality 95 -density 300x300 output.jpg
```

## Watermarking

### Add image watermark (southeast corner)
```bash
magick input.jpg watermark.png -gravity southeast -composite output.jpg
```

### Add watermark with opacity
```bash
magick input.jpg \( watermark.png -alpha set -channel A -evaluate multiply 0.5 +channel \) -gravity southeast -composite output.jpg
```

### Watermark positions
```bash
-gravity NorthWest   # Top-left
-gravity North        # Top-center
-gravity NorthEast   # Top-right
-gravity West         # Middle-left
-gravity Center       # Center
-gravity East         # Middle-right
-gravity SouthWest   # Bottom-left
-gravity South        # Bottom-center
-gravity SouthEast   # Bottom-right
```

### Add text watermark
```bash
magick input.jpg -pointsize 48 -fill white -gravity southeast -annotate +10+10 "Copyright 2024" output.jpg
```

## Color Operations

### Adjust brightness
```bash
magick input.jpg -modulate 120,100,100 output.jpg  # 20% brighter
magick input.jpg -modulate 80,100,100 output.jpg   # 20% darker
```

### Adjust contrast
```bash
magick input.jpg -modulate 100,120,100 output.jpg  # 20% more contrast
magick input.jpg -modulate 100,80,100 output.jpg   # 20% less contrast
```

### Adjust saturation
```bash
magick input.jpg -modulate 100,100,120 output.jpg  # 20% more saturated
magick input.jpg -modulate 100,100,80 output.jpg   # 20% less saturated
```

### Grayscale
```bash
magick input.jpg -grayscale Rec709 output.jpg
```

### Sepia tone
```bash
magick input.jpg -sepia-tone 80% output.jpg
```

## Filters and Effects

### Blur
```bash
magick input.jpg -blur 0x5 output.jpg  # Gaussian blur (radius 0, sigma 5)
```

### Sharpen
```bash
magick input.jpg -sharpen 0x2 output.jpg
```

### Vignette
```bash
magick input.jpg -vignette 0x50 output.jpg
```

### Border
```bash
magick input.jpg -border 10x10 -color white output.jpg
```

### Round corners
```bash
magick input.jpg \( +clone -alpha extract -draw 'fill black polygon 0,0 0,50 50,0' -flip -draw 'fill black polygon 0,0 50,0 0,50' -flop -draw 'fill black polygon 0,0 0,50 50,0' -rotate 180 -draw 'fill black polygon 0,0 50,0 0,50' \) -alpha off -compose CopyOpacity -composite output.jpg
```

## Transparency

### Add transparency
```bash
magick input.png -alpha set -channel A -evaluate multiply 0.5 output.png
```

### Remove transparency (flatten)
```bash
magick input.png -background white -alpha off output.jpg
```

### Convert to grayscale with transparency
```bash
magick input.png -type GrayscaleMatte output.png
```

## Batch Processing

### Process all images in directory
```bash
for f in *.jpg; do magick "$f" -resize 800 "resized_$f"; done
```

### Parallel processing
```bash
ls *.jpg | parallel -j 4 magick {} -resize 800 resized_{}
```

### Mogrify (modify in place)
```bash
# Resize all images in current directory
magick mogrify -resize 1920 *.jpg

# Convert format
magick mogrify -format png *.jpg
```

## Multi-Image Operations

### Create animated GIF
```bash
magick -delay 20 -loop 0 frame1.jpg frame2.jpg frame3.jpg output.gif
```

### Combine images side by side
```bash
magick left.jpg right.jpg +append output.jpg  # Vertical
magick left.jpg right.jpg -append output.jpg  # Horizontal
```

### Create montage
```bash
magick montage -tile 3x2 -geometry 200x200+5+5 *.jpg output.jpg
```

## Image Information

### Get detailed info
```bash
magick identify -verbose input.jpg
```

### Get basic info
```bash
magick identify input.jpg
```

### Get specific info
```bash
magick identify -format "%w x %h" input.jpg  # Width x Height
magick identify -format "%b" input.jpg      # File size
magick identify -format "%Q" input.jpg      # Quality
```

## Advanced

### Two-pass optimization
```bash
# First pass: gather info
magick input.jpg -write mpr:info +delete -write mpr:img null:

# Second pass: use info
magick mpr:img -strip -quality 85 output.jpg
```

### Resize and compress in one pass
```bash
magick input.jpg -resize 1920x -quality 85 -strip output.jpg
```

### Convert all images to WebP
```bash
magick mogrify -format webp -quality 85 *.jpg
```

## Performance Tips

1. **Limit memory**:
   ```bash
   -limit memory 256MB
   -limit map 512MB
   ```

2. **Use multithreading**:
   ```bash
   -limit thread 4
   ```

3. **Strip metadata** for web:
   ```bash
   -strip
   ```

4. **Use efficient formats**:
   ```bash
   # WebP for images with transparency
   # JPEG for photos
   # PNG for graphics with sharp edges
   ```

## Common Issues

### Quality loss on resize
Use proper filters:
```bash
magick input.jpg -filter Lanczos -resize 1920 output.jpg
```

### File size too large
Lower quality or strip metadata:
```bash
magick input.jpg -quality 75 -strip output.jpg
```

### Slow processing
Limit threads or use simpler filters.

## Official Documentation
- ImageMagick: https://imagemagick.org/script/command-line-options.php
- Examples: https://imagemagick.org/Usage/
