#!/bin/bash
###
#  @Author: Diana Tang
#  @Date: 2025-02-18 10:18:11
# @LastEditors: Diana Tang
#  @Description: some description
 # @FilePath: /add-srt-compress-video/source/BatchModification.sh
### 
# 定义分辨率预设
get_scale() {
    case "$1" in
        "4k")
            echo "3840:2160"
            ;;
        "2k")
            echo "2560:1440"
            ;;
        "1080p")
            echo "1920:1080"
            ;;
        "720p")
            echo "1280:720"
            ;;
        "480p")
            echo "854:480"
            ;;
        *)
            echo "$1"
            ;;
    esac
}

# 定义压缩视频的函数
compress_video() {
    input_file="$1"
    output_file="$2"
    crf="${3:-23}"
    preset="${4:-medium}"
    scale="$(get_scale ${5:-1080p})"
    fps="${6:-30}"
    audio_bitrate="${7:-128k}"

    echo "正在处理: $input_file"
    echo "输出到: $output_file"
    echo "输出分辨率: $scale"
    
    ffmpeg -i "$input_file" \
        -c:v libx265 -preset $preset -crf $crf \
        -vf "scale=$scale,fps=$fps" \
        -c:a aac -b:a $audio_bitrate \
        -movflags +faststart \
        "$output_file"
}

# 批量处理文件夹的函数
batch_compress_videos() {
    input_dir="$1"
    output_dir="$2"
    crf="${3:-23}"
    preset="${4:-medium}"
    scale="${5:-1080p}"
    fps="${6:-30}"
    audio_bitrate="${7:-128k}"

    # 确保路径以 / 结尾
    input_dir="${input_dir%/}/"
    output_dir="${output_dir%/}/"

    # 确保输出目录存在
    mkdir -p "$output_dir"
    
     # 遍历每种可能的视频格式
    for ext in mp4 MP4 avi AVI mkv MKV mov MOV; do
        # 查找当前格式的文件
        if ls "${input_dir}"*."${ext}" >/dev/null 2>&1; then
            for input_file in "${input_dir}"*."${ext}"; do
                output_file="${output_dir}$(basename "${input_file%.*}").mp4"
                echo "处理文件: $input_file"
                compress_video "$input_file" "$output_file" "$crf" "$preset" "$scale" "$fps" "$audio_bitrate"
                ((total_files++))
            done
        fi
    done

}

# 显示使用说明
show_help() {
    echo "使用方法: $0 输入目录 输出目录 [CRF值] [编码预设] [分辨率] [帧率] [音频比特率]"
    echo ""
    echo "参数说明："
    echo "1. CRF值: 0-51，默认23（数值越小质量越好，文件越大）"
    echo "2. 编码预设: ultrafast, superfast, veryfast, faster, fast, medium(默认), slow, slower, veryslow"
    echo "3. 分辨率预设:"
    echo "   - 4k     (3840:2160)"
    echo "   - 2k     (2560:1440)"
    echo "   - 1080p  (1920:1080) - 默认"
    echo "   - 720p   (1280:720)"
    echo "   - 480p   (854:480)"
    echo "   - 也可直接指定，如: 1920:1080"
    echo "4. 帧率: 默认30"
    echo "5. 音频比特率: 默认128k"
    echo ""
    echo "示例:"
    echo "$0 ./videos ./output 23 medium 1080p 30 128k"
    echo "$0 /home/user/videos /home/user/compressed 28 fast 720p 24 96k"
}

# 检查参数
if [ "$#" -lt 2 ]; then
    show_help
    exit 1
fi

# 检查输入目录是否存在
if [ ! -d "$1" ]; then
    echo "错误：输入目录 '$1' 不存在"
    exit 1
fi

# 执行批量处理
batch_compress_videos "$@"

# 完成后显示信息
echo "所有视频处理完成！"
echo "压缩后的视频保存在: $2"