import os
import subprocess
import sys


def transcribe_audio(input_file="temp.wav", output_file="temp"):
    """Transcribe audio using whisper"""
    cmd = [
        os.path.expanduser('~/Desktop/whisper.cpp/build/bin/whisper-cli'),
        '-m', os.path.expanduser('~/Desktop/whisper.cpp/models/ggml-large-v3-turbo.bin'),
        '-f', input_file,
        '-l', 'zh',
        '-otxt',
        '-of', output_file,
        # '-nt', 'true'
    ]
    subprocess.run(cmd, check=True)

def attach_transcript_to_file(transcript_file, markdown_file):
    """Attach transcript to the end of the markdown file"""
    with open(transcript_file, 'r', encoding='utf-8') as tf:
        transcript = tf.read()

    with open(markdown_file, 'a', encoding='utf-8') as mf:
        mf.write(f"\n\n## Transcript\n```\n{transcript}\n```")

def main():
    if len(sys.argv) != 3:
        print("Usage: python transcribe_audio.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not transcribe_audio(input_file, output_file):
       sys.exit(1)

if __name__ == "__main__":
    main()