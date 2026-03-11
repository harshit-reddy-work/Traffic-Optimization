# How to Install dlib on Windows

## The Problem
After installing CMake, it needs to be added to your system PATH, and you need to restart your terminal for the changes to take effect.

## Quick Steps:

1. **Verify CMake Installation:**
   - Open a NEW PowerShell window (close and reopen)
   - Run: `cmake --version`
   - If you see the version, CMake is ready!

2. **Install dlib:**
   ```powershell
   cd D:\ass\Adaptive-Traffic-Signal-Control-System
   .\venv\Scripts\Activate.ps1
   pip install dlib
   ```

3. **Install tensornets:**
   ```powershell
   pip install tensornets
   ```

## Alternative: Manual PATH Addition

If CMake isn't found even after restarting:

1. Find CMake installation folder (usually: `C:\Program Files\CMake\bin`)
2. Add it to System PATH:
   - Search for "Environment Variables" in Windows
   - Edit "Path" under System variables
   - Add: `C:\Program Files\CMake\bin`
   - Click OK
   - Restart terminal

## Or Use a Pre-built Binary

If you have Visual Studio Build Tools installed, try:
```powershell
pip install https://github.com/mars-project/dlib/releases/download/v19.22/dlib-19.22.99-cp312-cp312-win_amd64.whl
```

## Check Visual C++ Build Tools

dlib and tensornets require Microsoft Visual C++ Build Tools. Install from:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Select "Desktop development with C++" workload.

