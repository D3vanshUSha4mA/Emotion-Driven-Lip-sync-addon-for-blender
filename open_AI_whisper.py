import argparse
import os
import sys
import json
import csv
import whisper
from g2p_en import G2p
import re

# Phoneme to Viseme Mapping (Your existing mapping is used here)
PHONEME_TO_VISEME = {
    "REST": "Rest/Neutral",
    "P": "ClosedLips", "B": "ClosedLips", "M": "ClosedLips",
    "AA": "LipOpenSmall", "AH": "LipOpenSmall", "AO": "LipOpenSmall",
    "AE": "LipWide", "EH": "LipWide", "AY": "LipWide",
    "AW": "LipOpenBig", "EY": "LipOpenBig",
    "UW": "OO", "UH": "OO", "OW": "OO",
    "IY": "EE", "IH": "EE", "Y": "EE",
    "F": "FV", "V": "FV",
    "TH": "TH", "DH": "TH",
    "CH": "ChSh", "JH": "ChSh", "SH": "ChSh", "ZH": "ChSh", "S": "ChSh", "Z": "ChSh",
    "K": "KG", "G": "KG", "NG": "KG",
    "L": "LR", "R": "LR"
}

def remove_stress(phoneme_list):
    return [re.sub(r'\d$', '', p) for p in phoneme_list]

def classify_viseme(ph):
    return PHONEME_TO_VISEME.get(ph.upper(), "REST")

def main(audio_path, out_json_path=None):
    print(f"Python executable running this script: {sys.executable}")

    if not os.path.exists(audio_path):
        print(f"ERROR: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(2)

    # Use the provided output path if available, otherwise use a default relative to the audio file
    if out_json_path is None:
        out_json_path = os.path.splitext(audio_path)[0] + "_phonemes.json"
    
    save_dir = os.path.dirname(out_json_path)
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Load Whisper model (ensure it's installed in the external Python environment)
    model = whisper.load_model("base")
    print("Transcribing with Whisper... (this may take some time)")
    result = model.transcribe(audio_path, word_timestamps=True)

    word_timings = []
    if "segments" in result:
        for segment in result["segments"]:
            if "words" in segment:
                for word in segment["words"]:
                    w = word["word"].strip()
                    start = word.get("start", None)
                    end = word.get("end", None)
                    if start is None or end is None:
                        continue
                    word_timings.append((w, float(start), float(end)))

    g2p = G2p()
    phoneme_timings = []

    # Process word timings into phoneme/viseme timings (using average duration)
    for w, start, end in word_timings:
        phonemes = g2p(w)
        phonemes = remove_stress(phonemes)
        phonemes = [p for p in phonemes if p.isalpha()]
        
        # Add a rest viseme if there's a gap before the word starts (heuristic)
        if phoneme_timings and start > phoneme_timings[-1]['end'] + 0.05:
             # Insert a 'Rest' gap
             phoneme_timings.append({
                 "phoneme": "REST",
                 "start": round(phoneme_timings[-1]['end'], 4),
                 "end": round(start, 4),
                 "word": "",
                 "viseme": "Rest/Neutral"
             })

        if not phonemes:
            # Handle words that can't be transcribed (e.g., numbers, punctuation)
            continue
            
        duration = (end - start) / len(phonemes)
        current_start = start
        
        for ph in phonemes:
            ph_start = current_start
            ph_end = ph_start + duration
            viseme = classify_viseme(ph)
            
            phoneme_timings.append({
                "phoneme": ph,
                "start": round(ph_start, 4),
                "end": round(ph_end, 4),
                "word": w,
                "viseme": viseme
            })
            current_start = ph_end

    # Write final JSON output
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump({"phoneme_timings": phoneme_timings}, f, indent=2)

    print("Phoneme timings JSON saved to:", out_json_path)
    print(out_json_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--out", required=False, help="Path to output JSON (phoneme timings)")
    args = parser.parse_args()
    main(args.audio, args.out)