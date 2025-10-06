import os
import glob
import subprocess

input_folder = "temp/【耶鲁大学】【自动字幕】情绪管理"
output_base = "temp/slides"

os.makedirs(output_base, exist_ok=True)

mp4_files = sorted(glob.glob(os.path.join(input_folder, "*.mp4")))
for idx, mp4_file in enumerate(mp4_files, 1):
    output_dir = os.path.join(output_base, str(idx))
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "python3",
        "video2slides/main.py",
        mp4_file,
        "--output_dir",
        output_dir
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd)