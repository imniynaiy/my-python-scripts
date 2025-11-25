import os
import glob
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Batch extract slides from mp4 files")
parser.add_argument("input_folder", help="Path to folder containing .mp4 files")
parser.add_argument("--output-base", default="temp/slides", help="Base output directory (default: temp/slides)")
args = parser.parse_args()

input_folder = os.path.abspath(os.path.expanduser(args.input_folder))
output_base = os.path.abspath(os.path.expanduser(args.output_base))

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