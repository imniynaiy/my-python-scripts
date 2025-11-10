from dotenv import load_dotenv
load_dotenv()

from utils import get_audio_file_abs_uri
import os
import subprocess
from datetime import datetime
from openai import OpenAI

#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

import sys

from dashscope import MultiModalConversation
from pathlib import Path

def create_markdown(audio_file, date_str):
    # 将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频的绝对路径，
    # 本地文件的完整路径必须以 file:// 为前缀，以保证路径的合法性，例如：file:///home/images/test.mp3
    audio_file_path = get_audio_file_abs_uri(audio_file)
    prompt = """你将扮演一位秘书。这是一段语音转写文字，将它改为日记。summarize it into bullet points in md, with four categories as header: developer, thoughts, mood, entertainment and todo. 尽可能用我的原话，但是要去掉嗯啊语气词和重复。"""

    messages = [
        {
            "role": "system", 
            "content": [{"text": prompt}]},
        {
            "role": "user",
            # 在 audio 参数中传入以 file:// 为前缀的文件路径
            "content": [{"audio": audio_file_path}],
        }
    ]

    directory = os.path.dirname(audio_file)

    response = MultiModalConversation.call(model="qwen-audio-turbo-latest", messages=messages)
    markdown = response["output"]["choices"][0]["message"].content[0]["text"]
    
    # Parse date and get weekday
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    weekday = date_obj.strftime('%A')
    filename = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}, {weekday}.md"

    filename = os.path.join(directory, filename)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown)
    return filename    

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_markdown_omni.py <audio_file> <date_string(yyyymmdd)>")
        sys.exit(1)

    audio_file = sys.argv[1]
    date_str = sys.argv[2]

    # Create markdown file
    output_file = create_markdown(audio_file, date_str)
    print(f"Created diary entry: {output_file}")

if __name__ == "__main__":
    main()