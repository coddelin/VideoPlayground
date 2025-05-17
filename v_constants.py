import os
from v1_tts_gen import run_cmd


OUT_MP3 = "out_paper.mp3"
OUT_SRT = "out_paper.SRT"
OUT_MUXER_MP4 = "out_muxered_paper.mp4"
OUT_DIR = "out_mp4"
OUT_MP4 = f"{OUT_DIR}/output.mp4"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
    
XFADE = [
    "fade",  # 淡入淡出（默认）
    "wipeleft",  # 从右向左擦除
    "wiperight",  # 从左向右擦除
    "wipeup",  # 从下向上擦除
    "wipedown",  # 从上向下擦除
    "slideleft",  # 从右滑动到左
    "slideright",  # 从左滑动到右
    "slideup",  # 从下滑动到上
    "slidedown",  # 从上滑动到下
    "circlecrop",  # 圆形遮罩展开
    "rectcrop",  # 方形遮罩展开
    "distance",  # 像素距离放大式溶解
    "fadeblack",  # 淡出到黑再淡入
    "fadewhite",  # 淡出到白再淡入
    "radial",  # 放射状扩展溶解
    "smoothleft",  # 平滑左滑动
    "smoothright",  # 平滑右滑动
    "smoothup",  # 平滑上滑动
    "smoothdown",  # 平滑下滑动
    "circleopen",  # 圆形从中心打开
    "circleclose",  # 圆形从边缘收缩
    "vertopen",  # 垂直从中间分开
    "vertclose",  # 垂直向中间合并
    "horzopen",  # 水平从中间分开
    "horzclose",  # 水平向中间合并
    "dissolve",  # 像素随机淡出淡入
    "pixelize",  # 马赛克再清晰化
    "diagtl",  # 左上到右下对角线展开
    "diagtr",  # 右上到左下对角线展开
    "diagbl",  # 左下到右上对角线展开
    "diagbr",  # 右下到左上对角线展开
    "hlslice",  # 水平方向从多段展开
    "hrslice",  # 水平方向从多段合并
    "vuslice",  # 垂直方向从多段展开
    "vdslice",  # 垂直方向从多段合并
    "hblur",  # 水平模糊转场
    # "fadegrayscale",  # 灰度淡入淡出 当前版本ffmpeg没有实现
    # "rectangles",  # 随机矩形区域转场 当前版本ffmpeg没有实现
    "squeezeh",  # 水平挤压
    "squeezev",  # 垂直挤压
]

# 生成一个测试xfade的ffmpeg指令


def generate_ffmpeg_xfade_command(input_video, output_video, transition, duration=1, start_time=0):
    """
    Generate an ffmpeg command to test a specific xfade transition.

    :param input_video: Path to the input video file.
    :param output_video: Path to the output video file.
    :param transition: The xfade transition effect to use.
    :param duration: Duration of the transition in seconds (default is 1).
    :param start_time: Start time of the transition in seconds (default is 0).
    :return: A string containing the ffmpeg command.
    """
    command = (
        f"ffmpeg -hide_banner -y -i {input_video} -filter_complex "
        f"\"[0:v]trim=0:{start_time},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v0];"
        f"[0:v]trim={start_time},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v1];"
        f"[v0][v1]xfade=transition={transition}:duration={duration}:offset={start_time}[v]\" "
        f"-map \"[v]\" -map 0:a? {output_video}"
    )
    return command


def test_xfade_implements():
    # Example usage
    input_video = "v1.mp4"
    output_video = "output.mp4"
    duration = 1
    start_time = 2

    for i in range(36, len(xfade)):
        transition = xfade[i]
        print(f"\n {i} {transition}")
        ffmpeg_command = generate_ffmpeg_xfade_command(
            input_video, output_video, transition, duration, start_time)
        print(ffmpeg_command)
        if run_cmd(ffmpeg_command) != 0:
            print(f"\n error {i} {transition}")
            break


if __name__ == '__main__':
    test_xfade_implements()
