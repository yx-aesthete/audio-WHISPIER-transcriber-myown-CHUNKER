import os
import json
from transcribe_anything.api import transcribe
from datetime import datetime


# #########################################################

# for using : 
# ./transcribe.sh

# #########################################################


# CONFIGURATION
INPUT_DIR = "audio-input"
OUTPUT_DIR = "text-output"
PROCESSED_FILE = "processed_files.json"

# Create necessary directories
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_processed_files():
    """Load the list of already processed files."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_processed_files(processed):
    """Save the list of processed files."""
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(processed, f, indent=2)


def transcribe_audio_file(input_path, output_file):
    """
    Transcribe an audio file using transcribe-anything library.
    This handles chunking and processing automatically.
    """
    print(f"Transcribing {input_path}...")
    
    try:
        # Create a temporary output directory for this file
        temp_output_dir = os.path.join(OUTPUT_DIR, "temp_transcribe")
        os.makedirs(temp_output_dir, exist_ok=True)
        
        # Use transcribe-anything library to transcribe the audio
        # The library handles chunking, multiple formats, and backend selection automatically
        result_path = transcribe(
            url_or_file=input_path,
            output_dir=temp_output_dir,
            model="medium",  # Use large model for better accuracy
            task="transcribe",  # transcribe vs translate
            device="mlx",  # Use CPU for compatibility (change to "cuda" if you have GPU)
        )
        
        print(f"Transcription completed. Output directory: {result_path}")
        
        # The transcribe function returns a path to the output directory
        # Look for transcript files (.txt, .vtt, .srt)
        transcript_files = []
        if os.path.exists(result_path):
            for file in os.listdir(result_path):
                if file.endswith(('.txt', '.vtt', '.srt')):
                    transcript_files.append(os.path.join(result_path, file))
        
        if transcript_files:
            # Use the .txt file if available, otherwise use the first one
            txt_files = [f for f in transcript_files if f.endswith('.txt')]
            transcript_file = txt_files[0] if txt_files else transcript_files[0]
            
            # Read the generated transcript
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript = f.read()
            
            # Save to our desired output location
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transcript)
            
            # Clean up temp directory
            import shutil
            shutil.rmtree(temp_output_dir, ignore_errors=True)
            
            print(f"Transcript saved to: {output_file}")
            return True
        else:
            print("No transcript file found in output directory")
            # Clean up temp directory
            import shutil
            shutil.rmtree(temp_output_dir, ignore_errors=True)
            return False
            
    except Exception as e:
        print(f"Error transcribing {input_path}: {e}")
        # Clean up temp directory on error
        temp_output_dir = os.path.join(OUTPUT_DIR, "temp_transcribe")
        if os.path.exists(temp_output_dir):
            import shutil
            shutil.rmtree(temp_output_dir, ignore_errors=True)
        return False


def main():
    """Main function to process all audio files in the input directory."""
    processed_files = load_processed_files()

    # Get all audio files from input directory
    audio_extensions = ('.mp3', '.m4a', '.wav', '.flac', '.mp4', '.avi', '.mov', '.mkv')
    audio_files = [f for f in os.listdir(INPUT_DIR)
                   if f.lower().endswith(audio_extensions)]

    if not audio_files:
        print("No audio files found in the input directory.")
        return

    print(f"Found {len(audio_files)} audio file(s) to process.")

    for audio_file in audio_files:
        input_path = os.path.join(INPUT_DIR, audio_file)

        # Skip if already processed
        if input_path in processed_files:
            print(f"Skipping {audio_file} (already processed)")
            continue

        print(f"Processing {audio_file}...")
        output_file = os.path.join(OUTPUT_DIR,
                                   f"{os.path.splitext(audio_file)[0]}_transcript.txt")

        try:
            success = transcribe_audio_file(input_path, output_file)
            
            if success:
                # Mark as processed
                processed_files[input_path] = {
                    "processed_at": datetime.now().isoformat(),
                    "output_file": output_file
                }
                save_processed_files(processed_files)
                print(f"✅ Successfully processed {audio_file}")
            else:
                print(f"❌ Failed to process {audio_file}")

        except Exception as e:
            print(f"❌ Error processing {audio_file}: {e}")

    # Check if all files have been processed
    processed_count = sum(1 for f in audio_files if os.path.join(INPUT_DIR, f) in processed_files)
    print(f"\n📊 Processing Summary:")
    print(f"   Total files: {len(audio_files)}")
    print(f"   Processed: {processed_count}")
    print(f"   Remaining: {len(audio_files) - processed_count}")
    
    if processed_count == len(audio_files):
        print("🎉 All files have been processed successfully!")


if __name__ == "__main__":
    main()
