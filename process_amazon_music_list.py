## This files is for converting the Amazon music list to a format that can be used by the https://www.tunemymusic.com/

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        for i in range(0, len(lines), 6):
            if i + 3 < len(lines):
                track_info = f"{lines[i+1].strip()} - {lines[i+3].strip()}\n"
                outfile.write(track_info)

process_file('./temp/to_process_amaazon.txt', './temp/processed_amazon.txt')