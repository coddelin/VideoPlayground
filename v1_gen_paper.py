import json
import os
from run_local_ai import stream_api, sync_api
import v1_tts_gen


def load_chapter_prompt():
    with open("v_paper_prompt.json", "r", encoding="utf-8") as file:
        s = file.read()
        obj = json.loads(s)
        prompt = obj["prompt"]
        templateTitle = obj["templateTitle"]
        chapter = obj["chapter"]
    return prompt, chapter, templateTitle


if __name__ == '__main__':
    data = load_chapter_prompt()
    content = sync_api(data[0], data[1])
    with open("template_strings.txt", "w", encoding="utf-8") as f:
        f.write(content)
