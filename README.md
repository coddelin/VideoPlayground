# 1、TTS(Text to speech)
研究可行的TTS开源库
- Edge-tts 

    支持的语种很多，多国语言醒支持的蛮好。如果需要做面向国际化的应用还是不错的。

    [github](https://github.com/rany2/edge-tts) rany2/edge-tts
- Spark-TTS

    上海交通大学、香港科技大学、西北工业大学、南洋科技大学等大学间合作的开源项目，对中文支持很好，可以克隆挺多音色

    [github](https://github.com/SparkAudio/Spark-TTS) SparkAudio/Spark-TTS

    [docs pdf](https://arxiv.org/pdf/2503.01710)
- FishAudio/Fish Speech/TTS

    SOTA Open Source TTS

    - [github](https://github.com/fishaudio/fish-speech) fishaudio/fish-speech
    - [docs](https://speech.fish.audio/start_agent/)

- Huggingface/parler-tts

    Parler-TTS is a lightweight text-to-speech (TTS) model that can generate high-quality, natural sounding speech in the style of a given speaker (gender, pitch, speaking style, etc). 
- ChatTTS-ui

    一个简单的本地网页界面，在网页使用 ChatTTS 将文字合成为语音，支持中英文、数字混杂，并提供API接口.

    原 [ChatTTS](https://github.com/2noise/chattts) 项目. 0.96版起，源码部署必须先安装ffmpeg ,之前的音色文件csv和pt已不可用，请填写音色值重新生成.[获取音色](https://github.com/jianchang512/ChatTTS-ui/blob/main/?tab=readme-ov-file#%E9%9F%B3%E8%89%B2%E8%8E%B7%E5%8F%96)

- Bytedance/MegaTTS3

    🚀Lightweight and Efficient: The backbone of the TTS Diffusion Transformer has only 0.45B parameters.
    字节跳动的研究

    [github](https://github.com/bytedance/MegaTTS3)

    ![图片](https://raw.githubusercontent.com/bytedance/MegaTTS3/refs/heads/main/assets/fig/table_tts.png)
- ChatTTS_colab

    🚀 一键部署（含离线整合包）！基于 ChatTTS ，支持流式输出、音色抽卡、长音频生成和分角色朗读。简单易用，无需复杂安装。

    [github](https://github.com/6drf21e/ChatTTS_colab)

# 2、FFmpeg
视频编辑工具    