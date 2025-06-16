#!/bin/bash

# Audio Transcription Tool - Simple Runner
# This script activates the virtual environment and runs the transcription

echo "🚀 Starting Audio Transcription Tool..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "audio_transcribe_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run the setup first:"
    echo "python3.12 -m venv audio_transcribe_env"
    echo "source audio_transcribe_env/bin/activate"
    echo "pip install transcribe-anything"
    exit 1
fi

# Activate virtual environment and run transcription
echo "🔧 Activating virtual environment..."
source audio_transcribe_env/bin/activate

echo "🎵 Running transcription..."
python audioToNotes.py

echo "✅ Done!" 