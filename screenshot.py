#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

# 获取脚本所在目录
path = sys.path[0]

# 支持的视频格式（修复关键字冲突，统一格式）
VIDEO_TYPES = ['.mp4', '.avi', '.wmv', '.mkv', '.flv',
                '.ts', '.mov', '.m4v', '.qt', '.MP4', '.MOV', '.MKV']

def check_video_ext(filename):
    """优化：判断文件是否为支持的视频格式"""
    return any(filename.endswith(ext) for ext in VIDEO_TYPES)

def make_thumb():
    # 遍历目录
    for dirpath, _, filenames in os.walk(path):
        # 跳过包含 dfdf 的文件夹
        if "dfdf" in dirpath:
            continue
            
        for name in filenames:
            if check_video_ext(name):
                try:
                    videopath = os.path.join(dirpath, name)
                    videoname = os.path.splitext(name)[0]
                    output_base = os.path.join(dirpath, videoname)
                    final_output = f"{output_base}.jpg"
                    
                    # 已存在缩略图则跳过
                    if os.path.exists(final_output):
                        continue

                    # 修复：with语句自动释放视频资源，避免文件占用
                    with VideoFileClip(videopath) as clip:
                        width = clip.w
                        height = clip.h
                        duration = clip.duration

                    # 极短视频跳过
                    if duration < 1:
                        print(f"短视频跳过: {duration}s -> {final_output}")
                        continue

                    # ==================== 横屏视频处理 ====================
                    if width > height:
                        # 自动计算截图数量和行列
                        if duration > 3600:
                            row, line = 3, 3
                        elif duration < 10:
                            row, line = 1, 1
                        else:
                            row, line = 2, 2
                        num = row * line
                        interval = max(1, int(duration / num))  # 避免间隔为0
                        canvas_w, canvas_h = 1280 * line, 720 * row
                        img_w, img_h = 1280, 720

                    # ==================== 竖屏视频处理 ====================
                    else:
                        if duration > 120:
                            row, line = 2, 5
                        else:
                            row, line = 1, 3
                        num = row * line
                        interval = max(1, int(duration / num) + 1)
                        canvas_w, canvas_h = 720 * line, 1280 * row
                        img_w, img_h = 720, 1280

                    # 生成单帧截图（核心修复：FFmpeg参数添加MJPEG兼容配置）
                    now_time = 1
                    temp_imgs = []
                    for i in range(row):
                        for j in range(line):
                            temp_img = f"{output_base}_img_{i}_{j}.jpg"
                            temp_imgs.append(temp_img)

                            # ✅ 修复FFmpeg命令：解决编码器报错 + 路径引号 + 格式兼容
                            ffmpeg_cmd = (
                                f'ffmpeg -y -ss {now_time} -i "{videopath}" '
                                f'-vf "scale={img_w}:{img_h}:force_original_aspect_ratio=decrease,pad={img_w}:{img_h}:(ow-iw)/2:(oh-ih)/2" '
                                f'-frames:v 1 -strict -2 -pix_fmt yuvj420p -q:v 3 "{temp_img}"'
                            )
                            os.system(ffmpeg_cmd)
                            now_time += interval

                    # 拼接图片
                    to_image = Image.new('RGB', (canvas_w, canvas_h))
                    for i in range(row):
                        for j in range(line):
                            temp_img = f"{output_base}_img_{i}_{j}.jpg"
                            if os.path.exists(temp_img):
                                with Image.open(temp_img) as img:
                                    to_image.paste(img, (j * img_w, i * img_h))

                    # 保存最终缩略图
                    to_image.save(final_output, quality=95)
                    print(f"生成成功: {final_output} | 时长:{duration}s 行列:{row}x{line}")

                    # 删除临时截图
                    for img in temp_imgs:
                        if os.path.exists(img):
                            os.remove(img)

                except Exception as e:
                    print(f"处理失败 {videopath}: {str(e)}")

# 修复：只执行一次函数（原脚本重复执行12次，严重bug）
if __name__ == "__main__":
    make_thumb()
