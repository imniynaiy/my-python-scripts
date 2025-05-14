import re
import os
import sys

def generate_cue(input_file, album_title="", artist_name="", genre="", year="", audio_filename="audiofile.mp3"):
    # Regex pattern to extract time and title
    pattern = r"(\d{2}:\d{2}:\d{2})\s+(.*)"  # Matches "mm:ss:ms Title"
    
    # Derive the output file path
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(os.path.dirname(input_file), f"{base_name}.cue")
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            # Write the header for the .cue file
            outfile.write(f"FILE \"{audio_filename}\" MP3\n")
            
            # Write optional tags if provided
            if album_title:
                outfile.write(f"TITLE \"{album_title}\"\n")
            if artist_name:
                outfile.write(f"PERFORMER \"{artist_name}\"\n")
            if genre:
                outfile.write(f"REM GENRE \"{genre}\"\n")
            if year:
                outfile.write(f"REM DATE \"{year}\"\n")
            
            track_number = 1
            for line in infile:
                match = re.match(pattern, line.strip())
                if match:
                    time = match.group(1) # Group is splitted by "()"
                    title = match.group(2)
                    
                    # Write track information to the .cue file
                    outfile.write(f"  TRACK {track_number:02d} AUDIO\n")
                    outfile.write(f"    TITLE \"{title}\"\n")
                    outfile.write(f"    INDEX 01 {time}\n")
                    
                    track_number += 1
        print(f"Cue file generated successfully: {output_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_cue.py <input_txt_file> [album_title] [artist_name] [genre] [year] [audio_filename]")
    else:
        input_txt = sys.argv[1]
        album_title = sys.argv[2] if len(sys.argv) > 2 else ""
        artist_name = sys.argv[3] if len(sys.argv) > 3 else ""
        genre = sys.argv[4] if len(sys.argv) > 4 else ""
        year = sys.argv[5] if len(sys.argv) > 5 else ""
        audio_filename = sys.argv[6] if len(sys.argv) > 6 else "audiofile.mp3"
        generate_cue(input_txt, album_title, artist_name, genre, year, audio_filename)