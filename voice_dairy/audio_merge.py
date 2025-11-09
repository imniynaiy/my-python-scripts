from pathlib import Path
import subprocess
import os
import sys

def merge_audio_files(directory, output_file="temp.wav", spacing=1000):
    """Merge all audio files in directory into one wav file with silence between them"""
    # Find all mp3 and m4a files
    audio_files = []
    for ext in ['.mp3', '.m4a', '.MP3', '.M4A']:
        audio_files.extend(list(Path(directory).glob(f'*{ext}')))

    if not audio_files:
        print("No audio files found")
        return False

    # Get duration of each file
    durations = []
    for audio_file in audio_files:
        cmd = ['ffprobe', '-i', str(audio_file), '-show_entries', 
               'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
        duration = float(subprocess.check_output(cmd).decode().strip())
        durations.append(duration)

    ds = []
    total_duration = 0
    for duration in durations:
        total_duration += spacing / 1000 + duration
        ds.append(total_duration)

    # Construct the filter complex
    filter_parts = []
    inputs = []
    
    # Add input files to command
    cmd = ['ffmpeg']
    for audio_file in audio_files:
        cmd.extend(['-i', str(audio_file)])

    # Create silence sources and concatenations
    for i in range(len(audio_files) - 1):
        filter_parts.append(f"aevalsrc=0:d={ds[i]}[s{i}]")
        
    # Build the mixing command
    mix_inputs = []
    for i in range(len(audio_files)):
        mix_inputs.append(f"{i}:a")
        if i < len(audio_files) - 1:
            mix_inputs.append(f"[s{i}]")
    
    filter_complex = '\"' + ';'.join(filter_parts) + f";amix=inputs={len(mix_inputs)-1}[aout]\""
    
    output_file = os.path.join(directory, output_file)
    cmd.extend(['-filter_complex', filter_complex, '-map', '\"[aout]\"','-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', output_file])
    print(" ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python audio_merge.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    if not merge_audio_files(directory):
       sys.exit(1)

if __name__ == "__main__":
    main()