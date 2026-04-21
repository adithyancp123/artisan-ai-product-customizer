# 🎨 Artisan AI – Product Customization Platform

> AI-powered product customization platform for generating hyper-realistic wearable mockups using asynchronous rendering pipelines.

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-Backend-green?style=for-the-badge&logo=django)
![Celery](https://img.shields.io/badge/Celery-Async-success?style=for-the-badge&logo=celery)
![Redis](https://img.shields.io/badge/Redis-Queue-red?style=for-the-badge&logo=redis)
![Bootstrap](https://img.shields.io/badge/Bootstrap-UI-purple?style=for-the-badge&logo=bootstrap)
![OpenCV](https://img.shields.io/badge/OpenCV-Image_Processing-orange?style=for-the-badge&logo=opencv)

---

## 🚀 Live Concept

Artisan AI allows users to upload logos, graphics, or custom artwork and preview them on wearable products like t-shirts with realistic placement, perspective warping, and rendering.

The platform uses a scalable async architecture powered by Celery + Redis for background image generation.

---

## ✨ Key Features

✅ Upload custom logos/designs  
✅ Hyper-realistic product mockups  
✅ Fabric-aware image warping  
✅ Multi-angle preview generation  
✅ Background rendering queue with Celery  
✅ Fast task processing with Redis  
✅ Responsive premium UI  
✅ Django-powered backend architecture  

---

## 🧠 Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Backend | Django |
| Queue System | Celery |
| Message Broker | Redis |
| Image Processing | OpenCV, Pillow |
| Database | SQLite (default) |
| Dev Environment | Windows / PowerShell |

---

## 🏗️ System Architecture

```text
User Uploads Design
       ↓
Django Receives Request
       ↓
Celery Sends Task to Queue
       ↓
Redis Manages Background Jobs
       ↓
OpenCV Processes Mockup
       ↓
Rendered Image Returned to UI
