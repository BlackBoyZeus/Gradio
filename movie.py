import gradio as gr
import os
from moviepy.editor import VideoFileClip


def convert_video_color(video_path, output_path):
    video = VideoFileClip(video_path)
    converted_video = video.fx(lambda frame: frame[:, :, ::-1])  # Convert RGB to BGR
    converted_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path


def video_identity(video):
    if isinstance(video, str):
        # Check if the video format is supported
        ext = os.path.splitext(video)[1].lower()
        if ext in ['.mp4', '.ogg', '.webm']:
            return video
        else:
            # Convert the video to a playable mp4 format
            output_path = os.path.splitext(video)[0] + '.mp4'
            try:
                return convert_video_color(video, output_path)
            except Exception as e:
                print(f"Video conversion failed: {e}")
                return video
    elif isinstance(video, tuple):
        video_path, subtitle_path = video
        # Check if the video format is supported
        ext = os.path.splitext(video_path)[1].lower()
        if ext in ['.mp4', '.ogg', '.webm']:
            return video
        else:
            # Convert the video to a playable mp4 format
            output_path = os.path.splitext(video_path)[0] + '.mp4'
            try:
                return convert_video_color(video_path, output_path), subtitle_path
            except Exception as e:
                print(f"Video conversion failed: {e}")
                return video
    else:
        return video


demo = gr.Interface(
    video_identity,
    gr.Video(),
    "playable_video",
    examples=[
        os.path.join(os.path.dirname(__file__), "feb1-1.mp4")
    ],
    cache_examples=True,
)

if __name__ == "__main__":
    demo.launch()
