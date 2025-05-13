import os
import sys
from openai import OpenAI

# Read your OpenAI API key from a file
with open("./key.txt", "r") as key_file:
    client = OpenAI(api_key=key_file.read().strip())



def transcribe_audio(file_path):
    """Transcribe audio using Whisper API."""
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe", 
                file=audio_file
            )

            print(transcription.text)
            return transcription.text
    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python recordings2text.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        sys.exit(1)

    # List all files starting with '録音' and ending with '.m4a'
    files = [f for f in os.listdir(folder_path) if f.startswith("録音") and f.endswith(".m4a")]

    if not files:
        print("No matching files found.")
        sys.exit(0)

    output_file = os.path.join(folder_path, "transcriptions.txt")

    with open(output_file, "w", encoding="utf-8") as out_file:
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")
            transcription = transcribe_audio(file_path)
            out_file.write(f"--- {file_name} ---\n")
            out_file.write(transcription + "\n\n")

    print(f"Transcriptions saved to {output_file}")

if __name__ == "__main__":
    main()