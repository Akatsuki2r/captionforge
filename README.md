# CaptionForge

CaptionForge is a local, desktop application built with Python and PySide6 designed to help you generate, edit, and burn subtitles into your videos efficiently and entirely offline.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- **Local Transcription**: Uses `faster-whisper` (Tiny/Small models) to transcribe audio files locally, preserving privacy.
- **Manual Editing**: Edit generated captions in an intuitive, editable table view.
- **Subtitle Export**: Exports to `.srt` or `.ass` formats.
- **Subtitle Burning**: Uses `FFmpeg` to hard-burn subtitles into `.mp4` videos.
- **Clean UI**: A modern, dark-themed interface built with PySide6.

## Prerequisites

- **Python 3.10 or higher**.
- **FFmpeg**: Required for subtitle burning.
  - *Ubuntu/Debian*: `sudo apt update && sudo apt install ffmpeg`
  - *macOS*: `brew install ffmpeg`
- **Hugging Face Token** (Optional but Recommended): To avoid rate limits and improve model download speeds from the Hub. Create one at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd captionforge
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Hugging Face Access (Optional)**:
   To prevent unauthenticated request warnings and improve performance, set your token as an environment variable in your terminal session:
   ```bash
   export HF_TOKEN="your_hf_token_here"
   ```
   *Note: For convenience, you can add this line to your `~/.bashrc` or `~/.zshrc` file to make it permanent.*

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```
2. **Workflow**:
   - Click **Load Audio** to import your source audio file.
   - Click **Generate Captions** to transcribe audio using Whisper.
   - Edit the text/timestamps directly in the table.
   - Click **Load Video** to select the target video file.
   - Click **Burn Subtitles** to export the final video with subtitles applied.

## Contributing

Contributions are welcome! If you'd like to contribute to CaptionForge, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3. **Commit your changes** with descriptive commit messages.
4. **Push your branch** and open a Pull Request.

Please ensure your code follows the established modular architecture and maintains the project's dependency standards.
