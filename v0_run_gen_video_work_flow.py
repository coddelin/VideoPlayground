
import os

# #AI语音识别音频生成字幕，不太准确
# os.system("python v3_srt_subtitle_gen.py")
if __name__=='__main__':

    #生成声音
    print("➡️ 生成声音")
    os.system("python v1_tts_gen.py")
    # #下载图片
    print("➡️ 下载图片")
    os.system("python v2_download_images.py")

    # #生成视频
    print("➡️ 生成视频")
    os.system("python v4_concat_image_to_video.py")
    #合成视频
    print("➡️ 合成视频")
    os.system("python v5_muxer_video.py")
    #查看视频信息
    print("➡️ 查看视频信息")
    os.system("ffprobe -hide_banner -i out_muxered.mp4")
    # print("➡️ 播放视频")
    os.system("ffplay -loop 0  out_muxered.mp4")
    #清理工作区文件
    # os.system("rm -rf out.mp3 out_zoompan.mp4 out_muxered.mp4")
    os.system("rm -rf v_out_mp3")
    os.system("rm -rf img file_list.txt img_file_list.txt")
    
# x 优化图片张数，根据音频时长决定下载多少张图，合成视频。暂定每张5秒钟，2分20秒的音频对应视频就要2*60+20=140s,140/5=28张图片