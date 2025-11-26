from dotenv import load_dotenv
load_dotenv()
import os
import sys
import dashscope
from pydub import AudioSegment

from utils.get_file_abs_uri import get_file_abs_uri
from split_audio_file import export_segments

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

MAX_AUDIO_LENGTH_MS = 60_000  # 1 minutes in milliseconds

def split_and_transcribe(input_file, output_file="temp"):
    audio = AudioSegment.from_file(input_file)
    
    if len(audio) > MAX_AUDIO_LENGTH_MS:
        parts = (len(audio) + MAX_AUDIO_LENGTH_MS - 1) // MAX_AUDIO_LENGTH_MS
        # Split audio and transcribe each chunk
        chunks = export_segments(input_file, parts)
        for chunk in chunks:
            transcribe_audio(chunk, output_file)
    else:
        # Audio is short enough, transcribe directly
        transcribe_audio(input_file, output_file)

def transcribe_audio(input_file, output_file="temp"):
    audio_file_path = get_file_abs_uri(input_file)

    messages = [
        {
            "role": "system",
            "content": [
                # 此处用于配置定制化识别的Context
                {"text": ""},
            ]
        },
        {
            "role": "user",
            "content": [
                {"audio": audio_file_path},
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-asr-flash",
        messages=messages,
        result_format="message",
        asr_options={
            # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
            "enable_itn":True
        }
    )
    if response.status_code == 200:
        # Extract text from the response structure
        result = response.output.choices[0].message.content[0]['text']
        print(result)
        
        # Append to output file if specified (do not clear existing content)
        if output_file:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(result)
                f.write('\n')
                
        return True
    else:
        print(f"Error: {response.message}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python transcribe_audio.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not split_and_transcribe(input_file, output_file):
       sys.exit(1)

if __name__ == "__main__":
    main()