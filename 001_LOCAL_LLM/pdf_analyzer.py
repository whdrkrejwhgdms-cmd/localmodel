import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader
from openai import OpenAI

# 1. 파일 선택 창 열기
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="분석할 PDF 파일을 선택하세요",
    filetypes=[("PDF 파일", "*.pdf")]
)

if not file_path:
    print("선택된 파일이 없습니다.")
    exit()

# 2. PDF 텍스트 추출
print(f"[{os.path.basename(file_path)}] PDF 읽는 중...")
reader = PdfReader(file_path)
total_pages = len(reader.pages)
print(f"총 페이지 수: {total_pages}페이지\n")

# 3. LM Studio 로컬 API 연결
client = OpenAI(base_url="http://localhost:1235/v1", api_key="lm-studio")

# Qwen 모델 ID 자동 검색
models = client.models.list()
model_id = None
for model in models.data:
    if "qwen" in model.id.lower():
        model_id = model.id
        break

if model_id is None:
    model_id = models.data[0].id  # 없으면 첫 번째 모델 사용

print(f"사용 중인 모델: {model_id}\n")

# 4. 페이지 구간별(5페이지씩) 텍스트 추출 및 중간 요약 진행
chunk_size = 5
section_summaries = []

for i in range(0, total_pages, chunk_size):
    end_page = min(i + chunk_size, total_pages)
    current_chunk_text = ""
    
    for p in range(i, end_page):
        current_chunk_text += f"\n--- Page {p+1} ---\n" + reader.pages[p].extract_text()

    print(f">> [진행 중] {i+1} ~ {end_page}페이지 분석 및 구간 요약 중...")

    # 로컬 모델에 구간 요약 요청
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "다음 문서는 PDF의 일부분입니다. 핵심 내용을 한국어로 간결하게 요약해 주세요."},
            {"role": "user", "content": current_chunk_text}
        ],
        temperature=0.2,
        stream=True  # 실시간 출력을 위해 스트리밍 활성화
    )

    # 작업 중인 내용의 일부(스트리밍)를 화면에 실시간 출력
    print("   [구간 요약 출력]: ", end="", flush=True)
    chunk_summary = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            chunk_summary += content
    print("\n" + "-" * 40)
    
    section_summaries.append(f"[{i+1}~{end_page}페이지 요약]\n{chunk_summary}\n")

# 5. 전체 구간 요약들을 모아서 최종 요약 생성
print("\n>> [진행 중] 모든 구간 요약을 바탕으로 최종 전체 요약 생성 중...")

combined_text = "\n".join(section_summaries)
final_response = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "system", "content": "아래는 긴 PDF 문서의 구간별 요약본들입니다. 이를 바탕으로 전체 문서의 핵심 내용을 종합하여 깔끔하게 최종 요약해 주세요."},
        {"role": "user", "content": combined_text}
    ],
    temperature=0.2,
    stream=True
)

print("   [최종 요약 출력]: ", end="", flush=True)
final_output = ""
for chunk in final_response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
        final_output += content
print("\n" + "=" * 40)

# 6. 결과 파일로 저장
output_path = file_path.rsplit(".", 1)[0] + "_분석결과.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"\n분석 완료! 결과가 저장되었습니다: {output_path}")