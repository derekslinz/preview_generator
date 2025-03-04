import random
import tkinter as tk
from tkinter import filedialog, messagebox

from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut


def create_video_preview(video_path, output_file_name, clip_duration=2, num_clips=5, resolution=(1280, 720),
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
        output_file_name,
        codec="libx264",
        audio=include_audio,
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        ffmpeg_params=["-b:a", "192k"]
    )
    print(f"Preview video saved to {output_file_name}")


def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.m4v *.mkv")])
    if file_path:
        video_path_var.set(file_path)


def run_preview():
    video_path = video_path_var.get()
    output_file_name = output_file_name_var.get()
    clip_duration = int(clip_duration_var.get())
    num_clips = int(num_clips_var.get())
    resolution = tuple(map(int, resolution_var.get().split('x')))
    include_audio = include_audio_var.get()
    random_selection = random_selection_var.get()

    if not video_path or not output_file_name:
        messagebox.showerror("Error", "Please specify both video file and output path.")
        return

    create_video_preview(video_path, output_file_name, clip_duration, num_clips, resolution, include_audio,
                         random_selection)


app = tk.Tk()
app.title("Video Processing Tool")

video_path_var = tk.StringVar()
output_dir_var = tk.StringVar()
output_file_name_var = tk.StringVar()
num_frames_var = tk.StringVar(value="10")
clip_duration_var = tk.StringVar(value="2")
num_clips_var = tk.StringVar(value="5")
resolution_var = tk.StringVar(value="1280x720")
include_audio_var = tk.BooleanVar(value=True)
random_selection_var = tk.BooleanVar(value=True)

tk.Label(app, text="Video File:").grid(row=0, column=0, sticky="e")
tk.Entry(app, textvariable=video_path_var, width=50).grid(row=0, column=1)
tk.Button(app, text="Browse", command=select_video_file).grid(row=0, column=2)

tk.Label(app, text="Output File Name:").grid(row=2, column=0, sticky="e")
tk.Entry(app, textvariable=output_file_name_var, width=50).grid(row=2, column=1)

tk.Label(app, text="Clip Duration (s):").grid(row=4, column=0, sticky="e")
tk.Entry(app, textvariable=clip_duration_var, width=10).grid(row=4, column=1, sticky="w")

tk.Label(app, text="Number of Clips:").grid(row=5, column=0, sticky="e")
tk.Entry(app, textvariable=num_clips_var, width=10).grid(row=5, column=1, sticky="w")

tk.Label(app, text="Resolution:").grid(row=6, column=0, sticky="e")
tk.Entry(app, textvariable=resolution_var, width=10).grid(row=6, column=1, sticky="w")

tk.Checkbutton(app, text="Include Audio", variable=include_audio_var).grid(row=7, column=1, sticky="w")
tk.Checkbutton(app, text="Random Selection", variable=random_selection_var).grid(row=8, column=1, sticky="w")

tk.Button(app, text="Create Preview", command=run_preview).grid(row=9, column=1, pady=10)

app.mainloop()
