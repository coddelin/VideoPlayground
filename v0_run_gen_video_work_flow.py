
import os
import sys

from v_constants import OUT_MP3, OUT_MP4

# #AI语音识别音频生成字幕，不太准确
# os.system("python v3_srt_subtitle_gen.py")
if __name__ == '__main__':
    args = sys.argv
    #生成文章文案
    print("➡️ 生成文章文案")
    os.system("python v1_gen_paper.py")
    # 生成声音
    print("➡️ 生成声音")
    os.system("python v1_tts_gen.py")
    # #下载图片
    print("➡️ 下载图片")
    os.system("python v2_download_images.py")

    # #生成视频
    print("➡️ 生成视频")
    os.system("python v4_concat_image_to_video.py")
    # 合成视频
    print("➡️ 合成视频")
    os.system("python v5_muxer_video.py")
    # 查看视频信息
    print("➡️ 查看视频信息")
    os.system(f"ffprobe -hide_banner -i {OUT_MP4}")

    if len(args) > 0 and args[0] == "play-video":
        print("➡️ 播放视频")
        os.system(f"ffplay -loop 0  {OUT_MP4}")
    #运行上传视频脚本
    
    
    os.system("cd ../AutoUpload && python upload_dy_video.py \"-upload-gen-video\" \"随笔段子\" \"#随笔段子 #风景欣赏 #精美壁纸 #段子\"")
    # 清理工作区文件
    # if os.name == "nt":
    #     # windows
    #     os.system(
    #         f'powershell pwd && cd ../VideoPlayground && powershell Remove-Item "{OUT_MP3}", "out_zoompan.mp4"')
    #     os.system(
    #         'powershell pwd && cd ../VideoPlayground && powershell  Remove-Item "img","file_list.txt","img_file_list_file.txt" -Recurse')
    #     os.system(f"powershell pwd && cd ../VideoPlayground && powershell  Remove-Item {OUT_MP3} -Recurse")
    # else:
    #     os.system(f"rm -rf {OUT_MP3} out_zoompan.mp4 out_muxered.mp4")
    #     os.system(f"rm -rf {OUT_MP3}")
    #     os.system("rm -rf img file_list.txt img_file_list_file.txt")

# x 优化图片张数，根据音频时长决定下载多少张图，合成视频。暂定每张5秒钟，2分20秒的音频对应视频就要2*60+20=140s,140/5=28张图片
