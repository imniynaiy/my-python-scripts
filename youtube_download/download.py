import csv
import subprocess

# Path to the CSV file
csv_file_path = '/Users/kokugo/Desktop/scripts/youtube_download/filtered_youtube2.csv'

# Read the CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        video_url = row[0]
        # Download the video using yt-dlp
        subprocess.run(['yt-dlp','-f','140', video_url])