# input folder, yyyymmdd
# use audio_merge to merge audio into temp.wav
#     "Usage: python audio_merge.py <directory>"
# use ffmpeg to create mp3
#     ffmpeg -i temp.wav -b:a 128k -ar 44100 -ac 1 temp.mp3 -y
# use create_markdown_omni to create markdown
#     "Usage: python create_markdown_text.py <transcript_file> <date_string(yyyymmdd)>"
# clean up
#     "delete temp.wav and transcript.txt"

#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_folder> <yyyymmdd>"
    exit 1
fi

input_folder=$1
date_string=$2
TEMP_WAV="$input_folder/temp.wav"
TRANSCRIPT_FILE="$input_folder/transcript.txt"
TEMP_MP3="$input_folder/temp.mp3"

# Merge audio files into temp.wav
python audio_merge.py "$input_folder"

# Create mp3 from temp.wav
ffmpeg -i "$TEMP_WAV" -b:a 128k -ar 44100 -ac 1 "$TEMP_MP3" -y

# Create markdown from mp3
python create_markdown_omni.py "$TEMP_MP3" "$date_string"

# Clean up
rm temp.wav transcript.txt