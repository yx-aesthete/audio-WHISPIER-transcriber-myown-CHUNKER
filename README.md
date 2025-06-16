# Audio Transcription Tool

An easy-to-use audio transcription tool that converts audio files to text using the powerful `transcribe-anything` library, which provides multiple whisper backends for optimal performance.

## Features

- **Multiple Format Support**: Supports MP3, M4A, WAV, FLAC, MP4, AVI, MOV, MKV files
- **Automatic Processing**: Handles chunking and processing automatically 
- **Processed Files Tracking**: Keeps track of already processed files to avoid duplicates
- **Multiple Backend Support**: Leverages transcribe-anything's multiple whisper backends
- **Error Handling**: Robust error handling and cleanup
- **Progress Tracking**: Clear progress indicators and summaries

## Installation

1. Install the required dependencies:
```bash
pip3 install transcribe-anything
```

## Usage

1. **Place your audio files** in the `audio-input/` directory
2. **Run the transcription tool**:
```bash
python3 audioToNotes.py
```
3. **Find your transcripts** in the `text-output/` directory

## Directory Structure

```
├── audioToNotes.py          # Main transcription script
├── audio-input/             # Place your audio files here
├── text-output/             # Transcribed text files appear here
├── processed_files.json     # Tracks which files have been processed
└── requirements.txt         # Python dependencies
```

## Configuration Options

You can modify these settings in `audioToNotes.py`:

- **Model Size**: Change `model="large"` to use different whisper model sizes (tiny, small, base, medium, large)
- **Device**: Change `device="cpu"` to `device="cuda"` if you have a GPU for faster processing
- **Task**: Change `task="transcribe"` to `task="translate"` to translate to English

## Advanced Usage

The tool uses the `transcribe-anything` library which supports multiple backends:

- **CPU Mode**: `device="cpu"` (default, works everywhere)
- **GPU Mode**: `device="cuda"` (Windows/Linux with NVIDIA GPU)
- **Insane Mode**: `device="insane"` (fastest GPU mode)
- **Mac Apple Silicon**: `device="mlx"` (optimized for M1/M2 Macs)

## Output

For each audio file `example.mp3`, the tool creates:
- `example_transcript.txt` - The transcribed text

## Processed Files Tracking

The tool maintains a `processed_files.json` file that tracks:
- Which files have been processed
- When they were processed  
- Where the output files are located

This prevents re-processing the same files and allows you to resume interrupted sessions.

## Error Handling

- Files that fail to process are logged but don't stop the batch
- Temporary files are automatically cleaned up
- Clear error messages help identify issues

## Performance Tips

1. **Use GPU**: Set `device="cuda"` if you have an NVIDIA GPU
2. **Use Smaller Models**: For faster processing, try `model="medium"` or `model="small"`
3. **Batch Processing**: Place multiple files in `audio-input/` to process them all at once

## Supported Audio Formats

- **Audio**: MP3, M4A, WAV, FLAC
- **Video**: MP4, AVI, MOV, MKV (audio track will be extracted)

## Benefits Over Previous Version

- ✅ **No API Keys Required**: No need for OpenAI API keys
- ✅ **Better Performance**: Multiple optimized backends
- ✅ **Automatic Chunking**: Handles long files automatically
- ✅ **More Formats**: Supports video files and more audio formats
- ✅ **Simpler Setup**: Just install and run
- ✅ **Better Error Handling**: More robust processing
- ✅ **Cross-Platform**: Works on Windows, Mac, and Linux

## Troubleshooting

1. **Import Error**: Make sure transcribe-anything is installed: `pip3 install transcribe-anything`
2. **GPU Issues**: Start with `device="cpu"` to ensure basic functionality
3. **Memory Issues**: Use smaller models like `model="small"` for limited RAM
4. **Permission Issues**: Ensure the script has write access to the directory

## License

This tool uses the transcribe-anything library which is MIT licensed. 