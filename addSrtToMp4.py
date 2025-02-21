'''
Author: Diana Tang
Date: 2025-02-21 23:41:46
LastEditors: Diana Tang
Description: some description
FilePath: /add-srt-compress-video/addSrtToMp4.py
'''
import os
from moviepy import VideoFileClip
import speech_recognition as sr

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def generate_srt_from_audio(audio_path, srt_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        # 识别音频中的文字
        text = recognizer.recognize_google(audio, language="zh-CN")
        # 创建 SRT 文件
        with open(srt_path, "w", encoding="utf-8") as f:
            # 简单地将识别到的文本按行分割作为示例
            lines = text.split(". ")
            for i, line in enumerate(lines):
                start_time = i * 3  # 假设每段文本持续3秒
                end_time = start_time + 3
                f.write(f"{i+1}\n")
                f.write(f"{start_time // 60:02d}:{start_time % 60:02d},000 --> {end_time // 60:02d}:{end_time % 60:02d},000\n")
                f.write(f"{line.strip()}\n\n")
    except Exception as e:
        print(f"错误: {e}")

def process_mp4_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            video_path = os.path.join(folder_path, filename)
            audio_path = video_path.replace(".mp4", ".wav")
            srt_path = video_path.replace(".mp4", ".srt")
            
            # 提取音频并生成 SRT 文件
            extract_audio_from_video(video_path, audio_path)
            generate_srt_from_audio(audio_path, srt_path)
            print(f"已处理: {filename}")

# 输入文件夹路径
folder_path = "./videos"
process_mp4_files_in_folder(folder_path)
