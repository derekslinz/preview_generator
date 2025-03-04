# Video Preview Generator

This script allows you to generate a video preview by creating a short video composed of subclips from an input video
file, merging them with Fade-In and Fade-Out transitions. It uses MoviePy for video processing.

## Features

- Create a video preview composed of multiple subclips.
- Option to include audio in the preview.
- Random or evenly spaced selection of subclips.
- Customizable resolution for the output video.

## Requirements

- Python 3.x
- MoviePy
- ffmpeg-python
- Tkinter (for GUI)

## Installation

1. Clone the repository and set up a virtual environment:

   ```bash
   git clone https://github.com/derekslinz/preview_generator
   cd preview_generator
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

GUI mode launches if no command-line arguments are specified, or run the script in cli mode with the following options.

### Options

- `-t`, `--output_type`: Type of preview to generate (`frames` or `preview`). Default is `preview`.
- `-d`, `--output_dir`: Directory to save extracted frames. Default is `frames`.
- `-o`, `--output_path`: Path to save the preview video. Defaults to `<input_file>_preview.mp4`.
- `-f`, `--num_frames`: Number of frames to extract (for `frames`). Default is 10.
- `-c`, `--clip_duration`: Duration of each clip in seconds (for `preview`). Default is 2 seconds.
- `-n`, `--num_clips`: Number of clips to include (for `preview`). Default is 5.
- `-r`, `--resolution`: Resolution of the preview video in `WIDTHxHEIGHT` format. Default is `1280x720`.
- `-a`, `--include_audio`: Include audio in the preview video. Default is `True`.
- `-R`, `--random_selection`: Select subclips randomly instead of evenly spaced. Default is `False`.

## Examples

```bash
python video_preview_generator.py --random_selection -v example.mp4 -o example_preview.mp4
```

Create a video preview with custom resolution and no audio:

```bash
python video_preview_generator.py -r 1920x1080 -a False -v example.mp4 -o example_preview.mp4
```

Create a video preview with audio using 5 randomly selected subclips 3 seconds long:

```bash
python video_preview_generator.py -a --random_selection -c 3 -n 5 -v example.mp4 -o example_preview.mp4
```

This project is licensed under the MIT License.
