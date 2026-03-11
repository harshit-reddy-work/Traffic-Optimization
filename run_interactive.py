"""
Interactive version that keeps the window open and shows more info
"""
from multithreading_yolo8 import countVehicles
import cv2

def run_interactive():
	print("Starting interactive vehicle detection...")
	print("Press Q to quit, P to pause")
	print("=" * 60)
	
	total = countVehicles("/videos/1.mp4")
	
	print("=" * 60)
	print(f"✅ Final vehicle count: {total}")
	print("=" * 60)
	
	return total

if __name__ == "__main__":
	run_interactive()

