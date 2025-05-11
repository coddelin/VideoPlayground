import whisper

# 时间格式化函数
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

# 自动生成 SRT 文件
def generate_srt_with_timestamps(audio_file, transcript_file, output_srt):
    # 加载 Whisper 模型
    model = whisper.load_model("base",device="cuda")
    
    # 转录音频文件，获取时间戳
    print("Transcribing audio...")
    result = model.transcribe(audio_file, language="zh", task="transcribe")
    print(result)
    segments = result["segments"]

    # # 读取源文案
    # with open(transcript_file, "r", encoding="utf-8") as f:
    #     lines = f.readlines()

    # # 检查文案和转录段落数量是否一致
    # if len(lines) != len(segments):
    #     raise ValueError("文案句子数量与音频转录段落数量不匹配，请检查文案内容。")

    # 生成 SRT 文件
    print("Generating SRT file...")
    with open(output_srt, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"]
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{text}\n\n")

    print(f"SRT file saved to {output_srt}")

# 示例调用
if __name__ == "__main__":
    audio_file_path = "out.mp3"  # 替换为你的音频文件路径
    transcript_file_path = "template_strings.txt"  # 替换为你的文案文件路径
    output_srt_path = "output.srt"  # 输出的 SRT 文件路径

    generate_srt_with_timestamps(audio_file_path, transcript_file_path, output_srt_path)