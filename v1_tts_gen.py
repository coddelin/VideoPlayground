from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import sys

import edge_tts
import time_tools

out_dir = "."

if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def get_duration(input):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', input]
    cmd_str = " ".join(cmd)
    print(cmd_str)
    result = subprocess.run(cmd_str,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            shell=True
                            )
    time = float(result.stdout.strip())
    print(time)
    return time

@time_tools.timeCost
def gen_tts(text: str, out,voice= "zh-CN-YunjianNeural"):
    cmd = [
        "edge-tts",
        f"-t \"{text.strip()}\"",
        f"-v {voice}",
        f"--write-media {out}.mp3",
        f"--write-subtitles {out}.srt"
    ]
    cmd_str = " ".join(cmd)
    print(f"正在生成语音 {out}.mp3 ...")
    print(cmd_str)
    run_cmd(cmd_str)
@time_tools.timeCost    
def gen_tts_with_SentenceBoundary(text: str, out:str,voice= "zh-CN-YunjianNeural"):
    """生成按照句子的标点符号的srt"""
    communicate = edge_tts.Communicate(text, voice, Boundary="SentenceBoundary")
    submaker = edge_tts.SubMaker()
    stdout = sys.stdout
    stdout.write("gen_tts_with_SentenceBoundary...")
    audio_bytes = []
    with open(f"{out}.mp3","wb") as file:
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                audio_bytes.append(chunk["data"])
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)
    SRT_FILE=f"{out}.srt"
    with open(SRT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())
        
    stdout.write(f"audio file length: {len(audio_bytes)}")
    # stdout.write(submaker.get_srt())


@time_tools.timeCost
def run_cmd(cmd_str):
    return os.system(cmd_str)


def trim_silence_voice(input, output):
    cmd = (f"ffmpeg -hide_banner -i {input} -af silenceremove=start_periods=1:start_duration=0.1:start_threshold=-50dB:"
           + f"stop_periods=1:stop_duration=0.1:stop_threshold=-50dB -y {output}")
    result = os.system(cmd)
    print(result)


def start_trim_voice(lang):
    for i in range(size):
        file_mp3_name = f"{lang}{i+1}.mp3"
        file_in = os.path.join(out_dir, file_mp3_name)

        file_mp3_name_trim_out = f"{lang}{i+1}_out_trim.mp3"
        file_out = os.path.join(out_dir, file_mp3_name_trim_out)
        print(f"start_trim_voice file_in= {file_in}")
        print(f"start_trim_voice file_out= {file_out}")
        trim_silence_voice(file_in, file_out)

# 时间格式化函数


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"


def generate_srt_with_timestamps(lang):
    # 获取语音长度，生成字幕
    output_srt = "output.srt"
    with open("template_strings.txt", "r+", encoding="utf-8") as f:
        texts = f.readlines()
    size = len(texts)

    print("Generating SRT file...")

    start_duration = 0
    with open(output_srt, "w", encoding="utf-8") as srt_file:
        for i in range(size):
            file_mp3_name = f"{lang}{i+1}_out.mp3"
            file_out = os.path.join(out_dir, file_mp3_name)
            start = format_time(start_duration)
            start_duration += get_duration(file_out)
            end = format_time(start_duration)
            text = texts[i]
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{text}\n\n")

    print(f"SRT file saved to {output_srt} time={start_duration}")
    return start_duration

def generate_tts_mp3(lang):
    txt = []
    with open("template_strings.txt", "r+", encoding="utf-8") as f:
        while True:
            t = f.readline().strip()
            if t == "":
                break
            txt.append(t)
    size = len(txt)
    with ThreadPoolExecutor(max_workers=12) as pool:    
            # 生成语音
        _futures=[pool.submit(gen_tts,text=txt[i], out=os.path.join(out_dir, f"{lang}{i+1}_out")) for i in range(size)]
        for f in futures.as_completed(_futures):
            print(f.result())
    return size


def get_text_line_size():
    with open("template_strings.txt", "r+", encoding="utf-8") as f:
        texts = f.readlines()
    return len(texts)

def concat_mp3(lang):
    # 合成连接成一个 out.mp3
    file_list_path = f"file_list.txt"
    with open(file_list_path, "w", encoding="utf-8") as f:
        for i in range(size):
            file_mp3_name = f"{lang}{i+1}_out.mp3"
            file_out = f"{out_dir}/{file_mp3_name}"
            f.write(f"file '{file_out}'\n")
    
    # 使用文件列表进行合并
    cmd_str = f"ffmpeg -hide_banner -y -f concat -safe 0 -i {file_list_path} -c copy out.mp3"
    print(cmd_str)
    run_cmd(cmd_str)
    
if __name__ == '__main__':
    size = get_text_line_size()
    lang="zh"
    # generate_tts_mp3(lang)
    # # 开始时批处理音频时长
    #deprecated
    # # start_trim_voice(lang)
    # generate_srt_with_timestamps(lang)
    # concat_mp3(lang)
    content=[]
    with open("template_strings.txt", "r+", encoding="utf-8") as f:
        while True:
            t = f.readline().strip()
            if t == "":#empty string of EOF
                break
            content.append(t)
    content_str=" ".join(content)
    gen_tts_with_SentenceBoundary(content_str,"out_paper",voice="zh-CN-shaanxi-XiaoniNeural")
    # run_cmd("ffplay out_paper.mp3")
    
