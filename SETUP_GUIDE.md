# Setup Guide for Adaptive Traffic Signal Control System

## ✅ Installed Dependencies

The following packages have been successfully installed in your virtual environment:
- TensorFlow 2.20.0
- OpenCV (opencv-python)
- NumPy
- SciPy
- h5py
- imutils

## ⚠️ Additional Requirements Needed

### For Windows Users:

You need to install two compilation tools to build the remaining dependencies:

#### 1. CMake (Required for dlib)
Download and install from: https://cmake.org/download/
- Select "Add CMake to system PATH" during installation
- After installation, restart your terminal

#### 2. Microsoft Visual C++ Build Tools (Required for tensornets)
Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Select "C++ build tools" workload
- This will install the necessary compilers

### Alternative: Use Pre-built Wheels

After installing the above tools, run:
```bash
.\venv\Scripts\Activate.ps1
pip install dlib tensornets
```

## 🚀 How to Run

### Activate Virtual Environment:
```powershell
.\venv\Scripts\Activate.ps1
```

### Run the Project:
```powershell
# For Linux/Mac (use Git Bash on Windows):
bash run.sh

# Or manually:
python multithreading.py "/videos/1.mp4" >> out.txt
python multithreading.py "/videos/2.mp4" >> out.txt
python multithreading.py "/videos/3.mp4" >> out.txt
python multithreading.py "/videos/4.mp4" >> out.txt
python program.py
```

### Individual Video Analysis:
```powershell
python multithreading.py "/videos/test.mp4"
```

## 📝 Notes

- The project uses TensorFlow 1.x API (compat.v1) for YOLOv3
- Videos should be placed in the `/videos/` directory
- Vehicle counts are written to `out.txt`
- The timing calculation script reads from `out.txt` and calculates optimal signal durations

## 🔧 Troubleshooting

If you encounter issues:
1. Ensure all videos exist in the videos folder
2. Check that out.txt has 4 lines (one vehicle count per lane)
3. TensorFlow models will download automatically on first run
4. For best performance, use GPU-enabled TensorFlow (CUDA setup required)

