# Multimedia Tools

> Video/audio/image processing using FFmpeg & ImageMagick

## 功能特性

### 视频处理 (FFmpeg)
- 格式转换: MP4, WebM, MOV, AVI, MKV
- 视频压缩与优化
- 视频裁剪与合并
- 音频提取
- 缩略图生成

### 图像处理 (ImageMagick)
- 格式转换: JPEG, PNG, WebP, GIF, TIFF, BMP
- 图片压缩与调整大小
- 水印添加
- 批量处理

## 安装依赖

```bash
# FFmpeg
# macOS: brew install ffmpeg
# Windows: https://ffmpeg.org/download.html
# Linux: apt install ffmpeg

# ImageMagick
# macOS: brew install imagemagick
# Windows: https://imagemagick.org/script/download.php
# Linux: apt install imagemagick
```

## 快速开始

```bash
# 视频转换
ffmpeg -i input.mov output.mp4

# 视频压缩
ffmpeg -i input.mp4 -crf 28 output.mp4

# 图片转换
magick convert input.png output.jpg

# 图片调整大小
magick convert input.jpg -resize 800x600 output.jpg
```

## 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用指南。

## 许可证

MIT License