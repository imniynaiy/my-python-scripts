from dotenv import load_dotenv
load_dotenv()
import os
import subprocess
from datetime import datetime
from openai import OpenAI

#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

import sys

def process_with_chatgpt(transcript):
    """Process transcript with ChatGPT"""
    prompt = """你将扮演一位秘书。这是一段语音转写文字，将它改为日记。summarize it into bullet points in md, with four categories as header: developer, thoughts, mood, entertainment and todo. 尽可能用我的原话，但是要去掉嗯啊语气词和重复。"""

    response = client.chat.completions.create(model="qwen-plus", # insteadof gpt-5
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": transcript}
    ])
    return response.choices[0].message.content

def create_markdown(directory, date_str, summary):
    """Create markdown file with summary and transcript"""
    # Parse date and get weekday
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    weekday = date_obj.strftime('%A')
    filename = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}, {weekday}.md"

    filename = os.path.join(directory, filename)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(summary)
    return filename

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_markdown_text.py <transcript_file> <date_string(yyyymmdd)>")
        sys.exit(1)

    transcript_file = sys.argv[1]
    date_str = sys.argv[2]

    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # Process with ChatGPT
    summary = process_with_chatgpt(transcript)

    directory = os.path.dirname(transcript_file)

    # Create markdown file
    output_file = create_markdown(directory, date_str, summary)
    print(f"Created diary entry: {output_file}")

    # Cleanup
    # os.remove('temp.wav')
    # os.remove('temp.txt')

if __name__ == "__main__":
    main()