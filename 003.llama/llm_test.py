
from openai import OpenAI

# 로컬 LLM 서버 연결
client = OpenAI(
    base_url="http://localhost:9931/v1",
    api_key="lm-studio"
)

# 모델에 질문 보내기
response = client.chat.completions.create(
    model="local-model",
    messages=[
        {
            "role": "user",
            "content": "한국의 수도는 어디인가요? 한 문장으로 답하세요."
        }
    ],
    temperature=0.2,
    max_tokens=200,
    reasoning_effort="none"
)

# 답변 출력
print(response.choices[0].message.content)
