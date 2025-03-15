import os
from openai import OpenAI
from config import DEFAULT_CONFIG
from message_generator import prepare_prompt
from utils.git import git_diff


client = OpenAI(
    api_key=DEFAULT_CONFIG["api"]["key"],
)

# instructions: 모델의 행동을 결정하는 프롬프트
# input:  모델이 작업을 수행하기 위해 필요한 추가 데이터
response = client.responses.create(
    model=DEFAULT_CONFIG["api"]["model"],
    instructions=prepare_prompt(
        style="simple",
        lang="en",
    ),
    input=git_diff(),
)

print(response.output_text)
