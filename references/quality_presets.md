# Quality Presets Guide

This guide explains the quality presets available in multimedia-tools and how to customize them.

## Video Presets

### Web Preset

**Purpose**: Optimize for web streaming and social media

**Configuration**:
- Codec: H.264 (libx264)
- CRF: 28
- Preset: fast
- Audio Codec: AAC
- Audio Bitrate: 128k
- Format: MP4, WebM

**Recommended Resolutions**:
- 720p (1280x720) - Standard web video
- 1080p (1920x1080) - HD web video

**Use Cases**:
- YouTube, Vimeo, other video platforms
- Social media (Facebook, Twitter, LinkedIn)
- Website embedding
- Email attachments

**File Size Impact**: ~50-70% reduction from source

**Example**:
```bash
python scripts/video/compress_video.py input.mp4 output.mp4 --preset web
```

### Archive Preset

**Purpose**: High quality for long-term storage

**Configuration**:
- Codec: H.264 (libx264)
- CRF: 18
- Preset: slow
- Audio Codec: AAC
- Audio Bitrate: 192k
- Format: MP4, MOV

**Recommended Resolutions**:
- 1080p (1920x1080) - Full HD archive
- 1440p (2560x1440) - 2K archive
- 2160p (3840x2160) - 4K archive

**Use Cases**:
- Family videos
- Project archives
- Professional footage
- Legal or medical records

**File Size Impact**: ~20-30% reduction from source

**Example**:
```bash
python scripts/video/compress_video.py input.mp4 output.mp4 --preset archive
```

### Default Preset

**Purpose**: Balanced quality and file size

**Configuration**:
- Codec: H.264 (libx264)
- CRF: 23
- Preset: medium
- Audio Codec: AAC
- Audio Bitrate: 128k
- Format: MP4

**Recommended Resolutions**:
- 720p (1280x720)
- 1080p (1920x1080)

**Use Cases**:
- General-purpose video
- Personal use
- Internal business use
- Not sure which preset to use

**File Size Impact**: ~40-50% reduction from source

**Example**:
```bash
python scripts/video/compress_video.py input.mp4 output.mp4 --preset default
```

## Image Presets

### Web Preset

**Purpose**: Optimize for web loading

**Configuration**:
- Quality: 85%
- Strip Metadata: Yes
- Interlace: No
- Format: JPEG, WebP

**Recommended Sizes**:
- 800px width - Blog posts
- 1200px width - Website content
- 1920px width - Hero images

**Use Cases**:
- Website images
- Blog posts
- Email newsletters
- Social media posts

**File Size Impact**: ~30-50% reduction from source

**Example**:
```bash
python scripts/image/compress_image.py photo.jpg output.jpg --preset web
```

### Print Preset

**Purpose**: High quality for printing

**Configuration**:
- Quality: 95%
- Strip Metadata: No
- Density: 300 DPI
- Format: PNG, TIFF

**Recommended**:
- Maintain original resolution or higher
- Minimum 300 DPI for print

**Use Cases**:
- Photo printing
- Brochures and flyers
- Business cards
- Professional publications

**File Size Impact**: Minimal (or larger) due to high quality

**Example**:
```bash
python scripts/image/compress_image.py photo.jpg output.jpg --preset print
```

### Thumbnail Preset

**Purpose**: Small preview images

**Configuration**:
- Quality: 75%
- Strip Metadata: Yes
- Recommended Width: 200px
- Format: JPEG, WebP

**Recommended Sizes**:
- 200px width - Small thumbnails
- 400px width - Medium thumbnails

**Use Cases**:
- Gallery thumbnails
- Preview images
- Profile pictures
- Icon images

**File Size Impact**: ~70-90% reduction from source

**Example**:
```bash
python scripts/image/compress_image.py photo.jpg thumb.jpg --preset thumbnail
```

### Default Preset

**Purpose**: Balanced quality and file size

**Configuration**:
- Quality: 85%
- Strip Metadata: Yes
- Format: JPEG, PNG

**Recommended Sizes**:
- 800px width - General web use
- 1920px width - Full-size images

**Use Cases**:
- General-purpose images
- Personal use
- Internal business use
- Not sure which preset to use

**File Size Impact**: ~30-50% reduction from source

**Example**:
```bash
python scripts/image/compress_image.py photo.jpg output.jpg --preset default
```

## Customizing Presets

### Modify Preset Configuration Files

Edit preset JSON files in `assets/presets/`:

**video_presets.json**:
```json
{
  "web": {
    "description": "Optimized for web streaming and social media",
    "video": {
      "codec": "libx264",
      "crf": 28,
      "preset": "fast",
      "audio_codec": "aac",
      "audio_bitrate": "128k"
    },
    "formats": ["mp4", "webm"],
    "recommended_resolutions": [720, 1080]
  }
}
```

**image_presets.json**:
```json
{
  "web": {
    "description": "Optimized for web loading",
    "quality": 85,
    "strip": true,
    "interlace": false,
    "formats": ["jpeg", "webp"],
    "recommended_sizes": [800, 1200, 1920]
  }
}
```

### Create Custom Presets

Add new presets to the JSON files:

**Custom video preset (e.g., for Instagram)**:
```json
{
  "instagram": {
    "description": "Optimized for Instagram Reels",
    "video": {
      "codec": "libx264",
      "crf": 26,
      "preset": "medium",
      "audio_codec": "aac",
      "audio_bitrate": "128k"
    },
    "formats": ["mp4"],
    "recommended_resolutions": [1080, 1920]
  }
}
```

**Custom image preset (e.g., for e-commerce)**:
```json
{
  "ecommerce": {
    "description": "E-commerce product images",
    "quality": 90,
    "strip": true,
    "formats": ["jpeg", "webp"],
    "recommended_sizes": [800, 1600]
  }
}
```

### Update Scripts to Use Custom Presets

After adding custom presets to JSON files, update `apply_preset.py`:

```python
VIDEO_PRESETS = {
    "web": {...},
    "archive": {...},
    "default": {...},
    "instagram": {...}  # Add custom preset
}
```

## Quality Trade-offs

### CRF Values Explained

| CRF | Quality | File Size | Use Case |
|-----|---------|-----------|----------|
| 0-18 | Lossless/Excellent | Very large | Archive, professional |
| 18-23 | Very Good | Large | High-quality content |
| 23-28 | Good | Medium | Standard web content |
| 28-34 | Fair | Small | Low-bandwidth scenarios |
| 34-51 | Poor | Very small | Preview/low-quality |

### Image Quality Explained

| Quality | Visual Difference | File Size | Use Case |
|---------|------------------|-----------|----------|
| 95-100 | None perceptible | Large | Print, archive |
| 85-95 | Very subtle | Medium | Professional web |
| 75-85 | Slightly perceptible | Small | Standard web |
| 65-75 | Noticeable | Very small | Thumbnails |
| <65 | Poor | Minimal | Preview only |

## Choosing the Right Preset

### Decision Tree

**Video**:
1. Is this for long-term storage? → **Archive**
2. Is this for web/social media? → **Web**
3. Not sure? → **Default**

**Image**:
1. Is this for printing? → **Print**
2. Is this a thumbnail? → **Thumbnail**
3. Is this for web? → **Web**
4. Not sure? → **Default**

### Platform-Specific Recommendations

| Platform | Video Preset | Image Preset |
|----------|--------------|--------------|
| YouTube | Web (CRF 28) | Web (85%) |
| Vimeo | Web (CRF 26) | Web (90%) |
| Instagram | Web (CRF 26) | Web (85%) |
| Facebook | Web (CRF 28) | Web (85%) |
| Twitter | Web (CRF 28) | Web (80%) |
| Email | Default (CRF 23) | Web (75%) |
| Print | Archive | Print |
| Backup | Archive | Default |

## Best Practices

### For Videos
1. Test presets on short clips first
2. Use higher CRF for talking head content
3. Use lower CRF for action/fast-motion content
4. Consider target bandwidth when choosing preset
5. Archive original files before compression

### For Images
1. Preserve originals before processing
2. Use WebP for images with transparency
3. Use JPEG for photographs
4. Use PNG for graphics with sharp edges
5. Test quality settings on sample images

## Monitoring Quality

### Visual Inspection
Always visually inspect processed files:
```bash
# Compare original and compressed
python scripts/video/compress_video.py original.mp4 test.mp4 --preset web
# Open original.mp4 and test.mp4 side by side
```

### File Size Monitoring
Track compression ratios:
```bash
# Get file sizes
ls -lh original.mp4 test.mp4
```

### Quality Metrics
Use tools to measure quality degradation:
- VMAF (Video Multi-Method Assessment Fusion)
- SSIM (Structural Similarity Index)
- PSNR (Peak Signal-to-Noise Ratio)
