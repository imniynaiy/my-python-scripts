import tiktoken
import sys

def count_tokens_openai(text, model="gpt-4"):
    """Count tokens for OpenAI models"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

# Example usage
if len(sys.argv) < 2:
    print("Usage: python count_token.py <filename>")
    sys.exit(1)
filename = sys.argv[1]
with open(filename, "r", encoding="utf-8") as f:
    prompt = f.read()
token_count = count_tokens_openai(prompt)
print(f"{token_count}")