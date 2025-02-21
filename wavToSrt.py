'''
Author: Diana Tang
Date: 2025-02-21 23:57:21
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/wavToSrt.py
'''
import os
import speech_recognition as sr

def generate_srt_from_audio(audio_path, srt_path):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # 使用Google语音识别服务
        text = recognizer.recognize_google(audio, language="zh-CN")

        # 创建SRT文件
        with open(srt_path, "w", encoding="utf-8") as f:
            lines = text.split(". ")  # 按句号分割为行
            for i, line in enumerate(lines):
                start_time = i * 5  # 每段持续5秒
                end_time = start_time + 5
                f.write(f"{i+1}\n")
                f.write(f"{start_time // 60:02d}:{start_time % 60:02d},000 --> {end_time // 60:02d}:{end_time % 60:02d},000\n")
                f.write(f"{line.strip()}\n\n")
        print(f"SRT文件生成成功: {srt_path}")
    except Exception as e:
        print(f"生成SRT时出错: {e}")

def process_wav_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            audio_path = os.path.join(folder_path, filename)
            srt_path = audio_path.replace(".wav", ".srt")
            
            # 生成SRT文件
            generate_srt_from_audio(audio_path, srt_path)

# 输入文件夹路径
folder_path = "./videos"
process_wav_files_in_folder(folder_path)
