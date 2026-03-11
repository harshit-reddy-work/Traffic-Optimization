# Adaptive Traffic Signal Control System

![Stars](https://img.shields.io/github/stars/harshit-reddy-work/Traffic-Optimization.svg?style=social)
![Forks](https://img.shields.io/github/forks/harshit-reddy-work/Traffic-Optimization.svg?style=social)
![Language](https://img.shields.io/github/languages/top/harshit-reddy-work/Traffic-Optimization.svg)
![Issues](https://img.shields.io/github/issues/harshit-reddy-work/Traffic-Optimization)
![PRsWelcome](https://img.shields.io/badge/PRs-welcome-informational)

## Overview

An intelligent traffic signal control system that uses real-time vehicle detection to dynamically adjust signal timings. Instead of relying on fixed-cycle traffic lights, the system analyzes live traffic conditions using deep learning (YOLOv8) and optimizes green/red durations per lane based on actual vehicle density — reducing wait times and improving traffic flow.

## Key Features

- **Real-time vehicle detection** using YOLOv8 object detection
- **Adaptive signal timing** — green light duration adjusts based on traffic density per lane
- **Multi-lane support** — processes multiple lanes simultaneously with multithreading
- **Queue density analysis** — calculates vehicle counts and relative congestion per lane
- **Interactive GUI** — visual interface showing detections and signal states via Tkinter

## How It Works

1. **Capture** — Camera feeds capture real-time images of each lane at the intersection
2. **Detect** — YOLOv8 processes each frame to detect and count vehicles per lane
3. **Analyze** — The system computes relative traffic density across all lanes
4. **Optimize** — Signal timing is allocated proportionally — denser lanes get longer green phases
5. **Control** — Optimized timings are applied to the traffic signals in real-time

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Object Detection | YOLOv8 (Ultralytics) |
| Deep Learning Framework | PyTorch |
| Tracking | dlib correlation tracker |
| GUI | Tkinter |
| Language | Python 3.7+ |

## Installation

```bash
# Clone the repository
git clone https://github.com/harshit-reddy-work/Traffic-Optimization.git
cd Traffic-Optimization

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Traffic Control App
```bash
python traffic_control_app.py
```

### Running with Multithreading (YOLOv8)
```bash
python multithreading_yolo8.py
```

### Core Detection Script
```bash
python program.py
```

## Signal Timing Algorithm

The system uses a proportional allocation algorithm to distribute signal time:

```python
baseTimer = 120  # Total cycle time in seconds
timeLimits = [5, 30]  # Min and max green time per lane

# Each lane gets time proportional to its vehicle count
time_per_lane = (vehicles_in_lane / total_vehicles) * baseTimer
# Clamped within [5, 30] seconds
```

Lanes with more vehicles get longer green phases, while low-traffic lanes get shorter ones — all within configurable min/max bounds.

## Project Structure

```
├── program.py                 # Core vehicle detection logic
├── multithreading.py          # Multi-lane processing with threading
├── multithreading_yolo8.py    # YOLOv8 based multi-lane processing
├── traffic_control_app.py     # Interactive GUI application
├── run_interactive.py         # Interactive runner script
├── requirements.txt           # Python dependencies
├── yolov8n.pt                 # YOLOv8 nano model weights
└── images/                    # Project assets
```

## Future Scope

- Integration with real traffic camera feeds
- Emergency vehicle priority detection
- Pedestrian crossing detection and timing
- Cloud dashboard for traffic analytics
- Edge deployment on embedded devices (Raspberry Pi / Jetson Nano)

## Developer

**Harshit Reddy** — [GitHub](https://github.com/harshit-reddy-work)
