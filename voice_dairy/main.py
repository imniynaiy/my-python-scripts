from dotenv import load_dotenv
load_dotenv()
import os
import subprocess
from datetime import datetime
from openai import OpenAI

#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)
from pathlib import Path
import sys



def merge_audio_files(directory, output_file="temp.wav"):
    """Merge all audio files in directory into one wav file"""
    # Find all mp3 and m4a files
    audio_files = []
    for ext in ['.mp3', '.m4a', '.MP3', '.M4A']:
        audio_files.extend(list(Path(directory).glob(f'*{ext}')))

    if not audio_files:
        print("No audio files found")
        return False

    file_list_path = os.path.join(directory, 'files.txt')
    # Create ffmpeg input file list
    with open(file_list_path, 'w') as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    # Merge files using ffmpeg
    output_file = os.path.join(directory, output_file)
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0', 
        '-i', file_list_path,
        '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',
        output_file
    ]
    subprocess.run(cmd, check=True)
    # os.remove(file_list_path)
    return True

def transcribe_audio(directory, input_file="temp.wav", output_file="temp"):
    """Transcribe audio using whisper"""
    input_file = os.path.join(directory, input_file)
    output_file = os.path.join(directory, output_file)
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

def process_with_chatgpt(transcript):
    """Process transcript with ChatGPT"""
    prompt = """你将扮演一位秘书。这是一段语音转写文字，将它改为日记。summarize it into bullet points in md, with four categories as header: developer, thoughts, mood, entertainment and todo. 尽可能用我的原话，但是要去掉嗯啊语气词和重复。"""

    response = client.chat.completions.create(model="qwen-plus", # insteadof gpt-5
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": transcript}
    ])
    return response.choices[0].message.content

def create_markdown(directory, date_str, summary, transcript):
    """Create markdown file with summary and transcript"""
    # Parse date and get weekday
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    weekday = date_obj.strftime('%A')
    filename = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}, {weekday}.md"

    filename = os.path.join(directory, filename)
    content = f"{summary}\n\n## Transcript\n```\n{transcript}\n```"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <directory> <date_string(yyyymmdd)>")
        sys.exit(1)

    directory = sys.argv[1]
    date_str = sys.argv[2]

    # Merge audio files
    if not merge_audio_files(directory):
       sys.exit(1)

    # Transcribe audio
    transcribe_audio(directory=directory)

    output_txt = os.path.join(directory, 'temp.txt')

    # Read transcript
    with open(output_txt, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # Process with ChatGPT
    summary = process_with_chatgpt(transcript)

    # Create markdown file
    output_file = create_markdown(directory, date_str, summary, transcript)
    print(f"Created diary entry: {output_file}")

    # Cleanup
    # os.remove('temp.wav')
    # os.remove('temp.txt')

if __name__ == "__main__":
    main()