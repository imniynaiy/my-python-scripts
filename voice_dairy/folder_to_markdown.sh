# input folder, yyyymmdd
# use audio_merge to merge audio into temp.wav
#     "Usage: python audio_merge.py <directory>"
# use transcribe to get text
#     "Usage: python transcribe_audio.py <input_file> <output_file>"
# use create_markdown to create markdown
#     "Usage: python create_markdown_text.py <transcript_file> <date_string(yyyymmdd)>"
# clean up
#     "delete temp.wav and transcript.txt"

#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <folder_path> <yyyymmdd>"
    exit 1
fi

FOLDER_PATH="$1"
DATE_STRING="$2"
TEMP_WAV="$FOLDER_PATH/temp.wav"
TRANSCRIPT_FILE="$FOLDER_PATH/transcript.txt"

source ./venv/bin/activate

# Merge audio files
python audio_merge.py "$FOLDER_PATH"

# Transcribe audio
python transcribe_audio.py "$TEMP_WAV" "$TRANSCRIPT_FILE"

# Create markdown
python create_markdown_text.py "$TRANSCRIPT_FILE" "$DATE_STRING"

# Cleanup
# rm -f "$TEMP_WAV" "$TRANSCRIPT_FILE"