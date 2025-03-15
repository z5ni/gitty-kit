import os
from openai import OpenAI
from config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# instructions: 모델에게 어떤 작업을 수행해야 하는지에 대한 지침 -> prompt
# input: 작업을 수행하는 데 필요한 구체적인 데이터
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="너는 코딩 선생님이야.",
    input="openai 파이썬 라이브러리에서 client.responses.create의 인자로 오는 instructions과 input의 차이가 뭐야? instructions는 프롬프트 입력하는거라고 봐도 되는거야?",
)

print(response.output_text)
