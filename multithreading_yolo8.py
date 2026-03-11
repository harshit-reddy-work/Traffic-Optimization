from tracking.centroidtracker import CentroidTracker
from tracking.trackableobject import TrackableObject
from ultralytics import YOLO
import cv2
import numpy as np
import time
import os

def countVehicles(video_file_path):
	"""
	Count vehicles in a video file.
	
	Args:
		video_file_path: Absolute or relative path to video file
		
	Returns:
		int: Total count of vehicles detected
	"""
	
	# Initialize YOLOv8 model
	model = YOLO('yolov8n.pt')  # Loads pretrained model
	
	# Classes of interest (vehicle classes in COCO)
	# bicycle: 1, car: 2, motorcycle: 3, bus: 5, truck: 7
	vehicle_classes = [1, 2, 3, 5, 7]
	class_names = {1: 'bicycle', 2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
	
	# Initialize Centroid Tracker
	ct = CentroidTracker(maxDisappeared=5, maxDistance=50)
	trackableObjects = {}
	
	skip_frames = 10
	confidence_level = 0.40
	total = 0
	
	# Handle both absolute paths (from file upload) and relative paths
	if not os.path.isabs(video_file_path):
		# If relative path, make it absolute
		video_path = os.path.abspath(video_file_path)
	else:
		video_path = video_file_path
	
	video_name = os.path.basename(video_path)
	
	if not os.path.exists(video_path):
		print(f"File does not exist: {video_path}")
		return 0
	
	print(f"Processing video: {video_path}")
	
	cap = cv2.VideoCapture(video_path)
	
	# Get video properties
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(cap.get(cv2.CAP_PROP_FPS))
	
	print(f"Processing {video_name} ({width}x{height} @ {fps} FPS)")
	
	skipped_frames_counter = 0
	frame_count = 0
	
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break
		
		frame_count += 1
		
		# Perform detection every skip_frames
		if skipped_frames_counter == skip_frames:
			# YOLOv8 detection
			results = model(frame, conf=confidence_level, verbose=False)
			
			tracker_rects = []
			
			# Process detections
			for result in results:
				boxes = result.boxes
				for box in boxes:
					cls = int(box.cls[0])
					
					# Check if it's a vehicle class
					if cls in vehicle_classes:
						class_name = class_names.get(cls, 'vehicle')
						conf = float(box.conf[0])
						
						# Get bounding box coordinates
						x1, y1, x2, y2 = box.xyxy[0]
						startX, startY, endX, endY = int(x1), int(y1), int(x2), int(y2)
						
						# Draw rectangle and label
						cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
						label = f"{class_name} {conf:.2f}"
						cv2.putText(frame, label, (startX, startY - 10), 
									cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
						
						# Add to tracking rectangles
						tracker_rects.append((startX, startY, endX, endY))
			
			# Reset skip counter
			skipped_frames_counter = 0
		
		else:
			# For skipped frames, use last detections or skip
			skipped_frames_counter += 1
			tracker_rects = []
		
		# Update centroid tracker
		objects = ct.update(tracker_rects)
		
		# Loop over tracked objects
		for (objectID, centroid) in objects.items():
			to = trackableObjects.get(objectID, None)
			
			if to is None:
				to = TrackableObject(objectID, centroid)
			else:
				to.centroids.append(centroid)
				
				if not to.counted:
					total += 1
					to.counted = True
			
			trackableObjects[objectID] = to
			
			# Draw ID and centroid
			cv2.putText(frame, f"ID {objectID}", (centroid[0] - 10, centroid[1] - 10),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
		
		# Display total count
		cv2.putText(frame, f"Total: {total}", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
		cv2.putText(frame, f"Frame: {frame_count}", (10, 70),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
		
		# Display frame
		cv2.imshow(video_name, frame)
		
		# Handle keyboard input
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		elif key == ord('p'):
			cv2.waitKey(0)
		
		# Print progress every 100 frames
		if frame_count % 100 == 0:
			print(f"Processed {frame_count} frames, Total vehicles: {total}")
	
	cap.release()
	cv2.destroyAllWindows()
	
	print(f"\nVideo processing complete!")
	print(f"Total vehicles detected: {total}")
	print(f"Total frames processed: {frame_count}")
	
	return total

if __name__ == "__main__":
	total = countVehicles("videos/test.mp4")
	print(f"\nFinal count: {total}")

