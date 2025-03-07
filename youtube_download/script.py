import csv

input_file = '/Users/kokugo/Desktop/scripts/youtube_download/youtube.csv'
output_file = '/Users/kokugo/Desktop/scripts/youtube_download/filtered_youtube2.csv'

def process_csv():
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Skip the header
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            video_url, video_name = row
            print(f"Video Name: {video_name}")
            keep = input("Do you want to keep this video? (y/N): ").strip().lower()
            if keep == 'y':
                writer.writerow(row)
            else:
                print("Video not saved.")

if __name__ == "__main__":
    process_csv()