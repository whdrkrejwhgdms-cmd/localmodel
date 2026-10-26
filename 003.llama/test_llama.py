
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:9931/v1",
    api_key="lm-studio"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {
            "role": "user",
            "content": "한국의 수도는 어디인가요? 정답만 한 문장으로 답하세요."
        }
    ],
    reasoning_effort="none",
    temperature=0.1,
    max_tokens=100
)

print("답변:")
print(response.choices[0].message.content)

print("종료 이유:", response.choices[0].finish_reason)
