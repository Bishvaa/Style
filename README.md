---
title: StyleSense
emoji: 👗
colorFrom: pink
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# StyleSense - AI Wardrobe Assistant

StyleSense helps you organize your wardrobe and generates outfit ideas using AI.

## Features
- **Upload & Auto-Tag**: Automatically removes backgrounds and detects dominant colors.
- **Smart Wardrobe**: Organizing your clothes by category (Shirt, Pant, Shoes).
- **Outfit Generator**: Creates compatible outfit combinations based on color theory.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## Deployment

Designed for Hugging Face Spaces (Docker SDK) or Render (Python Environment).
