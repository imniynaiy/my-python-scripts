#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_folder>"
    exit 1
fi

# Directory containing audio files
SRT_DIR=$1

# Loop through all mp3 and wav files in the directory
for srt_file in "$SRT_DIR"/*.{srt,SRT}; do
    # Check if the file exists
    if [[ -f "$srt_file" ]]; then
        # Run the transcription script
        python ~/Desktop/scripts/srt2txt/srt2txt.py "$srt_file"
    fi
done