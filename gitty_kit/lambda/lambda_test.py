import configparser
import json
import os
from pathlib import Path

import requests
from lambda_function import lambda_handler

BASE_DIR = Path(__file__).resolve().parent.parent.parent
config_path = os.path.join(BASE_DIR, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)
LAMBDA_URL = config.get("API", "LAMBDA_URL")


def test_lambda_function():
    """
    Lambda 함수를 로컬에서 테스트하는 함수
    """

    # Git diff 샘플
    sample_diff = """diff --git a/example.py b/example.py
index 1234567..abcdefg 100644
--- a/example.py
+++ b/example.py
@@ -10,7 +10,7 @@ def hello_world():
     print("Hello, World!")
 
 def calculate_sum(a, b):
-    return a + b
+    return a + b + 0  # 불필요한 연산 추가
 
 def main():
     hello_world()
"""

    # Lambda 함수에 전달할 이벤트 생성
    event = {
        "body": json.dumps(
            {
                "diff": sample_diff,
                "language": "ko",
                "style": "simple",
                "max_length": 50,
            }
        )
    }

    # Lambda 함수 호출
    response = lambda_handler(event, None)

    # 응답 출력
    print("Lambda 함수 응답:")
    print(response)


def test_lambda_url():
    """
    배포된 Lambda URL을 테스트하는 함수
    """
    # Lambda URL 주소 TODO: lambda url 보안 강화 후 공개
    lambda_url = LAMBDA_URL

    # Git diff 샘플 (테스트용)
    sample_diff = """diff --git a/example.py b/example.py
index 1234567..abcdefg 100644
--- a/example.py
+++ b/example.py
@@ -10,7 +10,7 @@ def hello_world():
     print("Hello, World!")
 
 def calculate_sum(a, b):
-    return a + b
+    return a + b + 0  # 불필요한 연산 추가
 
 def main():
     hello_world()
"""

    # 테스트 케이스
    test_cases = [
        # 한국어, conventional
        {
            "diff": sample_diff,
            "language": "ko",
            "style": "conventional",
            "max_length": 75,
        },
        # 영어, simple 스타일
        {"diff": sample_diff, "language": "en", "style": "simple", "max_length": 50},
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\n===== 테스트 케이스 {i+1} =====")
        print(f"요청 파라미터: {json.dumps(test_case, ensure_ascii=False, indent=2)}")

        try:
            # Lambda URL에 POST 요청 보내기
            response = requests.post(
                lambda_url, json=test_case, headers={"Content-Type": "application/json"}
            )

            # 응답 상태 코드 확인
            print(f"응답 상태 코드: {response.status_code}")

            # 응답 내용 출력
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    print(
                        f"응답 내용: {json.dumps(response_json, ensure_ascii=False, indent=2)}"
                    )
                except json.JSONDecodeError:
                    print(f"JSON이 아닌 응답 내용: {response.text}")
            else:
                print(f"오류 응답: {response.text}")

        except Exception as e:
            print(f"요청 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    test_lambda_url()
