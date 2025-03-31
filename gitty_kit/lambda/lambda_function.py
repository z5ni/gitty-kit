from openai import OpenAI
import configparser
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
config_path = os.path.join(BASE_DIR, "config.ini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 로컬 테스트 환경을 위한 설정
if not OPENAI_API_KEY and os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    OPENAI_API_KEY = config.get("API", "OPENAI_API_KEY")


# 고정된 모델 설정
OPENAI_MODEL = "gpt-4o-mini"

# 프롬프트 템플릿
PROMPT_TEMPLATE = {
    "conventional": """다음 Git 변경사항을 분석하고, Conventional Commits 형식으로 커밋 메시지를 작성해주세요:
        
    타입은 다음 중 하나를 사용하세요: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

    커밋 메시지 형식:
    <type>: <description>

    [body]

    [footer]

    간결하고 명확하게 작성해주세요.
    body의 경우에는 - 를 사용해 한 줄씩 입력해주세요.

    코드 블럭을 사용하지 않고 커밋 메시지 내용만 입력해주세요.
    """,
    "simple": """다음 Git 변경사항을 분석하고, 간결한 커밋 메시지를 작성해주세요:

    간결하고 명확하게 작성해주세요.

    코드 블럭을 사용하지 않고 커밋 메시지 내용만 입력해주세요.
    """,
}


def lambda_handler(event, context):
    try:
        if "body" in event:
            # Lambda URL로 받은 경우 event에 직접 body가 있음
            body = (
                json.loads(event["body"])
                if isinstance(event["body"], str)
                else event["body"]
            )
        else:
            body = event

        diff = body.get("diff")
        if not diff:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "diff 값이 필요합니다."}),
            }

        language = body.get("language", "ko")
        style = body.get("style", "conventional")
        max_length = body.get("max_length", 75)

        if language not in ["ko", "en"]:
            language = "ko"

        if style not in ["conventional", "simple"]:
            style = "conventional"

        if not isinstance(max_length, int):
            try:
                max_length = int(max_length)
            except (ValueError, TypeError):
                max_length = 75

        if max_length < 10 or max_length > 500:
            max_length = 75  # 범위를 벗어나면 기본값 사용

        # 미리 정의된 프롬프트 템플릿 사용
        prompt = PROMPT_TEMPLATE[style]

        # 언어 지정 및 최대 길이 제한 추가
        prompt += f"\n\n사용 언어: {language}"
        prompt += f"\n\n커밋 제목은 {max_length}자 이내로 작성해주세요."

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=prompt,
            input=diff,
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": response.output_text}, ensure_ascii=False),
        }

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": f"메시지 생성 중 오류가 발생했습니다: {str(e)}"}
            ),
        }
