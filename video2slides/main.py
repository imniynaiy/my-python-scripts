import cv2
import os
import numpy as np
import argparse

def frame_difference(f1, f2):
    # Compute normalized difference between two frames
    diff = cv2.absdiff(f1, f2)
    non_zero_count = np.count_nonzero(diff)
    total_pixels = diff.size
    return non_zero_count / total_pixels

def get_default_output_dir(video_path):
    base = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(os.getcwd(), f"{base}_slides")

def main():
    parser = argparse.ArgumentParser(description="Extract slides from a lecture video.")
    parser.add_argument("video_path", help="Path to your lecture video")
    parser.add_argument("--output_dir", help="Directory to save extracted slides (default: <video>_slides under current folder)")
    parser.add_argument("--interval_sec", type=float, default=2, help="Check every X seconds (default: 2)")
    parser.add_argument("--diff_threshold", type=float, default=0.2, help="Y%% difference threshold (default: 0.2)")

    args = parser.parse_args()

    video_path = args.video_path
    output_dir = args.output_dir or get_default_output_dir(video_path)
    interval_sec = args.interval_sec
    diff_threshold = args.diff_threshold

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * interval_sec)
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
                cv2.imwrite(f"{output_dir}/{slide_idx:03d}.png", frame)
                last_frame = gray
                slide_idx += 1
            else:
                diff = frame_difference(last_frame, gray)
                if diff > diff_threshold:
                    cv2.imwrite(f"{output_dir}/{slide_idx:03d}.png", frame)
                    last_frame = gray
                    slide_idx += 1

        frame_count += 1

    cap.release()
    print(f"Extraction complete. {slide_idx-1} slides saved to '{output_dir}'.")

if __name__ == "__main__":
    main()