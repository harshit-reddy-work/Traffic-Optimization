import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
import os
from multithreading_yolo8 import countVehicles

class TrafficControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Traffic Signal Control System")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Video paths for 4 lanes
        self.video_paths = [None, None, None, None]
        self.vehicle_counts = [0, 0, 0, 0]
        self.timings = [0, 0, 0, 0]
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🚦 Adaptive Traffic Control System", 
                        font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        # Instructions
        info = tk.Label(self.root, text="Upload videos from 4 lanes to calculate optimal light timing",
                       font=('Arial', 11), bg='#2c3e50', fg='#95a5a6')
        info.pack(pady=5)
        
        # Video upload frame
        upload_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        upload_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Lane labels and buttons
        self.lane_widgets = []
        for i in range(4):
            lane_frame = tk.Frame(upload_frame, bg='#34495e')
            lane_frame.pack(pady=10, padx=20, fill=tk.X)
            
            lane_label = tk.Label(lane_frame, text=f"Lane {i+1}:", 
                                 font=('Arial', 12, 'bold'), bg='#34495e', fg='white', width=8)
            lane_label.pack(side=tk.LEFT)
            
            video_label = tk.Label(lane_frame, text="No video selected", 
                                  font=('Arial', 10), bg='#34495e', fg='#ecf0f1', width=40)
            video_label.pack(side=tk.LEFT, padx=10)
            
            upload_btn = tk.Button(lane_frame, text="📁 Upload Video", 
                                  command=lambda idx=i: self.upload_video(idx),
                                  bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
                                  relief=tk.FLAT, padx=10, pady=5, cursor='hand2')
            upload_btn.pack(side=tk.LEFT)
            
            count_label = tk.Label(lane_frame, text="Vehicles: 0", 
                                   font=('Arial', 10, 'bold'), bg='#34495e', fg='#27ae60', width=12)
            count_label.pack(side=tk.LEFT, padx=10)
            
            self.lane_widgets.append({
                'label': video_label,
                'count': count_label
            })
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=20)
        
        self.process_btn = tk.Button(control_frame, text="🚀 Process All Videos", 
                                     command=self.process_videos,
                                     bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                                     relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        self.process_btn.pack(side=tk.LEFT, padx=10)
        
        self.calculate_btn = tk.Button(control_frame, text="⚡ Calculate Timing", 
                                       command=self.calculate_timing,
                                       bg='#e67e22', fg='white', font=('Arial', 14, 'bold'),
                                       relief=tk.FLAT, padx=20, pady=10, cursor='hand2', 
                                       state=tk.DISABLED)
        self.calculate_btn.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='determinate', length=400)
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="Ready to process videos",
                                     font=('Arial', 10), bg='#2c3e50', fg='white')
        self.status_label.pack(pady=5)
        
        # Results frame
        results_frame = tk.LabelFrame(self.root, text="⚡ Traffic Light Timing", 
                                     font=('Arial', 12, 'bold'), bg='#34495e', fg='white',
                                     labelanchor='n')
        results_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Results display
        self.results_text = tk.Text(results_frame, height=8, font=('Consolas', 10),
                                   bg='#2c3e50', fg='#27ae60', relief=tk.FLAT)
        self.results_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
    def upload_video(self, lane_idx):
        file_path = filedialog.askopenfilename(
            title=f"Select video for Lane {lane_idx + 1}",
            filetypes=[("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")]
        )
        
        if file_path:
            self.video_paths[lane_idx] = file_path
            filename = os.path.basename(file_path)
            self.lane_widgets[lane_idx]['label'].config(text=filename[:50])
            self.lane_widgets[lane_idx]['count'].config(text="Vehicles: ?", fg='#f39c12')
    
    def process_videos(self):
        if not any(self.video_paths):
            messagebox.showwarning("No Videos", "Please upload at least one video!")
            return
        
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.calculate_btn.config(state=tk.DISABLED)
        
        # Run in separate thread to avoid freezing UI
        thread = Thread(target=self._process_videos_thread)
        thread.daemon = True
        thread.start()
    
    def _process_videos_thread(self):
        total_lanes = sum(1 for p in self.video_paths if p)
        
        for i, video_path in enumerate(self.video_paths):
            if not video_path:
                continue
            
            self.root.after(0, lambda idx=i: self._update_status(f"Processing Lane {idx+1}..."))
            self.root.after(0, lambda idx=i: self.progress.config(value=(idx)*100//total_lanes))
            
            try:
                count = countVehicles(video_path)
                self.vehicle_counts[i] = count
                
                self.root.after(0, lambda idx=i, cnt=count: self._update_lane_count(idx, cnt))
                self.root.after(0, lambda: self._update_status(f"✓ Lane {i+1}: {count} vehicles"))
            except Exception as e:
                self.root.after(0, lambda: self._update_status(f"✗ Error: {str(e)}"))
                self.vehicle_counts[i] = 0
        
        self.root.after(0, lambda: self.progress.config(value=100))
        self.root.after(0, lambda: self._update_status("✓ All lanes processed!"))
        self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.calculate_btn.config(state=tk.NORMAL))
        self.root.after(0, lambda: setattr(self, 'processing', False))
    
    def _update_status(self, message):
        self.status_label.config(text=message)
    
    def _update_lane_count(self, idx, count):
        self.lane_widgets[idx]['count'].config(text=f"Vehicles: {count}", fg='#27ae60')
    
    def calculate_timing(self):
        baseTimer = 120
        timeLimits = [5, 30]
        
        # Calculate timing for each lane
        total_vehicles = sum(self.vehicle_counts)
        
        if total_vehicles == 0:
            messagebox.showwarning("No Vehicles", "No vehicles detected in any lane!")
            return
        
        results = []
        self.timings = []
        
        for i, count in enumerate(self.vehicle_counts):
            if count > 0:
                proportion = count / total_vehicles
                time = proportion * baseTimer
                
                # Clamp to limits
                if time < timeLimits[0]:
                    time = timeLimits[0]
                elif time > timeLimits[1]:
                    time = timeLimits[1]
                
                self.timings.append(time)
            else:
                self.timings.append(timeLimits[0])  # Minimum time for no vehicles
            
            results.append(f"Lane {i+1}: {count:3d} vehicles → {self.timings[i]:5.1f}s")
        
        # Display results
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', 
            f"═══════════════════════════════════════════\n"
            f"TRAFFIC SIGNAL TIMING CALCULATION\n"
            f"═══════════════════════════════════════════\n\n"
            + '\n'.join(results) +
            f"\n\n═══════════════════════════════════════════\n"
            f"Total vehicles: {total_vehicles}\n"
            f"Total cycle time: {sum(self.timings):.1f}s\n"
            f"═══════════════════════════════════════════\n"
        )
        
        self._simulate_traffic_lights()
    
    def _simulate_traffic_lights(self):
        # Create a new window for traffic light simulation
        light_window = tk.Toplevel(self.root)
        light_window.title("🔄 Traffic Light Simulation")
        light_window.geometry("600x400")
        light_window.configure(bg='#2c3e50')
        
        # Title
        title = tk.Label(light_window, text="🔄 Live Traffic Light Status", 
                        font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        # Current lane label
        self.current_lane_label = tk.Label(light_window, text="", 
                                          font=('Arial', 14), bg='#2c3e50', fg='white')
        self.current_lane_label.pack()
        
        # Status label
        self.light_status_label = tk.Label(light_window, text="", 
                                          font=('Arial', 24, 'bold'), bg='#2c3e50', fg='red')
        self.light_status_label.pack(pady=20)
        
        # Time remaining
        self.time_label = tk.Label(light_window, text="", 
                                   font=('Arial', 16), bg='#2c3e50', fg='#95a5a6')
        self.time_label.pack(pady=10)
        
        # Stop simulation button
        self.simulating = True
        stop_btn = tk.Button(light_window, text="⏹️ Stop Simulation", 
                            command=lambda: setattr(self, 'simulating', False),
                            bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                            relief=tk.FLAT, padx=20, pady=10)
        stop_btn.pack(pady=20)
        
        # Start simulation
        Thread(target=self._animate_lights, args=(light_window,), daemon=True).start()
    
    def _animate_lights(self, window):
        lane = 0
        
        while self.simulating and window.winfo_exists():
            # Show green for current lane
            for i in range(4):
                if i == lane:
                    window.after(0, lambda idx=i: self._show_green(window, idx))
            
            # Wait for this lane's timing
            remaining = self.timings[lane]
            while remaining > 0 and self.simulating and window.winfo_exists():
                import time
                time.sleep(0.5)
                remaining -= 0.5
                window.after(0, lambda r=remaining: self._update_time_display(window, r))
            
            # Move to next lane
            lane = (lane + 1) % 4
            
            # Brief yellow phase
            if self.simulating and window.winfo_exists():
                window.after(0, lambda: self._show_yellow(window))
                import time
                time.sleep(1)
    
    def _show_green(self, window, lane_idx):
        self.current_lane_label.config(text=f"🟢 Lane {lane_idx + 1} - GREEN")
        self.light_status_label.config(text="🟢 GO", fg='#27ae60')
        self._update_time_display(window, self.timings[lane_idx])
    
    def _show_yellow(self, window):
        self.light_status_label.config(text="🟡 YELLOW", fg='#f39c12')
    
    def _update_time_display(self, window, remaining):
        self.time_label.config(text=f"Time remaining: {remaining:.1f}s")

def main():
    root = tk.Tk()
    app = TrafficControlApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

