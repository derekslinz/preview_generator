import os

import cv2
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut

from moviepy import VideoFileClip, concatenate_videoclips


def extract_frames(video_path, output_dir, num_frames=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(total_frames // num_frames, 1)

    frame_count = 0
    extracted_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0 and extracted_count < num_frames:
            frame_file = os.path.join(output_dir, f"frame_{extracted_count + 1:03d}.jpg")
            cv2.imwrite(frame_file, frame)
            extracted_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {extracted_count} frames to {output_dir}")


def create_video_preview(video_path, output_path, clip_duration=2, num_clips=5, resolution=(1280, 720)):
    # Open and resize the video clip
    clip = VideoFileClip(video_path).resized(resolution)
    duration = clip.duration
    interval = max(duration / num_clips, clip_duration)

    start_times = [i * interval for i in range(num_clips)]
    preview_clips = []

    for i, start in enumerate(start_times):
        end = min(start + clip_duration, duration)
        # Extract the subclip using the new API and set its duration
        subclip = clip.subclipped(start, end).with_duration(clip_duration)

        # Build a list of effects to apply.
        # For all but the first clip, add a fade-in effect.
        effects = []
        if i > 0:
            effects.append(FadeIn(duration=0.5))
        effects.append(FadeOut(duration=0.5))
        # Apply the effects using with_effects(), which returns a modified VideoFileClip.
        subclip = subclip.with_effects(effects)

        preview_clips.append(subclip)

    # Debug output
    print(f"Clips to concatenate: {preview_clips}")
    print(f"Clip types: {[type(clip) for clip in preview_clips]}")
    print(f"Clip durations: {[clip.duration for clip in preview_clips]}")

    # Concatenate the clips and write the output file
    preview = concatenate_videoclips(preview_clips, method="compose")
    preview.write_videofile(output_path, codec="libx264", audio=False)
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
    parser.add_argument("-r", "--resolution", type=str, default="640x480",
                        help="Resolution of the preview video (format: WIDTHxHEIGHT).")

    args = parser.parse_args()

    # Parse resolution argument
    width, height = map(int, args.resolution.split('x'))
    resolution = (width, height)

    # Default output path if not specified
    if args.output_path is None:
        base, ext = os.path.splitext(args.video_path)
        args.output_path = f"{base}_preview.mp4"

    if args.output_type == "frames":
        extract_frames(args.video_path, args.output_dir, args.num_frames)
    elif args.output_type == "preview":
        create_video_preview(args.video_path, args.output_path, args.clip_duration, args.num_clips, resolution)
