
import asyncio
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
import hashlib
import math
import os
import requests

from v1_tts_gen import get_duration


url = "https://bing.ee123.net/img/rand"
poop = ThreadPoolExecutor(max_workers=12, thread_name_prefix="download_image")
dir = os.path.join(os.path.dirname(__file__), "img")
names = []
if not os.path.exists(dir):
    os.makedirs(dir)


def get_images(i):
    print(f"request {i}")
    res: requests.Response = requests.get(url=url)
    print(res.headers)
    if res.status_code == 200:
        image_name = f"img/images{i}.jpg"
        #保存文件名
        # names.append(image_name)
        with open(image_name, "wb") as f:
            #保存图片二进制
            f.write(res.content)
    return i


def start_download(size):
    arry = [poop.submit(get_images, i) for i in range(size)]

    for f in futures.as_completed(arry):
        print(f"complete {f.result()}")
    print("all complete")


def calculate_md5(file_path):
    """计算文件的 MD5 哈希值"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

ITEM_IMAGE_SHOWING_DRATION=3.0
if __name__ == "__main__":
    time = get_duration("out.mp3")
    num = math.ceil(time/ITEM_IMAGE_SHOWING_DRATION)
    print(time, num)
    for i in range(num):
        image_name = f"img/images{i}.jpg"
        names.append(image_name)
    start_download(size=num)
    with open("img_file_list_file.txt", "w+", encoding="utf-8") as f:
        for n in names:
            f.write(f"{n}\n")
        print("saved")
