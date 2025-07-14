# 🤖 AI-Powered Media Processor (Phase 1 & 2)

Automatically process images, audio, and video uploaded to Amazon S3 using AWS Lambda, Pillow, FFmpeg, Amazon Rekognition, and Event Trigger Chaining.

---

## 📌 Project Overview

This project demonstrates a **real-world, serverless media processing pipeline** with integrated AI capabilities. It supports image resizing, audio/video conversion, intelligent labeling using Rekognition, and advanced asynchronous orchestration between Lambda functions using SNS.

---

## 🛠️ Tech Stack

- AWS Lambda (Python 3.9)
- Amazon S3
- Amazon Rekognition
- AWS SNS (Event Chaining)
- FFmpeg (Static Layer)
- Pillow (Image Layer)
- IAM + VPC + CloudWatch

---

## 🚀 Features

- ✅ Image resizing and conversion to `.jpg`
- 🧠 AI labeling using Rekognition
- 🎵 Audio: `.wav` → `.mp3` with FFmpeg
- 🎥 Video: `.mov` / `.avi` → `.mp4` with FFmpeg
- 📦 Frame capture and label storage for videos
- 🔁 Asynchronous workflow using SNS topic chaining
- ❌ Graceful handling of unsupported formats
- 🔁 Handles multiple S3 records per trigger

---

## 📂 Folder Structure

```
.
├── lambda/
│   ├── image_processor.py
│   ├── audio_processor.py
│   ├── video_converter.py
│   ├── video_ai_analyzer.py
├── layers/
│   ├── pillow-layer.zip
│   └── ffmpeg-layer.zip
├── README.md
└── architecture-phase2.png
```

---

## 🧠 AI Integration

### 📷 Image Recognition

Amazon Rekognition automatically tags images with descriptive labels:

```json
{
  "Labels": [
    { "Name": "Dog", "Confidence": 99.2 },
    { "Name": "Pet", "Confidence": 97.5 }
  ]
}
```

### 🎥 Video AI Analysis (Asynchronous)

- Uses `start_label_detection()`
- Results received via SNS → Triggers a second Lambda
- Saves labels in `labels/` and frames to `thumbnails/` (future scope)

---

## 🔄 Event Chaining with SNS

- **Lambda 1 (Conversion)**: Converts video → triggers Rekognition
- **Lambda 2 (AI Post-Processing)**: Triggered via SNS notification from Rekognition → stores label results

---

## 🔐 Security

- IAM Roles with Least Privilege
- Lambda inside custom VPC
- S3 access policies and bucket logging
- Resource-based policy on SNS for Lambda subscription

---

## ✅ How to Deploy

1. Upload ZIP layers (`pillow-layer.zip`, `ffmpeg-layer.zip`) to S3
2. Create Lambda functions and attach layers
3. Subscribe Lambda 2 to Rekognition SNS Topic
4. Set IAM and SNS permissions
5. Test with image/audio/video uploads

---

## 📄 License

MIT License — free to use and modify!

---

## 🙋‍♂️ Author

**Prabhu S.**\
Cloud & Security Enthusiast | [Cloudica.in](https://cloudica.in)

