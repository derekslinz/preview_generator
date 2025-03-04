import os
import random
from concurrent.futures import ThreadPoolExecutor

import cv2
from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from tqdm import tqdm


def save_frame(frame, output_dir, index):
    frame_file = os.path.join(output_dir, f"frame_{index:03d}.jpg")
    cv2.imwrite(frame_file, frame)


def extract_frames(video_path, output_dir, num_frames=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(total_frames // num_frames, 1)

    frame_count = 0
    extracted_count = 0

    with ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=num_frames, desc="Extracting frames") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % interval == 0 and extracted_count < num_frames:
                    future = executor.submit(save_frame, frame, output_dir, extracted_count + 1)
                    futures.append(future)
                    extracted_count += 1
                    pbar.update(1)

                frame_count += 1

        # Ensure all frames are saved
        for future in futures:
            future.result()

    cap.release()
    print(f"Extracted {extracted_count} frames to {output_dir}")


def create_video_preview(video_path, output_path, clip_duration=2, num_clips=5, resolution=(1280, 720),
                         include_audio=True, random_selection=False):
    clip = VideoFileClip(video_path).resized(resolution)
    duration = clip.duration
    avg_interval = duration / num_clips

    start_times = []
    if random_selection:
        for _ in range(num_clips):
            start_time = random.uniform(0, max(0, duration - clip_duration))
            start_times.append(start_time)
        start_times.sort()  # Sort to ensure chronological order
    else:
        start_times = [i * avg_interval for i in range(num_clips)]

    preview_clips = []
    for i, start in enumerate(start_times):
        end = min(start + clip_duration, duration)
        subclip = clip.subclipped(start, end).with_duration(clip_duration)

        effects = []
        if i > 0:
            effects.append(FadeIn(duration=0.5))
        effects.append(FadeOut(duration=0.5))
        subclip = subclip.with_effects(effects)

        preview_clips.append(subclip)

    preview = concatenate_videoclips(preview_clips, method="compose")
    preview.write_videofile(
        output_path,
        codec="libx264",
        audio=include_audio,
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        ffmpeg_params=["-b:a", "192k"]
    )
    print(f"Preview video saved to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a video preview.")
    parser.add_argument("video_path", help="Path to the input video file.")
    parser.add_argument("-t", "--output_type", choices=["frames", "preview"], default="preview",
                        help="Type of preview to generate.")
    parser.add_argument("-d", "--output_dir", default="frames", help="Directory to save extracted frames.")
    parser.add_argument("-o", "--output_path", help="Path to save the preview video.")
    parser.add_argument("-f", "--num_frames", type=int, default=10,
                        help="Number of frames to extract (for 'frames').")
    parser.add_argument("-c", "--clip_duration", type=int, default=2,
                        help="Duration of each clip (in seconds, for 'preview').")
    parser.add_argument("-n", "--num_clips", type=int, default=5,
                        help="Number of clips to include (for 'preview').")
    parser.add_argument("-r", "--resolution", type=str, default="1280x720",
                        help="Resolution of the preview video (format: WIDTHxHEIGHT).")
    parser.add_argument("-a", "--include_audio", action="store_true", default=True,
                        help="Include audio in the preview video.")
    parser.add_argument("--random_selection", action="store_true", default=False,
                        help="Select subclips randomly instead of evenly spaced.")

    args = parser.parse_args()

    width, height = map(int, args.resolution.split('x'))
    resolution = (width, height)

    if args.output_path is None:
        base, ext = os.path.splitext(args.video_path)
        args.output_path = f"{base}_preview.mp4"

    if args.output_type == "frames":
        extract_frames(args.video_path, args.output_dir, args.num_frames)
    elif args.output_type == "preview":
        create_video_preview(args.video_path, args.output_path, args.clip_duration, args.num_clips, resolution,
                             args.include_audio, args.random_selection)
