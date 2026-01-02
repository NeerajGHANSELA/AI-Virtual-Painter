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

## Installation

### Prerequisites

- Python 3.7 or higher
- Webcam

### Setup

1. Clone the repository:

```bash
git clone https://github.com/NeerajGHANSELA/AI-Virtual-Painter.git
cd AI-Virtual-Painter
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python virtualPainter.py
```

## Usage

Once the application starts, your webcam will activate and you'll see a color palette menu at the top of the screen.

### Gesture Controls

| Gesture                                     | Mode           | Action                                    |
| ------------------------------------------- | -------------- | ----------------------------------------- |
| ☝️ **Index finger up** (middle finger down) | Drawing Mode   | Draw with selected color/eraser           |
| ✌️ **Index + Middle fingers up**            | Selection Mode | Hover over menu to select color or eraser |

### Available Colors & Tools

- **White** - Default color
- **Blue** - Bright blue for contrast
- **Red** - Bold red strokes
- **Green** - Vibrant green
- **Eraser** - Remove drawn content

### Tips for Best Experience

- Ensure good lighting for optimal hand detection
- The video feed is mirror-flipped for natural drawing (move right, draw right)
- Draw below the menu bar (top 125 pixels reserved for palette)
- Use two fingers to select colors, then switch to one finger to draw
- The selected color/tool is indicated by a line above it in the menu
