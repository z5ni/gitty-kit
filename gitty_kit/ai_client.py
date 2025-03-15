import os
from openai import OpenAI
from setup_manager import config_load
from message_generator import prepare_prompt
from utils.git import git_diff


def ai_client_init(config):
    client = OpenAI(api_key=config["api"]["key"])
    return client


def generate_commit_message():
    """
    openai API를 이용해 Git 변경사항에 대한 커밋 메시지 생성
    """

    config = config_load()
    diff_text = git_diff()

    if not diff_text:
        return "변경사항이 없습니다."

    client = ai_client_init(config)

    model = config["api"]["model"]
    language = config["language"]
    style = config["format"]["style"]
    max_length = config["format"]["max_length"]

    try:
        # instructions: 모델의 행동을 결정하는 프롬프트
        # input:  모델이 작업을 수행하기 위해 필요한 추가 데이터
        response = client.responses.create(
            model=model,
            instructions=prepare_prompt(
                style=style,
                lang=language,
                max_length=max_length,
            ),
            input=diff_text,
        )
        return response.output_text
    except Exception as e:
        return f"커밋 메시지 생성 중 오류가 발생했습니다: {str(e)}"
