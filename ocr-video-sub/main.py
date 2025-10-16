import cv2
import numpy as np
import os

# --- Configurations ---
VIDEO_PATH = 'temp/neko.mp4'  # Path to your video file

# TODO: Change to center and size for easier adjustment
SUBTITLE_REGION = (592, 909, 1624, 1080)  # (x1, y1, x2, y2) for subtitle area
FRAME_INTERVAL = 2  # seconds between frames to check
SIMILARITY_THRESHOLD = 0.5  # threshold for frame similarity (1.0 = identical)

# Save or process this subtitle frame
OUTPUT_FOLDER = 'temp/neko_sub'

def crop_subtitle_region(frame, region):
    x1, y1, x2, y2 = region
    return frame[y1:y2, x1:x2]

def frame_similarity(img1, img2):
    # Convert to grayscale for comparison
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Resize to same size if needed
    if img1_gray.shape != img2_gray.shape:
        img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))
    # Compute normalized correlation coefficient
    score = np.corrcoef(img1_gray.flatten(), img2_gray.flatten())[0, 1]
    return score

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_gap = int(FRAME_INTERVAL * fps)
    prev_sub_img = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_gap == 0:
            sub_img = crop_subtitle_region(frame, SUBTITLE_REGION)
            if prev_sub_img is not None:
                sim = frame_similarity(sub_img, prev_sub_img)
                if sim < SIMILARITY_THRESHOLD:
                    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
                    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f'subtitle_{frame_idx}.png'), sub_img)
            prev_sub_img = sub_img

        frame_idx += 1

    cap.release()

if __name__ == '__main__':
    main()