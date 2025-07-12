# 🤖 AI-Powered Media Processor (AWS Lambda + Rekognition)

Automatically process images, audio, and video uploaded to Amazon S3 using AWS Lambda, Pillow, FFmpeg, and Amazon Rekognition.



---

## 📌 Project Overview

This project demonstrates a **real-world, serverless media processing pipeline** with integrated AI capabilities. Supports image resizing, audio/video conversion, and intelligent labeling using Rekognition.

---

## 🛠️ Tech Stack

- AWS Lambda (Python 3.9)
- Amazon S3
- Amazon Rekognition
- FFmpeg (Static Layer)
- Pillow (Image Layer)
- IAM + VPC + CloudWatch

---

## 🚀 Features

- ✅ Image resizing and conversion to `.jpg`
- 🧠 AI labeling using Rekognition
- 🎵 Audio: `.wav` → `.mp3` with FFmpeg
- 🎥 Video: `.mov` / `.avi` → `.mp4` with FFmpeg
- ❌ Graceful handling of unsupported formats
- 🔁 Handles multiple S3 records per trigger

---

## 📂 Folder Structure

```
.
├── lambda/
│   ├── image_processor.py
│   ├── audio_processor.py
│   └── video_processor.py
├── layers/
│   ├── pillow-layer.zip
│   └── ffmpeg-layer.zip
├── README.md
└── architecture.png
```

---

## 🧠 AI Integration

Amazon Rekognition is used to automatically tag images with descriptive labels.\
Sample output:

```json
{
  "Labels": [
    { "Name": "Dog", "Confidence": 99.2 },
    { "Name": "Pet", "Confidence": 97.5 }
  ]
}
```

---

## 🔐 Security

- IAM Roles with Least Privilege
- Lambda runs inside a custom VPC
- CloudWatch for detailed logs
- Public access disabled on S3 buckets

---

## ✅ How to Deploy

1. Upload ZIP layers (`pillow-layer.zip`, `ffmpeg-layer.zip`) to S3
2. Create Lambda functions and attach the layers
3. Set IAM policies and test with sample S3 events

---

## 📄 License

MIT License — free to use and modify!

---

## 🙋‍♂️ Author

**Prabhu S.**\
Cloud & Security Enthusiast | [Cloudica.in](https://cloudica.in)

