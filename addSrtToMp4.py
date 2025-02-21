'''
Author: Diana Tang
Date: 2025-02-21 23:29:05
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/addSrtToMp4.py
'''
import os
import subprocess

# 设置文件夹路径
video_folder = "./videos"
output_folder = "./srt-files"

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的MP4文件
for filename in os.listdir(video_folder):
    if filename.endswith(".mp4"):
        video_path = os.path.join(video_folder, filename)
        srt_filename = os.path.splitext(filename)[0] + ".srt"
        srt_path = os.path.join(output_folder, srt_filename)

        # 提取音频（可选）
        audio_path = os.path.join(output_folder, "temp_audio.wav")
        subprocess.run(f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 16000 {audio_path}", shell=True)

        # 调用语音识别工具生成字幕（以Vosk为例）
        subprocess.run(f"vosk-transcriber -i {audio_path} -o {srt_path}", shell=True)

        # 删除临时音频文件
        os.remove(audio_path)

        print(f"Generated SRT for {filename}")