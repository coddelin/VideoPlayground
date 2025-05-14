
import os


if __name__ == '__main__':
    def muxer_video(input_video, input_audio, srt, out_final_mp4):
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
            f"-map 0:v -map 1:a {out_final_mp4}"
        ]
        cmd_str = " ".join(cmd)
        print(f"\n{cmd_str}\n")
        result = os.system(cmd_str)
        print(result)
    import os
    out_dir="out_mp4"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    muxer_video("out_zoompan.mp4", "out.mp3", "output.srt",f"{out_dir}/out_muxered.mp4")
