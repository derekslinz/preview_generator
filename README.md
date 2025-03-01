# Video Preview Generator

This script allows you to generate a video preview by extracting frames or creating a short video composed of subclips from an input video file, merging them with Fade-In and Fade-Out transitions. It uses OpenCV for frame extraction and MoviePy for video processing.

## Features

- Extract a specified number of frames from a video.
- Create a video preview composed of multiple subclips.
- Option to include audio in the preview.
- Random or evenly spaced selection of subclips.
- Customizable resolution for the output video.

## Requirements

- Python 3.x
- OpenCV
- MoviePy

## Installation

1. Ensure you have python3 and the pyvenv module.

   ```bash
   git checkout https://github.com/derekslinz/preview_generator
   cd preview_generator
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command-line arguments:

```bash
python  video_preview_generator.py  [options] <video_path>
```

### Arguments

- `video_path`: Path to the input video file.

### Options

- `-t`, `--output_type`: Type of preview to generate (`frames` or `preview`). Default is `preview`.
- `-d`, `--output_dir`: Directory to save extracted frames. Default is `frames`.
- `-o`, `--output_path`: Path to save the preview video. Defaults to `<input_file>_preview.mp4`.
- `-f`, `--num_frames`: Number of frames to extract (for `frames`). Default is 10.
- `-c`, `--clip_duration`: Duration of each clip in seconds (for `preview`). Default is 2 seconds.
- `-n`, `--num_clips`: Number of clips to include (for `preview`). Default is 5.
- `-r`, `--resolution`: Resolution of the preview video in `WIDTHxHEIGHT` format. Default is `1280x720`.
- `-a`, `--include_audio`: Include audio in the preview video. Default is `True`.
- `--random_selection`: Select subclips randomly instead of evenly spaced. Default is `False`.

## Examples

Extract frames from a video:

```bash
python video_preview_generator.py  -t frames -f 20 example.mp4
```

Create a video preview with random subclips:

```bash
python video_preview_generator.py --random_selection example.mp4 
```

Create a video preview with custom resolution and no audio:

```bash
python video_preview_generator.py -r 1920x1080 -a False example.mp4 
```
Create a video preview with audio using 5 randomly selected subclips 3 seconds long
```bash
python video_preview_generator.py -a --random_selection -c 3 -n 5 example.mp4
```
## License

This project is licensed under the MIT License.
