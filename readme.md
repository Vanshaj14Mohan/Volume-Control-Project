# 🔊 Real-Time Hand Gesture Volume Control with MediaPipe, OpenCV & Pycaw

This project demonstrates real-time **hand gesture-based volume control** using **MediaPipe**, **OpenCV**, and **pycaw**. By measuring the distance between your thumb and index finger, you can intuitively control your system’s audio volume in real time. Ideal for anyone exploring gesture recognition, computer vision, and interactive applications.

---

## 🚀 Features

* Real-time hand detection and landmark tracking
* Dynamic volume adjustment mapped to finger distance
* Visual feedback with annotated landmarks, lines, and volume bar
* FPS display to monitor performance
* Uses MediaPipe's pre-trained hand tracking model
* System volume control via pycaw (Windows only)

---

## 🛠️ Technologies Used

* Python 🐍
* [MediaPipe](https://google.github.io/mediapipe/) by Google
* OpenCV (cv2)
* pycaw (Python Core Audio Windows Library)
* NumPy

---

## 📂 Project Structure

```plaintext
volume-control-project/
│
├── VolumeHandControl.py     # Main file to run hand gesture volume control
├── HandTrackingModule.py    # Module for hand tracking functions
├── README.md                # Project overview and details
````

---

## 🖥️ How It Works

1. Accesses webcam feed using `cv2.VideoCapture(0)`
2. Detects hand landmarks via `HandTrackingModule.py` (MediaPipe)
3. Identifies thumb tip (ID 4) and index finger tip (ID 8)
4. Calculates Euclidean distance between thumb and index finger
5. Interpolates distance to system volume range (-65 dB to 0 dB)
6. Sets the master volume using pycaw
7. Renders annotated video stream with:

   * Landmark circles
   * Connection line
   * Volume bar
   * Volume percentage
   * FPS indicator

---

## ✅ Landmark Details

* Each hand has 21 landmarks (e.g., fingertips, joints, wrist).
* Example:

  * ID `4` – Tip of the thumb
  * ID `8` – Tip of the index finger

---

## ▶️ Getting Started

### Prerequisites

* Python 3.x
* Webcam
* Windows OS (required for pycaw)

### Installation

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

---

### Run the Code

```bash
python VolumeHandControl.py
```

Make sure your webcam is connected and accessible.

---

## 🙌 Applications

* Touchless media controls
* Interactive presentations
* Smart home control interfaces
* Assistive technologies for accessibility

---

## 📌 Notes

* The hand distance range (8–200 pixels) is mapped to system volume levels (-65 dB to 0 dB).
* Adjust the range mapping in `VolumeHandControl.py` as needed.
* This project is tested on Windows due to pycaw compatibility.
* Frame rate (FPS) helps evaluate real-time performance.
* Note: pycaw works on Windows only.

---

## 💡 Future Enhancements

* Add gesture recognition for mute/unmute
* Support multi-hand interactions
* Cross-platform audio control
* Integration with a GUI dashboard or web app

---

👤 **Author**

Made with ❤️ by Vanshaj P Mohan, a Data Science Enthusiast.
Feel free to reach out for any collaborations or feedback!
