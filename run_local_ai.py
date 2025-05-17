import json
import os
import time
import requests

from time_tools import timeCost
data=""
def stream_api(prompt="帮我翻译一下markdow文件成中文,注意front matter字段名称不要翻译",data_str: str = data,model="deepseek-r1:8B",callback=None):
    """使用流式API"""
    # 1. 创建一个请求，设置请求方法、URL和请求体
    # 2. 使用requests库发送请求，并获取响应流
    # 3. 遍历响应流，逐块读取数据并处理
    # 4. 如果接收到的块数据为空，则退出循环

    # 发送POST请求，设置流式传输
    # 注意：这里的URL需要替换为实际的API地址
    response = requests.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        data=None,
        json={
            "model": model,
            "prompt": f"{prompt}：{data_str}",
            "stream": True,
        },
        stream=True,
    )
    if response.status_code==200:
        print("请求失败，状态码：", response.status_code)
        return None
    response.iter_content(chunk_size=None)
    for chunk in response:
        if chunk:
            response = chunk.decode("utf-8")
            dict_str: dict = json.loads(response)
            if dict_str.get("done") == True:
                break
            # time.sleep(0.1)
            print(dict_str.get("response"), end="", flush=True)
            if callback:
                callback(dict_str.get("response"))


@timeCost
def sync_api(prompt="帮我翻译一下markdow文件成中文,注意front matter字段名称不要翻译",data_str: str = data,model="deepseek-r1:8B"):
    """使用同步API"""
    # 1. 创建一个请求，设置请求方法、URL和请求体
    # 2. 使用requests库发送请求，并获取响应
    # 3. 处理响应数据

    # 发送POST请求，获取响应
    response = requests.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        data=None,
        json={
            "model": model,
            "prompt": f"{prompt}：{data_str}",
            "stream": False,
        },
    )
    print("请求返回的数据：", response)
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        return None
    # 处理响应数据
    dict_str: dict = json.loads(response.text)
    result: str = dict_str.get("response")
    if result is None:
        print("没有返回结果")
        return None
    index = result.find("</think>") + len("</think>")
    string: str = result[index:].replace("\n"," ").replace("##","").replace("#","").replace("**","")
    response = string.strip()
    print(response)
    # with open("test.md", "w", encoding="utf-8") as f:
    #     f.write(string.strip())
    return response

@timeCost
def translate(model):
    """翻译函数"""
    i18n = "i18n/en/docusaurus-plugin-content-docs/current"
    count = 0
    for root, dirs, files in os.walk(f"../rhino-doc/{i18n}/"):
        for file in files:
            if file.endswith(".md"):
                count+=1
                path = os.path.join(root, file)
                print(f"正在翻译文件：{path}")
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
                response = sync_api(data,model=model)
                if response is None:
                    print("翻译失败")
                    continue
                with open(path.replace(i18n, "docs"), "w", encoding="utf-8") as f:
                    f.write(response)
            # break
        # break
    print(f"翻译完成，共翻译{count}个文件")
if __name__ == "__main__":
    #解析命令行参数，获取大模型名称
    import argparse
    parser = argparse.ArgumentParser(description="翻译markdown文件")
    parser.add_argument(
        "-m", "--model", type=str, default="deepseek-r1:8B", help="大模型名称"
    )
    args = parser.parse_args()
    model = args.model
    print(f"大模型名称：{model}")
    # stream_api(model=model) 
    
    # translate(model)
