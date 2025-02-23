'''
Author: Diana Tang
Date: 2025-02-18 10:51:37
LastEditors: Diana Tang
Description: some description
FilePath: /add-srt-compress-video/main-ffmpeg.py
'''
import os
import cv2
import whisper
import moviepy.editor as mp
import subprocess

# 设置文件路径
video_path = "./videos/绪论1中文.mp4"
audio_path = "./videos/1.1.wav"
output_video_path = "./videos/绪论1有字幕.mp4"
final_output_path="./videos/绪论1有字幕音频.mp4"
subtitle_path = "./videos/subtitles.srt"

# 提取视频中的音频并保存为 WAV 格式
command = [
    "ffmpeg",
    "-i", video_path,          # 输入文件
    "-ac", "1",                # 设置音频为单声道
    "-ar", "16000",            # 设置采样率为 16kHz
    "-y",                      # 如果文件已存在则覆盖
    audio_path                  # 输出文件路径
]
subprocess.run(command)

# 加载 Whisper 模型
model = whisper.load_model("turbo")

# 使用 Whisper 进行语音识别
result = model.transcribe(audio_path)

# 生成 SRT 字幕文件
def generate_srt_file(subtitle_path, segments):
    os.makedirs(os.path.dirname(subtitle_path), exist_ok=True)
    if not segments:
        print("未识别到任何内容，字幕文件将为空。")
    with open(subtitle_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"].strip()

            if not text:
                continue

            # 格式化时间戳
            start_hours, start_remainder = divmod(start_time, 3600)
            start_minutes, start_seconds = divmod(start_remainder, 60)
            start_milliseconds = int((start_seconds % 1) * 1000)
            start_seconds = int(start_seconds)

            end_hours, end_remainder = divmod(end_time, 3600)
            end_minutes, end_seconds = divmod(end_remainder, 60)
            end_milliseconds = int((end_seconds % 1) * 1000)
            end_seconds = int(end_seconds)

            f.write(f"{i + 1}\n")
            f.write(f"{int(start_hours):02}:{int(start_minutes):02}:{int(start_seconds):02},{start_milliseconds:03} --> {int(end_hours):02}:{int(end_minutes):02}:{int(end_seconds):02},{end_milliseconds:03}\n")
            f.write(f"{text}\n\n")

# 调用生成 SRT 文件的函数
generate_srt_file(subtitle_path, result["segments"])


# 使用 ffmpeg 将原始音频和字幕叠加到最终输出视频中
command = [
    "ffmpeg",
    "-i", video_path,      # 输入没有音频的视频
    # "-i", audio_path,             # 输入原始音频
    "-vf", f"subtitles='{subtitle_path}'",  # 添加字幕
    "-c:v", "libx264",           # 使用 H.264 编码视频
    "-c:a", "aac",               # 使用 AAC 编码音频
    "-b:a", "192k",              # 设置音频比特率
    "-movflags", "+faststart",   # 优化视频播放
    "-y",                         # 如果文件已存在则覆盖
    final_output_path              # 输出带有音频和字幕的视频
]

subprocess.run(command)

print(f"字幕已取得并保存为 {final_output_path}")
