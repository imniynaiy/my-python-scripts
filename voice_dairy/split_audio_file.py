import argparse
import sys
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import detect_silence

#!/usr/bin/env python3
"""
split_audio_file.py

Usage:
    python split_audio_file.py /path/to/audiofile.mp3 3

Splits the audio file into X parts, preferring to cut on silent regions.
Outputs files named basename_1.ext ... basename_X.ext in the same folder.
"""



def find_silent_cut_positions(audio, parts, min_silence_len=700, silence_thresh_delta=16, search_radius_ms=5000):
        total_ms = len(audio)
        if parts <= 1:
                return []

        # detect silence intervals [(start_ms, end_ms), ...]
        silence_thresh = audio.dBFS - silence_thresh_delta
        silences = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh, seek_step=100)
        # normalize silence intervals
        silences = [(max(0, s), min(total_ms, e)) for s, e in silences]

        targets = [(i * total_ms) // parts for i in range(1, parts)]
        cuts = []
        for t in targets:
                # find silences that overlap the search window around target
                window_start = max(0, t - search_radius_ms)
                window_end = min(total_ms, t + search_radius_ms)
                candidates = []
                for s, e in silences:
                        if e >= window_start and s <= window_end:
                                center = (s + e) // 2
                                candidates.append((abs(center - t), center, s, e))
                if candidates:
                        # choose candidate whose center is closest to target
                        _, center, s, e = min(candidates, key=lambda x: x[0])
                        cuts.append(int(center))
                else:
                        # fallback to exact target
                        cuts.append(int(t))
        # ensure cuts are strictly increasing and in bounds
        cleaned = []
        last = 0
        for c in cuts:
                c = min(max(last + 1, c), total_ms - 1)
                cleaned.append(c)
                last = c
        return cleaned


def export_segments(audio, cuts, src_path, out_dir):
        total_ms = len(audio)
        boundaries = [0] + cuts + [total_ms]
        src = Path(src_path)
        stem = src.stem
        ext = src.suffix.lstrip(".")
        out_paths = []
        for i in range(len(boundaries) - 1):
                start = boundaries[i]
                end = boundaries[i + 1]
                segment = audio[start:end]
                out_name = f"{stem}_{i+1}.{ext}"
                out_path = Path(out_dir) / out_name
                # export uses format param without dot
                segment.export(out_path.as_posix(), format=ext)
                out_paths.append(out_path.as_posix())
        return out_paths

def cut_audio(audio_path, parts, min_silence_ms=700, silence_delta_db=16, search_radius_ms=5000):
                src = Path(audio_path)
                if not src.exists() or not src.is_file():
                        print("Error: audio file not found.", file=sys.stderr)
                        sys.exit(2)
                if parts <= 0:
                        print("Error: parts must be a positive integer.", file=sys.stderr)
                        sys.exit(2)

                try:
                        audio = AudioSegment.from_file(src.as_posix())
                except Exception as e:
                        print(f"Error loading audio: {e}", file=sys.stderr)
                        sys.exit(3)

                cuts = find_silent_cut_positions(
                        audio,
                        parts=parts,
                        min_silence_len=min_silence_ms,
                        silence_thresh_delta=silence_delta_db,
                        search_radius_ms=search_radius_ms,
                )

                out_dir = src.parent
                out_paths = export_segments(audio, cuts, src.as_posix(), out_dir)
                return out_paths

def main():
        parser = argparse.ArgumentParser(description="Split an audio file into X parts, preferring silent cuts.")
        parser = argparse.ArgumentParser(description="Split an audio file into X parts, preferring silent cuts.")
        parser.add_argument("audio", help="Path to audio file (wav, mp3, etc.)")
        parser.add_argument("parts", type=int, help="Number of parts to split into (integer > 0)")
        parser.add_argument("--min-silence-ms", type=int, default=700, help="Minimum silence length to consider (ms)")
        parser.add_argument("--silence-delta-db", type=int, default=16, help="Silence threshold = audio.dBFS - delta_db")
        parser.add_argument("--search-radius-ms", type=int, default=5000, help="Search radius around target cut (ms)")
        args = parser.parse_args()
        
        out_paths = cut_audio(
                args.audio,
                args.parts,
                args.min_silence_ms,
                args.silence_delta_db,
                args.search_radius_ms,
        )

        # print output filenames (one per line)
        for p in out_paths:
                print(p)


if __name__ == "__main__":
        main()