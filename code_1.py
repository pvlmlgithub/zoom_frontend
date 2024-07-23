import os
import re
from datetime import datetime
import cv2

def get_latest_recording_folder(base_path):     
    folders = os.listdir(base_path)
    timestamp_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}')
    
    latest_time = None
    latest_folder = None
    
    for folder in folders:
        match = timestamp_pattern.search(folder)
        if match:
            folder_time = datetime.strptime(match.group(), '%Y-%m-%d %H.%M.%S')
            if not latest_time or folder_time > latest_time:
                latest_time = folder_time
                latest_folder = folder
    
    return os.path.join(base_path, latest_folder) if latest_folder else None

def extract_frames_from_video(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
    
    cap.release()

def main():
    username = "Akshay"  # Replace with the actual username
    base_path = f"C:\\Users\\{username}\\Documents\\Zoom"
    output_folder = f"zoom_code\\out"
    
    latest_folder = get_latest_recording_folder(base_path)
    if not latest_folder:
        print("No recording folders found.")
        return
    
    video_file = None
    for file in os.listdir(latest_folder):
        if file.startswith("video"):
            video_file = os.path.join(latest_folder, file)
            break
    
    if not video_file:
        print("No video file found in the latest recording folder.")
        return

    # Create a new subfolder with the current timestamp inside the provided output folder
    current_time = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    new_output_folder = os.path.join(output_folder, current_time)
    
    extract_frames_from_video(video_file, new_output_folder)
    print(f"Frames extracted and saved to {new_output_folder}")

if __name__ == "__main__":
    main()
