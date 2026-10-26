
from dotenv import load_dotenv
from google import genai
import os

# .env 파일 읽기
load_dotenv()

# API 키로 Gemini 연결
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# 질문하기
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=input("질문을 입력하세요: ")
)

# 답변 출력
print(response.text)