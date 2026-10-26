
import os
import fitz
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# ========================================
# 1. 로컬 LLM 서버 연결
# ========================================

client = OpenAI(
    base_url="http://localhost:9931/v1",
    api_key="lm-studio"
)

MODEL_NAME = "local-model"


# ========================================
# 2. 임베딩 모델 준비
# ========================================

print("임베딩 모델을 불러오는 중입니다...")

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-small"
)

print("임베딩 모델 준비 완료!")


# ========================================
# 3. PDF 파일 읽기
# ========================================

def read_pdf(pdf_path):
    pdf = fitz.open(pdf_path)

    documents = []

    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text("text").strip()

        if not text:
            continue

        # 페이지 내용을 일정한 길이로 나누기
        chunk_size = 900
        overlap = 150

        start = 0

        while start < len(text):
            chunk = text[start:start + chunk_size]

            if chunk.strip():
                documents.append({
                    "page": page_number,
                    "text": chunk
                })

            start += chunk_size - overlap

    pdf.close()

    return documents


# ========================================
# 4. PDF 내용의 임베딩 생성
# ========================================

def create_embeddings(documents):
    print("PDF 내용을 분석하고 검색 데이터를 생성합니다...")

    texts = [
        "passage: " + document["text"]
        for document in documents
    ]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.array(embeddings)


# ========================================
# 5. 질문과 관련된 PDF 내용 검색
# ========================================

def search_documents(question, documents, embeddings, top_k=6):
    query_embedding = embedding_model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )[0]

    # 임베딩 사이의 유사도 계산
    scores = np.dot(embeddings, query_embedding)

    # 유사도가 높은 순서로 정렬
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append(documents[index])

    return results


# ========================================
# 6. 검색된 PDF 내용을 바탕으로 답변 생성
# ========================================

def ask_llm(question, search_results):
    context = ""

    for item in search_results:
        context += (
            f"\n[PDF {item['page']}페이지]\n"
            f"{item['text']}\n"
        )

    system_prompt = """
당신은 PDF 문서를 전문적으로 분석하는 AI입니다.

반드시 제공된 PDF 발췌 내용을 근거로 답변하세요.

답변 작성 규칙:

1. 질문에 대한 답변을 먼저 명확하게 제시하세요.
2. 핵심 내용만 짧게 나열하지 말고 충분히 상세하게 설명하세요.
3. 중요한 개념, 원인, 결과, 특징을 구분하여 설명하세요.
4. 필요한 경우 번호 목록과 소제목을 사용하세요.
5. PDF에 구체적인 수치, 날짜, 사례가 있다면 포함하세요.
6. PDF에 코드나 절차가 있다면 가능한 한 단계별로 설명하세요.
7. 답변의 근거가 된 PDF 페이지 번호를 표시하세요.
8. PDF에 없는 내용을 사실인 것처럼 만들어 내지 마세요.
9. 질문에 대한 근거가 부족하면 부족하다고 명확히 알려주세요.
10. 불필요하게 같은 내용을 반복하지 마세요.

답변은 한국어로 작성하세요.
질문이 상세한 설명을 요구하면 충분한 분량으로 답변하세요.
"""

    user_prompt = f"""
다음은 질문과 관련하여 PDF에서 검색한 내용입니다.

================ PDF 내용 시작 ================

{context}

================ PDF 내용 끝 ==================

질문:
{question}

위 PDF 내용을 꼼꼼하게 검토하고, 근거와 세부 설명을 포함하여 답변하세요.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=3000,
        extra_body={
            "reasoning_effort": "none"
        }
    )

    return response.choices[0].message.content


# ========================================
# 7. 프로그램 실행
# ========================================

def main():
    print("=" * 50)
    print("PDF 문서 분석 프로그램")
    print("=" * 50)

    pdf_path = input("PDF 파일 경로를 입력하세요: ").strip().strip('"')

    if not os.path.exists(pdf_path):
        print("파일을 찾을 수 없습니다.")
        return

    if not pdf_path.lower().endswith(".pdf"):
        print("PDF 파일만 사용할 수 있습니다.")
        return

    # PDF 읽기
    documents = read_pdf(pdf_path)

    if not documents:
        print("PDF에서 텍스트를 추출하지 못했습니다.")
        print("스캔 이미지로만 구성된 PDF인지 확인하세요.")
        return

    print(f"\nPDF 분석 준비 완료: {len(documents)}개 문서 조각")

    # 검색용 임베딩 생성
    embeddings = create_embeddings(documents)

    print("\n분석 준비가 완료되었습니다.")
    print("질문을 입력하세요.")
    print("전체 요약을 원하면 '전체 요약'이라고 입력하세요.")
    print("종료하려면 'exit'를 입력하세요.")

    while True:
        question = input("\n질문: ").strip()

        if question.lower() == "exit":
            print("프로그램을 종료합니다.")
            break

        if not question:
            continue

        # 전체 요약 요청
        if question == "전체 요약":
            question = """
이 PDF 문서의 전체 내용을 체계적으로 요약하세요.

문서 전체를 한 번에 요약할 수 있도록
각 페이지의 핵심 내용을 순서대로 검토하고,
주요 주제, 핵심 주장, 중요한 세부 내용,
수치와 사례, 결론을 구분하여 설명하세요.

가능하면 목차 형태로 구성하고,
각 내용의 근거가 되는 페이지 번호를 표시하세요.
"""

        # 질문과 관련된 PDF 내용 검색
        search_results = search_documents(
            question,
            documents,
            embeddings,
            top_k=6
        )

        # 답변 생성
        answer = ask_llm(question, search_results)

        print("\n" + "=" * 50)
        print("분석 결과")
        print("=" * 50)
        print(answer)
        print("=" * 50)

        # 답변을 텍스트 파일로 저장
        output_path = os.path.splitext(pdf_path)[0] + "_분석결과.txt"

        with open(output_path, "a", encoding="utf-8") as file:
            file.write("\n" + "=" * 50 + "\n")
            file.write(f"질문: {question}\n\n")
            file.write(f"답변:\n{answer}\n")

        print(f"\n분석 결과 저장: {output_path}")


if __name__ == "__main__":
    main()
