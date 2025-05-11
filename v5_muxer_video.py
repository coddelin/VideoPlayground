
import os


if __name__ == '__main__':
    def muxer_video(input_video, input_audio, srt):
        cmd = [
            "ffmpeg -y -hide_banner",
            "-hwaccel cuda",  # 使用CUDA硬件加速
            f"-i {input_video}",
            f"-i {input_audio}",
            f"-vf subtitles={srt}",
            "-c:v h264_nvenc",  # 使用NVIDIA硬件编码器
            "-preset fast",
            "-profile:v high",
            "-shortest",
            "-map 0:v -map 1:a out_muxered.mp4"
        ]
        cmd_str = " ".join(cmd)
        print(f"\n{cmd_str}\n")
        result = os.system(cmd_str)
        print(result)
    muxer_video("output_na.mp4", "out.mp3", "output.srt")
