from pathlib import Path
import os
import sys
from pydub import AudioSegment

def merge_audio_files(directory, output_file="temp.wav", spacing=1000):
    """Merge all audio files in directory into one wav file with silence between them"""
    # Find all mp3 and m4a files
    audio_files = []
    for ext in ['.mp3', '.m4a', '.MP3', '.M4A']:
        audio_files.extend(list(Path(directory).glob(f'*{ext}')))

    if not audio_files:
        print("No audio files found")
        return False

    # Create silence
    silence = AudioSegment.silent(duration=spacing)
    merged_audio = AudioSegment.empty()


    # Get duration of each file
    audios = []
    for audio_file in audio_files:
        audios.append(AudioSegment.from_file(audio_file))

    for audio in audios:
        merged_audio += audio + silence

    output_file = os.path.join(directory, output_file)
    merged_audio.export(output_file, format="wav", parameters=['-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000'])

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