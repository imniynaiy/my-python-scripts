import cv2
import os
import numpy as np

VIDEO_PATH = 'temp/【耶鲁大学】【自动字幕】情绪管理/[P01]1-1. 马克·布雷克特博士的课程引入.mp4'  # Path to your lecture video
OUTPUT_DIR = '../temp/slides/p1'       # Directory to save extracted slides
INTERVAL_SEC = 2            # Check every X seconds
DIFF_THRESHOLD = 0.2        # Y% difference (e.g., 0.2 = 20%)

def frame_difference(f1, f2):
    # Compute normalized difference between two frames
    diff = cv2.absdiff(f1, f2)
    non_zero_count = np.count_nonzero(diff)
    total_pixels = diff.size
    return non_zero_count / total_pixels

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * INTERVAL_SEC)
    frame_count = 0
    slide_idx = 1
    last_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval_frames == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if last_frame is None:
                cv2.imwrite(f"{OUTPUT_DIR}/{slide_idx:03d}.png", frame)
                last_frame = gray
                slide_idx += 1
            else:
                diff = frame_difference(last_frame, gray)
                if diff > DIFF_THRESHOLD:
                    cv2.imwrite(f"{OUTPUT_DIR}/{slide_idx:03d}.png", frame)
                    last_frame = gray
                    slide_idx += 1

        frame_count += 1

    cap.release()
    print(f"Extraction complete. {slide_idx-1} slides saved to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    main()