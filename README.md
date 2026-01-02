# AI-Virtual-Painter
Real-time air painting tool powered by computer vision and hand gesture recognition with multi-color palette and eraser

## Overview

VirtualPainter uses MediaPipe's hand tracking and OpenCV to detect hand gestures in real-time, allowing you to create digital artwork by simply moving your finger through the air. Switch between colors, use an eraser, and watch your drawings appear live on screen—no physical stylus or touchscreen required.

**Key Features:**
- 🎨 Multi-color palette with 4 vibrant colors (White, Blue, Red, Green)
- ✏️ Eraser tool for corrections
- ✋ Intuitive dual-mode gestures:
  - Index finger up = Draw mode
  - Index + Middle fingers = Selection mode
- 🎥 Real-time canvas overlay on webcam feed
- 🪞 Mirror-flipped display for natural drawing experience
- ⚡ Smooth, artifact-free mode transitions

**Technologies:** Python • MediaPipe • OpenCV • NumPy • Computer Vision

## How It Works

**Drawing Mode:** Raise your index finger (middle finger down) and move it to draw
**Selection Mode:** Raise both index and middle fingers, then hover over the menu to select colors or eraser

The application uses advanced image processing techniques including bitwise operations and binary thresholding to seamlessly blend your virtual drawings with the live video feed, creating an augmented reality art experience.
