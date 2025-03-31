import json
import os


from lambda_function import lambda_handler


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


if __name__ == "__main__":
    test_lambda_function()
