import os
import math
import json
from openai import OpenAI
from pydub import AudioSegment
from datetime import datetime

# CONFIGURATION
INPUT_DIR = "audio-input"
OUTPUT_DIR = "text-output"
PROCESSED_FILE = "processed_files.json"
CHUNK_LENGTH_MS = 10 * 60 * 1000  # 10 minutes in milliseconds
OPENAI_API_KEY = "YOUR API KEY"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create necessary directories
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def split_audio(audio_path, chunk_length_ms):
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"chunk_{i // chunk_length_ms}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks


def transcribe_chunk(chunk_path):
    with open(chunk_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text


def assign_roles(transcript):
    lines = transcript.strip().split(". ")
    speaker_toggle = True
    final_transcript = ""
    for line in lines:
        if len(line.strip()) < 2:
            continue
        speaker = "Person A" if speaker_toggle else "Person B"
        final_transcript += f"{speaker}: {line.strip()}\n"
        speaker_toggle = not speaker_toggle
    return final_transcript


def load_processed_files():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_processed_files(processed):
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(processed, f, indent=2)


def main():
    processed_files = load_processed_files()

    # Get all audio files from input directory
    audio_files = [f for f in os.listdir(INPUT_DIR)
                   if f.lower().endswith(('.mp3', '.m4a', '.wav', '.flac'))]

    for audio_file in audio_files:
        input_path = os.path.join(INPUT_DIR, audio_file)

        # Skip if already processed
        if input_path in processed_files:
            continue

        print(f"Processing {audio_file}...")
        output_file = os.path.join(OUTPUT_DIR,
                                   f"{os.path.splitext(audio_file)[0]}_transcript.txt")

        try:
            print("Splitting audio into chunks...")
            chunks = split_audio(input_path, CHUNK_LENGTH_MS)

            full_transcript = ""
            for chunk_path in chunks:
                try:
                    raw_text = transcribe_chunk(chunk_path)
                    with_roles = assign_roles(raw_text)
                    full_transcript += with_roles
                except Exception as e:
                    print(f"Error processing chunk {chunk_path}: {e}")
                finally:
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)

            # Save transcript
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_transcript)

            # Mark as processed
            processed_files[input_path] = {
                "processed_at": datetime.now().isoformat(),
                "output_file": output_file
            }
            save_processed_files(processed_files)

            print(f"Transcription complete! Output saved to '{output_file}'")

        except Exception as e:
            print(f"Error processing {audio_file}: {e}")

    if not audio_files:
        print("No new audio files to process in the input directory.")
    elif all(os.path.join(INPUT_DIR, f) in processed_files for f in audio_files):
        print("All files have already been processed.")


if __name__ == "__main__":
    main()
