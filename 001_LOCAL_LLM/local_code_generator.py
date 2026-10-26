from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1235/v1",
    api_key="lm-studio"
)

# LM Studio 서버에서 사용 가능한 모델 목록 확인
models = client.models.list()

for model in models.data:
    print(model.id)