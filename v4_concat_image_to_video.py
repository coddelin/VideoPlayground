import asyncio
from asyncio.log import logger
import os
import random
import subprocess
import uuid
import json

from my_log import log


async def get_video_info(file_path):
    # 使用 FFmpeg 获取 video 文件信息
    cmd = f"ffprobe -v quiet -print_format json -show_format -show_streams {file_path}"
    stdout = await run_command(cmd)
    info = json.loads(stdout)
    mp4_info = {
        "duration": float(info.get("format", {}).get("duration", 0)),
        "bit_rate": info.get("format", {}).get("bit_rate"),
        "width": info.get("streams", [])[0].get("width"),
        "height": info.get("streams", [])[0].get("height"),
    }
    return mp4_info


def run_cmd(cmd):
    """执行命令并实时打印标准输出和标准错误"""
    try:
        log(f"run_cmd  {cmd}")

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
        )

        # 实时打印标准输出
        for stdout_line in iter(process.stdout.readline, ""):
            print(f"{stdout_line}")

        # 实时打印标准错误
        for stderr_line in iter(process.stderr.readline, ""):
            print(f"{stderr_line}")

        # 等待命令执行完成
        process.stdout.close()
        process.stderr.close()
        process.wait()

    except Exception as e:
        logger.error(f"An error occurred while running the command: {e}")


async def run_command(cmd: str):
    """执行命令并返回结果"""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    flag = '-filter_complex "'
    index = cmd.find(flag)
    rindex = index + len(flag)
    cmd_str = cmd[rindex:].replace(";", "; \\\n")
    log(f"run_command => [\n{cmd[0:rindex]} \\\n{cmd_str}\n]")
    stdout, stderr = await process.communicate()
    print(stdout.decode())
    if process.returncode != 0:
        raise Exception(f"Error executing command: {stderr}")
    return stdout.decode()  # 将字节流解码为字符串


def generate_uuid():
    val = "%s" % (uuid.uuid4())
    val = val.replace("-", "")
    return val


async def run_ffmpeg_cmd_without_gpu(
    tmp_dir, cmd, final_dir, final_name, need_copy=False
):
    uuid = generate_uuid()
    tmp_name = f"{uuid}_{final_name}"
    tmp_path = f"{tmp_dir}/{tmp_name}"
    tmp_path = f"{tmp_dir}/{final_name}"
    cmds = ["ffmpeg",   "-hwaccel cuda",  # 使用CUDA硬件加速
            cmd, f"-y {tmp_path}"]
    cmd_str = " ".join(cmds)

    os.system(cmd_str)
    # stdout = await run_command(cmd_str)
    # log(f"run_ffmpeg_cmd {stdout}")
    # if need_copy:
    #    log(f"copy_file {stdout}")

    return tmp_path


effect_duration = 1


async def concat_zoompan_video(
    images: list[str],
    video_animation_type,
    transition_name=None,
    transition_type=1,
    output_name="output_na.mp4",
    item_duration=10
):

    img_size = len(images)
    total_duration = img_size * item_duration
    fps = 30
    width = 1280
    height = 720
    zoom = 1.2
    zoomed_height = height * zoom
    zoomed_width = width * zoom
    total_frames = fps * item_duration
    total_hor_move = zoomed_width - width
    total_vir_move = zoomed_height - height
    frame_offset_y = total_vir_move / total_frames
    frame_offset_x = total_hor_move / total_frames

    item_frames = item_duration * fps
    if transition_name is not None:
        item_frames = (item_duration + 1) * fps

    print(f"垂直方向移动速度: {frame_offset_y}, 水平方向移动速度:{frame_offset_x}")
    max_width = int(width * 2.5)
    max_height = int(height * 2.5)
    up_zoompan = f"scale={max_width}*{max_height},setsar=1,zoompan=z='{zoom}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2+{frame_offset_y:.2f}*on':s={width}x{height}:d={item_frames}:fps={fps}"
    down_zoompan = f"scale={max_width}*{max_height},setsar=1,zoompan=z='{zoom}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2-{frame_offset_y:.2f}*on':s={width}x{height}:d={item_frames}:fps={fps}"
    left_zoompan = f"scale={max_width}*{max_height},setsar=1,zoompan=z='{zoom}':x='(iw-iw/zoom)/2+{frame_offset_x}*on':y='(ih-ih/zoom)/2':s={width}x{height}:d={item_frames}:fps={fps}"
    right_zoompan = f"scale={max_width}*{max_height},setsar=1,zoompan=z='{zoom}':x='(iw-iw/zoom)/2-{frame_offset_x}*on':y='(ih-ih/zoom)/2':s={width}x{height}:d={item_frames}:fps={fps}"

    complex = '"'

    command = []
    shuffled_images = images[:]
    random.shuffle(shuffled_images)
    for i in range(img_size):
        command.extend(["-i", f"{shuffled_images[i].strip()}"])

    for i in range(img_size):
        zoom_pan = up_zoompan
        if video_animation_type == 1:
            if i % 2 == 0:
                zoom_pan = up_zoompan
            else:
                zoom_pan = down_zoompan

        elif video_animation_type == 2:
            if i % 2 == 0:
                zoom_pan = left_zoompan
            else:
                zoom_pan = right_zoompan

        if transition_name is not None:
            zoom_pan += f",trim=duration={item_duration+1}"
        complex += f"[{i}:v]{zoom_pan}[v{i}];"

    if transition_name is not None:
        if transition_type == 1:
            complex += f"[v0][v1]xfade=transition={transition_name}:duration=1:offset={item_duration}[vv1];"
            for i in range(1, img_size - 1):
                complex += f"[vv{i}][v{i+1}]xfade=transition={transition_name}:duration=1:offset={(i+1)*item_duration}[vv{i+1}];"
            complex += f'[vv{img_size-1}]format=yuv420p[outv]"'
        else:
            # gl transition
            # 复制每个片段成两个流
            for i in range(0, img_size):
                complex += f"[v{i}]split[v{i}cp1][v{i}cp2];"
            # 为每个片段分割截取转场所需的片段和待连接片段
            for i in range(img_size):
                complex += f"[v{i}cp1]trim=0:{item_duration}[v{i}trim_head];"
                complex += f"[v{i}cp2]trim={item_duration}:{item_duration+effect_duration}[v{i}trim_tail];"
                complex += f"[v{i}trim_tail]setpts=PTS-STARTPTS[v{i}trans_tail];\n"
            # 为每个片段合成转场
            trans_count = img_size - 1
            for i in range(trans_count):
                complex += f"[v{i}trans_tail][v{i+1}trim_head]gltransition=duration={effect_duration}:source={transition_name}[v{i}trans_fragment];"
            # 连接截取的head与转场
            for i in range(img_size):
                if i == 0:
                    complex += f"[v{i}trim_head][v{i}trans_fragment]"
                else:
                    complex += f"[v{i}trans_fragment]"
                # 最后一个片段
                if i == img_size - 1:
                    complex += f'[v{i}trans_tail]concat=n={img_size+2},format=yuv420p[outv]"'
            pass
    else:
        for i in range(img_size):
            complex += f"[v{i}]"
        complex += f'concat=n={img_size}:v=1:a=0,format=yuv420p[outv]"'

    command.extend(
        [

            f"-filter_complex",
            complex,
            f"-t",
            f"{total_duration}",
            "-map",
            '[outv]',
            # "-c:v",
            # "libx264",
            
            "-c:v h264_nvenc",  # 使用NVIDIA硬件编码器
            # "-preset",
            # "ultrafast",
            "-threads",
            "0",
        ]
    )

    cmd = " ".join(command)

    out_dir = "."
    stdout = await run_ffmpeg_cmd_without_gpu(out_dir, cmd, "", f"{output_name}")
    log(f"图片合成视频 {stdout}")


if __name__ == "__main__":
    input_imgs = './img_file_list_file.txt'
    image_files = []
    with open(f'{input_imgs}', 'r', encoding='utf-8') as file:
        image_files = file.readlines()
    print(f'files: image_files: {image_files}')

    asyncio.run(concat_zoompan_video(
        image_files, 1, "fade", 1, item_duration=5,output_name="out_zoompan.mp4"))

    # asyncio.run(
    #     concat_zoompan_video(image_files,
    #         1, "crosswarp.glsl", 2, output_name="output_gltransition.mp4"
    #     )
    # )
