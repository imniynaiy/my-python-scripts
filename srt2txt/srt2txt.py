#!/usr/bin/env python3
"""
srt_to_txt.py

Simple utility to convert a SubRip (.srt) file to plain text (.txt).
Usage:
    python srt_to_txt.py input.srt [-o output.txt]

The script:
 - removes subtitle indices and timestamp lines
 - joins multi-line subtitles into single lines
 - unescapes HTML entities and strips basic tags like <i>
"""

import argparse
import os
import re
import sys
import html

TIMESTAMP_RE = re.compile(r'^\s*\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}\s*$')
INDEX_RE = re.compile(r'^\s*\d+\s*$')
HTML_TAG_RE = re.compile(r'<[^>]+>')

def srt_to_lines(text):
    # Split into blocks separated by one or more blank lines
    blocks = re.split(r'\n\s*\n', text.strip(), flags=re.MULTILINE)
    out_lines = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip() != '']
        if not lines:
            continue
        # Remove index line if present
        if INDEX_RE.match(lines[0]):
            lines = lines[1:]
            if not lines:
                continue
        # Remove timestamp line if present
        if lines and TIMESTAMP_RE.match(lines[0]):
            lines = lines[1:]
        # Join remaining lines of this block into one line
        if not lines:
            continue
        joined = ' '.join(lines)
        # Remove simple HTML tags and unescape entities
        joined = HTML_TAG_RE.sub('', joined)
        joined = html.unescape(joined)
        # Collapse multiple spaces
        joined = re.sub(r'\s+', ' ', joined).strip()
        if joined:
            out_lines.append(joined)
    return out_lines

def main():
    parser = argparse.ArgumentParser(description='Convert .srt subtitles to plain .txt')
    parser.add_argument('input', help='input .srt file')
    parser.add_argument('-o', '--output', help='output .txt file (optional)')
    args = parser.parse_args()

    inp = args.input
    if not os.path.isfile(inp):
        print(f'Error: input file not found: {inp}', file=sys.stderr)
        sys.exit(2)

    out = args.output
    if not out:
        base, ext = os.path.splitext(inp)
        out = base + '.txt'

    with open(inp, 'r', encoding='utf-8', errors='replace') as f:
        srt_text = f.read()

    lines = srt_to_lines(srt_text)

    # Write lines separated by a blank line between subtitle blocks (optional).
    # Here we keep each subtitle on its own line.
    with open(out, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

    print(f'Converted: {inp} -> {out}')

if __name__ == '__main__':
    main()