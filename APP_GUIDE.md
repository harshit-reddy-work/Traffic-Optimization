# 🚦 Traffic Control Application

## ✅ Application is Running!

The **Adaptive Traffic Signal Control System** GUI window should now be open!

## 📖 How to Use:

### Step 1: Upload Videos for 4 Lanes
1. Click **"📁 Upload Video"** for each lane
2. Select your video file (MP4, AVI, MOV)
3. Repeat for all 4 lanes (or as many as you have)

### Step 2: Process Videos
1. Click **"🚀 Process All Videos"**
2. Wait for processing to complete
3. You'll see vehicle counts appear for each lane

### Step 3: Calculate Timing
1. Click **"⚡ Calculate Timing"**
2. See the optimal traffic light durations
3. View the traffic light simulation

## 🎯 Features:

### Main Window:
- ✅ Upload videos for 4 different lanes
- ✅ Process all videos to count vehicles
- ✅ Calculate optimal traffic light timing
- ✅ Real-time progress bar
- ✅ Live vehicle count updates

### Traffic Light Simulation:
- 🟢 Shows which lane is currently green
- ⏱️ Displays time remaining for current phase
- 🔄 Automatically cycles through all lanes
- ⏹️ Stop button to end simulation

## 📊 How It Works:

1. **Vehicle Detection**: Uses YOLOv8 to detect vehicles in each video
2. **Counting**: Tracks and counts each vehicle once
3. **Calculation**: 
   - Calculates proportional timing based on vehicle density
   - Minimum: 5 seconds per lane
   - Maximum: 30 seconds per lane
   - Base cycle: 120 seconds total

4. **Formula**:
   ```
   lane_time = (lane_vehicles / total_vehicles) × 120 seconds
   (clamped between 5s and 30s)
   ```

## 🎮 Example Workflow:

1. Upload `1.mp4` to Lane 1
2. Upload `2.mp4` to Lane 2  
3. Upload `3.mp4` to Lane 3
4. Upload `4.mp4` to Lane 4
5. Click **Process All Videos**
6. Wait for "✓ All lanes processed!"
7. Click **Calculate Timing**
8. Watch the traffic light simulation!

## 📋 Example Output:

```
═══════════════════════════════════════════
TRAFFIC SIGNAL TIMING CALCULATION
═══════════════════════════════════════════

Lane 1:  98 vehicles →   30.0s
Lane 2:  75 vehicles →   24.0s
Lane 3:  45 vehicles →   16.5s
Lane 4:  32 vehicles →   11.5s

═══════════════════════════════════════════
Total vehicles: 250
Total cycle time: 82.0s
═══════════════════════════════════════════
```

## 💡 Tips:

- **Single Lane**: Can process just 1-2 lanes if needed
- **Re-upload**: Click upload again to change a video
- **Performance**: First frame may take 2-3 seconds (model loading)
- **Accuracy**: Results depend on video quality and lighting

## 🆘 Troubleshooting:

**No window opened?**
- Check if Python is running
- Look for error messages in terminal

**Processing takes too long?**
- Large videos will take longer
- Progress bar shows current status
- Can process one lane at a time

**No vehicles detected?**
- Check video quality
- Ensure vehicles are visible
- Try different video

## 🎊 Ready to Optimize Traffic Flow!

Your application is now running. Start by uploading videos and clicking "Process All Videos"!

