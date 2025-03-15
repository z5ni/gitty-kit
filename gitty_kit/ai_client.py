import os
from openai import OpenAI
from setup_manager import config_load
from message_generator import prepare_prompt
from utils.git import git_diff

# 설정 파일에서 값 가져오기
config = config_load()

client = OpenAI(
    api_key=config["api"]["key"],
)

model = config["api"]["model"]
language = config["language"]
style = config["format"]["style"]
max_length = config["format"]["max_length"]

# instructions: 모델의 행동을 결정하는 프롬프트
# input:  모델이 작업을 수행하기 위해 필요한 추가 데이터
response = client.responses.create(
    model=model,
    instructions=prepare_prompt(
        style=style,
        lang=language,
        max_length=max_length,
    ),
    input=git_diff(),
)

print(response.output_text)
