import sys


def attach_transcript_to_file(transcript_file, markdown_file):
    """Attach transcript to the end of the markdown file"""
    with open(transcript_file, 'r', encoding='utf-8') as tf:
        transcript = tf.read()

    with open(markdown_file, 'a', encoding='utf-8') as mf:
        mf.write(f"\n\n## Transcript\n```\n{transcript}\n```")

def main():
    if len(sys.argv) != 3:
        print("Usage: python attach_transcript_to_file.py <transcript_file> <markdown_file>")
        sys.exit(1)

    transcript_file = sys.argv[1]
    markdown_file = sys.argv[2]

    attach_transcript_to_file(transcript_file, markdown_file)

if __name__ == "__main__":
    main()

