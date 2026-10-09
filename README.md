# 🦾 High-Performance AI Virtual Canvas

An interactive, glitch-free computer vision application that allows you to draw on your screen in real time using hand gestures via your webcam. Featuring a custom **Black Ink Engine**, it creates high-fidelity digital drawings directly on your video stream with fluid line tracking.

---

## ✨ Key Features

* **Glitch-Free Black Ink Engine:** Leverages advanced image masking (`cv2.bitwise_and` and inverse thresholds) to apply pure, solid black ink to the frame without overlapping issues or transparency glitches.
* **Intuitive Gesture Controls:**
  * ☝️ **Draw Mode (Index Up):** Draws thick, smooth anti-aliased lines.
  * ✌️ **Hover Mode (Index + Middle Up):** Safely breaks the drawing path, acting as a non-marking cursor.
* **Auto-Reset Pipeline:** Instantly severs the drawing path when your hand leaves the frame to prevent random, accidental lines.
* **High-Definition Resolution:** Configured specifically for a sharp `1280x720` HD canvas capture.

---

## 🛠️ Prerequisites & Installation

Make sure you have Python installed, then run the following command to install the required libraries:

```bash
pip install opencv-python numpy cvzone mediapipe
```

---

## 🚀 How to Run

1. Connect your webcam.
2. Execute the script:
   ```bash
   python main.py
   ```
3. Keep your hand inside the camera frame and start creating!

---

## 🕹️ Controls & Gestures

| Gesture / Key | Action | Visual Feedback |
| :---: | :--- | :--- |
| **☝️ Index Finger UP** | **Draw Mode:** Draws continuous black ink lines onto the screen. | Red target cursor 🔴 |
| **✌️ Index + Middle UP** | **Hover Mode:** Moves the cursor without drawing (breaks the stroke line). | Blue hover cursor 🔵 |
| **`c` Key** | **Clear Canvas:** Wipes out all drawings to give you a clean slate. | Re-initializes layer |
| **`q` Key** | **Quit:** Safely closes the camera stream and shuts down the window. | Closes clean |

---

## 🧠 Technical Workflow

1. **Frame Capture & Mirroring:** The live webcam feed is grabbed via `OpenCV` and flipped horizontally (`cv2.flip`) to provide a natural, mirror-like drawing experience.
2. **Hand Tracking & Landmark Isolation:** `cvzone` maps **21 distinct landmarks** on the hand. The tip of the index finger (Landmark `8`) serves as the core drawing coordinate.
3. **Advanced Image Masking:** The strokes are rendered in white on an independent background canvas. During the blending phase, the frame converts this mask into a sharp binary inverse layer, punching holes through the original webcam footage to inject pixel-perfect black ink line paths seamlessly.
