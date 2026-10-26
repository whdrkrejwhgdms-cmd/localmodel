
import os
import fitz
import numpy as np

from openai import OpenAI
from sentence_transformers import SentenceTransformer


# 1. 로컬 LLM 서버 연결
client = OpenAI(
    base_url="http://localhost:9931/v1",
    api_key="lm-studio"
)

# 2. 한국어를 포함한 다국어 문서 검색 모델
embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-small"
)


# 3. PDF에서 텍스트 추출 및 문단 분할
def load_pdf(pdf_path):
    pdf = fitz.open(pdf_path)
    documents = []

    for page_number, page in enumerate(pdf, start=1):
        text = " ".join(page.get_text("text").split())

        if not text:
            continue

        chunk_size = 900
        overlap = 150
        start = 0

        while start < len(text):
            chunk = text[start:start + chunk_size]

            if chunk.strip():
                documents.append({
                    "text": chunk,
                    "page": page_number
                })

            start += chunk_size - overlap

    pdf.close()
    return documents


# 4. 문서의 검색용 벡터 생성
def create_embeddings(documents):
    texts = [
        "passage: " + doc["text"]
        for doc in documents
    ]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.asarray(embeddings)


# 5. 질문과 관련된 문단 검색
def search_documents(question, documents, embeddings):
    query_embedding = embedding_model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )[0]

    scores = embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:4]

    results = []

    for index in top_indices:
        results.append({
            "text": documents[index]["text"],
            "page": documents[index]["page"],
            "score": float(scores[index])
        })

    return results


# 6. 검색한 문서를 근거로 AI 답변 생성
def ask_llm(question, results, pdf_name):
    context = ""

    for result in results:
        context += (
            f"\n[출처: {pdf_name}, "
            f"{result['page']}페이지]\n"
            f"{result['text']}\n"
        )

    prompt = f"""
다음은 PDF 문서에서 검색한 내용입니다.

[참고 문서]
{context}

[질문]
{question}

[답변 규칙]
1. 참고 문서에 근거하여 답변하세요.
2. 문서에 없는 내용은 추측하지 마세요.
3. 답을 찾을 수 없으면 문서에서 확인할 수 없다고 하세요.
4. 관련 페이지 번호를 표시하세요.
5. 한국어로 명확하게 답변하세요.
"""

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 PDF 문서 분석 도우미입니다. "
                    "제공된 문서 내용을 근거로 답변하세요."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700,
        reasoning_effort="none"
    )

    return response.choices[0].message.content


# 7. 프로그램 실행
pdf_path = input("PDF 파일 경로를 입력하세요: ").strip().strip('"')

if not os.path.isfile(pdf_path):
    print("파일을 찾을 수 없습니다.")
    raise SystemExit

if not pdf_path.lower().endswith(".pdf"):
    print("PDF 파일을 지정해 주세요.")
    raise SystemExit

print("\nPDF 문서를 읽고 있습니다...")

documents = load_pdf(pdf_path)

if not documents:
    print("PDF에서 텍스트를 찾을 수 없습니다.")
    print("스캔 PDF라면 OCR 처리가 필요합니다.")
    raise SystemExit

print("검색 문단 수:", len(documents))

print("\n문서 검색용 벡터를 생성합니다.")
embeddings = create_embeddings(documents)

pdf_name = os.path.basename(pdf_path)

print("\nPDF 준비 완료!")
print("질문을 입력하세요. 종료하려면 exit를 입력하세요.")

while True:
    question = input("\n질문: ").strip()

    if question.lower() == "exit":
        print("프로그램을 종료합니다.")
        break

    if not question:
        continue

    results = search_documents(
        question,
        documents,
        embeddings
    )

    print("\n[검색된 페이지]")

    for result in results:
        print(
            f"- {pdf_name}, "
            f"{result['page']}페이지 "
            f"(유사도: {result['score']:.3f})"
        )

    print("\n[AI 답변]")

    answer = ask_llm(question, results, pdf_name)
    print(answer)
