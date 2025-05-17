
import os

from my_log import log
from v1_gen_paper import load_chapter_prompt
from v1_tts_gen import get_duration
from v_constants import OUT_MP3, OUT_MP4, OUT_MUXER_MP4, OUT_SRT


def add_title_watermark_txt(
    input="input.mp4",
    output="output.mp4",
    fontsize=60,
    fontcolor="yellow",
    text="@爵醒影视",
):
    """
    添加水印到视频
    :param input: 输入视频文件路径
    :param output: 输出视频文件路径
    :param duration1: 水印持续时间1
    :param duration2: 水印持续时间2
    :param fontsize: 字体大小
    :param fontcolor: 字体颜色
    :param text: 水印文本
    :param gap_x: 水印横向间距
    :param gap_y: 水印纵向间距
    :return: 运行结果
    """
    # 修改时间
    # duration1 = f"0:3"
    # tital=get_duration(input)
    # duration2 = f"3:{tital}"
    log("Adding watermark to video...")
    # 使用ffmpeg添加水印，水印隔一段时间出现在不同位置
    # 合并为一条指令，前半段视频水印左上角，后半段水印在右下角
    # fontfile='simhei.ttf'
    # 水印持续时间
    # :enable='between(t,0,4)'
    cmd = (
        f'ffmpeg -hide_banner'
        + " -hwaccel cuda "  # 使用CUDA硬件加速
        + f'-y -i {input} -filter_complex "'
        + f"[0:v]drawtext=fontfile='C\\:/Windows/Fonts/simhei.ttf':fontsize={fontsize}:fontcolor={fontcolor}:text='{text}':x='(w-text_w)/2':y='(h-text_h)/2-10':enable='between(t,0,4)'"
        + f'" -map 0:a -c:v h264_nvenc -preset fast -rc vbr  -c:a copy {output}'
        # + f'" -map [v1out] -map 0:a -c:v libx264 -c:a aac {output}'
    )
    # 方式一 单一视频流
    # ffmpeg -hide_banner -y -i out_muxered_paper.mp4 -filter_complex "[0:v]drawtext=fontfile='C\:/Windows/Fonts/simhei.ttf':fontsize=60:fontcolor=yellow:text='《 水浒传》--平妖感怀':x='w/2-text_w/2':y='h/2-text_h/2-10':enable='between(t,0,4)'[v1out];" -map [v1out] -map 0:a -c:v libx264 -c:a aac output.mp4
    # 方式二 分割成两个视频流处理
    # ffmpeg -hide_banner -y -i out_muxered_paper.mp4 -filter_complex "[0:v]split=2[v1][v2];[v1]trim=0:3,setpts=PTS-STARTPTS,drawtext=fontfile='C\:/Windows/Fonts/simhei.ttf':fontsize=60:fontcolor=yellow:text='《水浒传》--平妖感怀':x='w/2-text_w/2':y='h/2-text_h/2-10'[v1out];[v2]trim=3:89.928,setpts=PTS-STARTPTS[v2out];[v1out][v2out]concat=n=2:v=1:a=0[outv]" -map [outv] -map 0:a -c:a aac output.mp4
    log(f"Running command: \n{cmd}\n")
    code = os.system(cmd)
    log(f"run cmd result code: {code}")
    return code


if __name__ == '__main__':
    def muxer_video(input_video, input_audio, srt, out_final_mp4, Fontname="Noto Serif SC", FontSize=18, PrimaryColour="&H64F1F3"):
        cmd = [
            "ffmpeg -y -hide_banner",
            "-hwaccel cuda",  # 使用CUDA硬件加速
            f"-i {input_video}",
            f"-i {input_audio}",
            f"-vf \"subtitles={srt}:force_style='Fontname={Fontname},FontSize={FontSize},PrimaryColour={PrimaryColour}'\"",
            "-c:v h264_nvenc",  # 使用NVIDIA硬件编码器
            # "-c:v libx264",
            "-preset fast",
            "-profile:v high",
            "-shortest",
            f"-map 0:v -map 1:a {out_final_mp4}"
        ]
        cmd_str = " ".join(cmd)
        print(f"\n{cmd_str}\n")
        result = os.system(cmd_str)
        print(result)
    import os
    # out_dir="out_mp4"
    # if not os.path.exists(out_dir):
    #     os.makedirs(out_dir)
    # muxer_video("out_zoompan.mp4", OUT_MP3, OUT_SRT,OUT_MP4)
    data = load_chapter_prompt()
    add_title_watermark_txt(OUT_MUXER_MP4,output=OUT_MP4, text=f"{data[2]}{data[1]}")
