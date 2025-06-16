#!/usr/bin/env python3
"""
Audio Transcription Tool - Auto Environment Wrapper
This script automatically activates the correct environment and runs the transcription.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the virtual environment
    venv_path = script_dir / "audio_transcribe_env"
    
    # Path to the Python executable in the virtual environment
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        python_exe = venv_path / "bin" / "python"
    
    # Path to the actual transcription script
    transcription_script = script_dir / "audioToNotes.py"
    
    # Check if virtual environment exists
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print(f"Expected location: {venv_path}")
        print("\nPlease run the setup first:")
        print("python3.12 -m venv audio_transcribe_env")
        print("source audio_transcribe_env/bin/activate")
        print("pip install transcribe-anything")
        return 1
    
    # Check if Python executable exists in venv
    if not python_exe.exists():
        print("❌ Python executable not found in virtual environment!")
        print(f"Expected location: {python_exe}")
        return 1
    
    # Check if transcription script exists
    if not transcription_script.exists():
        print("❌ Transcription script not found!")
        print(f"Expected location: {transcription_script}")
        return 1
    
    print("🚀 Starting Audio Transcription Tool...")
    print(f"📁 Working directory: {script_dir}")
    print(f"🐍 Using Python: {python_exe}")
    print(f"📄 Running script: {transcription_script}")
    print("-" * 50)
    
    try:
        # Run the transcription script using the virtual environment's Python
        result = subprocess.run([
            str(python_exe), 
            str(transcription_script)
        ], cwd=str(script_dir))
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⏹️  Transcription interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error running transcription: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 