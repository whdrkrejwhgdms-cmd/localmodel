# Windows에서 llama.cpp 로컬 서버와 PDF RAG 만들기

이 문서는 **Windows + VS Code + Python** 환경에서 `llama.cpp`로 로컬
언어 모델 서버를 실행하고, PDF 문서를 검색해 질문에 답하는 간단한 RAG
시스템을 만드는 과정을 정리합니다.

> 목표: PDF를 선택하고 질문을 입력하면, PDF에서 관련 내용을 찾아 로컬
> LLM에 전달하고 답변을 출력합니다. 모델 파일과 개인 PDF는 GitHub
> 저장소에 올리지 않습니다.

## 목차

1.  동작 구조 이해하기
2.  준비물 및 프로젝트 폴더 만들기
3.  llama.cpp 설치 확인
4.  모델 다운로드 및 서버 실행
5.  Python 가상환경과 라이브러리 설치
6.  로컬 서버 연결 테스트
7.  PDF RAG 프로그램 작성
8.  실행 및 테스트
9.  GitHub 공개 준비
10. 문제 해결

---

## 1. 동작 구조 이해하기

RAG는 **검색 증강 생성(Retrieval-Augmented Generation)** 방식입니다.

1.  PDF에서 텍스트를 추출합니다.
2.  텍스트를 작은 조각(chunk)으로 나눕니다.
3.  임베딩 모델이 각 조각을 숫자 벡터로 변환합니다.
4.  질문도 벡터로 변환하고, 의미가 가까운 조각을 검색합니다.
5.  검색된 조각과 질문을 로컬 LLM에 전달합니다.
6.  LLM이 문서 내용을 바탕으로 답변합니다.

이 예제에서 사용하는 구성은 다음과 같습니다.

---

구성 요소 역할

---

llama.cpp 로컬 언어 모델을 실행하는 엔진

Qwen GGUF 모델 질문에 답변을 생성하는 LLM

llama.cpp 서버 Python 프로그램이 모델에 요청할 수
있게 API 제공

PyMuPDF (`fitz`) PDF에서 텍스트 추출

`intfloat/multilingual-e5-small` 한국어를 포함한 텍스트 임베딩 생성

NumPy 벡터 유사도 계산

OpenAI Python 라이브러리 OpenAI 호환 로컬 API에 요청 전송

---

임베딩 모델과 LLM은 서로 다른 역할을 합니다. 임베딩 모델이 답변을
생성하는 것은 아니며, 관련 문서 조각을 찾는 데 사용됩니다.

## 2. 준비물 및 프로젝트 폴더 만들기

- Windows
- Python 3.13
- VS Code
- llama.cpp
- GGUF 형식의 LLM 모델
- 인터넷 연결(설치 및 모델 최초 다운로드 시)

예시 프로젝트 폴더:

```text
C:\\local-rag
├── .gitignore
├── README.md
├── requirements.txt
├── pdf_rag.py
└── documents/
    └── 여기에_테스트용_PDF_넣기.pdf
```

`documents/` 폴더에는 테스트할 PDF를 넣을 수 있습니다. 공개 저장소에
PDF를 올릴 필요는 없습니다.

PowerShell에서 폴더를 만들고 VS Code로 엽니다.

```powershell
mkdir C:\local-rag
cd C:\local-rag
code .
```

`code .` 명령을 사용할 수 없다면 VS Code에서 **파일 → 폴더 열기**로
`C:\local-rag`를 선택합니다.

## 3. llama.cpp 설치 확인

이미 설치했다면 이 단계를 건너뛰고 버전을 확인합니다.

```powershell
llama --version
```

일부 설치 방식에서는 실행 명령이 `llama-cli` 또는 `llama-server`로
제공될 수 있습니다. 설치 방식과 배포 버전에 따라 명령 이름이 다를 수
있으므로 다음도 확인합니다.

```powershell
llama-server --version
```

### 설치가 안 되어 있다면

1.  공식 저장소의 Windows용 설치 안내 또는 릴리스 페이지를 엽니다.
    - GitHub: https://github.com/ggml-org/llama.cpp
    - Releases: https://github.com/ggml-org/llama.cpp/releases
2.  Windows와 PC의 CPU/GPU 환경에 맞는 배포 파일을 선택합니다.
3.  압축 파일을 내려받았다면 원하는 폴더에 압축을 풉니다.
4.  실행 파일이 있는 폴더에서 PowerShell을 열어 버전 명령을 확인합니다.

> **주의:** 다운로드한 실행 파일 폴더가 `PATH`에 등록되어 있지 않으면,
> 다른 폴더에서 `llama` 명령이 인식되지 않을 수 있습니다. 처음에는 실행
> 파일이 있는 폴더에서 명령을 실행하는 방법이 가장 단순합니다.

공식 프로젝트와 릴리스에서 제공하는 최신 설치 방법을 기준으로
진행하세요. 배포 버전에 따라 명령 옵션이 바뀔 수 있습니다.

## 4. 모델 다운로드 및 서버 실행

### 4-1. 모델 선택

이전 작업에서는 Qwen 계열 GGUF 모델을 사용했습니다. 모델 이름과 크기는
PC 메모리 및 성능에 맞춰 선택합니다.

예시 모델 저장소:

- `Qwen/Qwen3.5-0.8B-GGUF`
- `SoAIHQ/Qwen3.5-4B-GGUF`의 `Q4_K_M` 양자화 모델(지원 여부와 저장소의
  최신 사용법 확인 필요)

작은 모델은 메모리를 적게 사용하지만 답변 품질이 제한될 수 있습니다. 큰
모델은 더 많은 메모리와 처리 시간이 필요합니다.

### 4-2. Hugging Face에서 모델을 불러 서버 실행

사용 중인 llama.cpp 버전이 `llama serve -hf` 명령을 지원하는 경우,
다음과 같은 형식으로 실행할 수 있습니다.

```powershell
llama serve -hf SoAIHQ/Qwen3.5-4B-GGUF:Q4_K_M -c 8192 --port 9931
```

이 명령은 모델을 내려받거나 캐시에서 불러온 뒤 서버를 실행합니다. 실제
저장소의 모델 태그와 양자화 이름이 다르면 해당 저장소 안내에 맞게
수정하세요.

이미 Qwen 0.8B 모델을 사용하고 있다면, 그 모델의 정확한 저장소 이름을
명령에 넣으면 됩니다.

> 모델을 처음 실행할 때는 파일 크기에 따라 다운로드 시간이 오래 걸릴 수
> 있습니다. 서버가 실행 중인 터미널은 종료하지 마세요.

### 4-3. 서버 주소

이 프로젝트의 Python 예제는 다음 주소를 사용합니다.

```text
http://localhost:9931/v1
```

`localhost`는 현재 PC를 의미합니다. 다른 사람이 인터넷을 통해 이 주소로
접속할 수 있는 공개 서버가 아닙니다.

서버를 중지하려면 서버가 실행 중인 터미널에서 `Ctrl + C`를 누릅니다.

## 5. Python 가상환경과 라이브러리 설치

VS Code 터미널에서 프로젝트 폴더에 있는지 확인합니다.

```powershell
cd C:\local-rag
```

가상환경을 만듭니다.

```powershell
py -3.13 -m venv .llm
```

가상환경을 활성화합니다.

```powershell
.\.llm\Scripts\Activate.ps1
```

PowerShell에서 실행 정책 오류가 발생하면, 현재 사용자 정책을 바꾸기 전에
VS Code 터미널에서 안내된 오류 내용을 확인하세요. 필요하면 명령
프롬프트(CMD)에서 다음을 실행할 수 있습니다.

```bat
.llm\Scripts\activate.bat
```

필요한 라이브러리를 설치합니다.

```powershell
python -m pip install --upgrade pip
python -m pip install openai pymupdf sentence-transformers numpy
```

### 왜 `fitz`가 아니라 `pymupdf`를 설치하나요?

- 설치할 패키지 이름: `pymupdf`
- Python 코드에서 사용하는 이름: `fitz`

다음 명령으로 확인할 수 있습니다.

```powershell
python -c "import fitz; print('PyMuPDF 설치 확인 완료')"
```

`pip install fitz`는 사용하지 마세요. 이 프로젝트에서 필요한 것은
`pymupdf`입니다.

## 6. `requirements.txt` 만들기

프로젝트 폴더에 `requirements.txt` 파일을 만들고 다음을 작성합니다.

```text
openai
pymupdf
sentence-transformers
numpy
```

다른 PC에서 의존성을 설치할 때는 다음 명령을 사용합니다.

```powershell
python -m pip install -r requirements.txt
```

## 7. 로컬 서버 연결 테스트

프로젝트 폴더에 `test_llm.py` 파일을 만들고 다음 코드를 작성합니다.

```python
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
            "content": "한국의 수도는 어디인가요? 한 문장으로 답하세요."
        }
    ],
    temperature=0.2,
    max_tokens=200
)

print(response.choices[0].message.content)
```

실행합니다.

```powershell
python test_llm.py
```

정상적으로 답변이 출력되면 Python에서 로컬 LLM 서버에 요청을 보낼 수
있는 것입니다.

`api_key="lm-studio"`는 이 로컬 예제에서 사용하는 자리표시자입니다. 실제
비밀 API 키가 아닙니다. 서버 설정에 따라 인증 동작은 달라질 수 있습니다.

문제가 생기면 다음을 확인합니다.

- llama.cpp 서버가 실행 중인지
- 포트가 `9931`인지
- `base_url`이 서버 주소와 일치하는지
- 모델 로딩 오류가 서버 터미널에 표시되는지

## 8. PDF RAG 프로그램 작성

프로젝트 폴더에 `pdf_rag.py` 파일을 만들고 다음 코드를 작성합니다.

```python
from pathlib import Path

import fitz
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer


# 1. 로컬 LLM 서버 연결
client = OpenAI(
    base_url="http://localhost:9931/v1",
    api_key="lm-studio"
)

# 2. 임베딩 모델 불러오기
embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")


def read_pdf(pdf_path):
    """PDF의 페이지별 텍스트를 추출합니다."""
    pdf = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text().strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    pdf.close()
    return pages


def split_text(pages, chunk_size=900, overlap=150):
    """페이지 텍스트를 겹치는 작은 조각으로 나눕니다."""
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text
                })

            start += chunk_size - overlap

    return chunks


def create_embeddings(chunks):
    """문서 조각을 임베딩 벡터로 변환합니다."""
    texts = ["passage: " + chunk["text"] for chunk in chunks]

    vectors = embedding_model.encode(
        texts,
        normalize_embeddings=True
    )

    return np.array(vectors)


def search_chunks(question, chunks, vectors, top_k=4):
    """질문과 의미가 가까운 문서 조각을 찾습니다."""
    question_vector = embedding_model.encode(
        ["query: " + question],
        normalize_embeddings=True
    )[0]

    scores = vectors @ question_vector
    best_indices = np.argsort(scores)[::-1][:top_k]

    return [chunks[i] for i in best_indices]


def ask_llm(question, relevant_chunks):
    """검색 결과를 바탕으로 로컬 LLM에 답변을 요청합니다."""
    context = "\n\n".join(
        f"[PDF {chunk['page']}페이지]\n{chunk['text']}"
        for chunk in relevant_chunks
    )

    prompt = f"""
다음은 사용자가 제공한 PDF에서 검색한 내용입니다.
아래 문맥을 근거로 질문에 답하세요.
문서에서 확인할 수 없는 내용은 추측하지 말고,
문서에서 확인할 수 없다고 말하세요.
답변에 근거가 된 PDF 페이지 번호를 표시하세요.

[검색한 문서 내용]
{context}

[질문]
{question}
"""

    response = client.chat.completions.create(
        model="local-model",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content


def main():
    pdf_path = input("분석할 PDF 파일 경로를 입력하세요: ").strip().strip('"')

    if not Path(pdf_path).is_file():
        print("PDF 파일을 찾을 수 없습니다.")
        return

    pages = read_pdf(pdf_path)

    if not pages:
        print("PDF에서 텍스트를 추출하지 못했습니다.")
        print("스캔한 PDF라면 OCR 작업이 필요할 수 있습니다.")
        return

    chunks = split_text(pages)

    if not chunks:
        print("검색할 문서 내용이 없습니다.")
        return

    print("문서 임베딩을 생성하고 있습니다...")
    vectors = create_embeddings(chunks)

    print(f"PDF 분석 준비 완료: {len(pages)}페이지, {len(chunks)}개 조각")

    while True:
        question = input("\n질문을 입력하세요 (종료하려면 q): ").strip()

        if question.lower() == "q":
            break

        if not question:
            continue

        relevant_chunks = search_chunks(question, chunks, vectors)
        answer = ask_llm(question, relevant_chunks)

        print("\n[답변]")
        print(answer)


if __name__ == "__main__":
    main()
```

### 코드의 핵심

- `read_pdf()`: PDF의 텍스트를 페이지별로 읽습니다.
- `split_text()`: 긴 텍스트를 900자 단위로 나누고, 조각 사이에 150자를
  겹치게 합니다.
- `create_embeddings()`: 각 문서 조각을 임베딩 벡터로 변환합니다.
- `search_chunks()`: 질문과 유사한 문서 조각 4개를 찾습니다.
- `ask_llm()`: 검색한 내용을 로컬 LLM에 전달하고 답변을 받습니다.

이 예제는 간단한 교육용 RAG입니다. 문서가 매우 많아지면 임베딩을 파일로
저장하거나 벡터 데이터베이스를 사용하는 방식으로 확장할 수 있습니다.

## 9. RAG 실행 및 테스트

먼저 별도 터미널에서 llama.cpp 서버를 실행해 둡니다. 그런 다음 VS Code의
프로젝트 터미널에서 가상환경을 활성화하고 실행합니다.

```powershell
.\.llm\Scripts\Activate.ps1
python pdf_rag.py
```

예를 들어 PDF 경로를 입력합니다.

```text
C:\local-rag\documents\테스트문서.pdf
```

그다음 질문을 입력합니다.

```text
이 문서의 핵심 내용을 요약해줘.
```

또는:

```text
문서에서 제시한 주요 문제점은 무엇인가요?
```

종료하려면 `q`를 입력합니다.

### 참고 사항

- PDF에 텍스트 레이어가 없고 페이지가 이미지로만 되어 있으면 PyMuPDF로
  텍스트가 추출되지 않을 수 있습니다. 이 경우 OCR이 필요합니다.
- 임베딩 모델을 처음 실행할 때 모델 파일을 인터넷에서 다운로드할 수
  있습니다.
- 이 예제는 실행할 때 PDF 전체의 임베딩을 메모리에 만듭니다. PDF가
  크면 시간이 오래 걸리거나 메모리를 많이 사용할 수 있습니다.
- 모델 답변은 완벽하지 않을 수 있으므로 원문과 페이지 번호를 함께
  확인하세요.

## 10. GitHub 공개 준비

GitHub에는 **코드와 설치 안내만 공개하고, 모델·가상환경·개인 문서는
제외**합니다.

### 10-1. `.gitignore` 만들기

프로젝트 최상위 폴더에 `.gitignore` 파일을 만들고 다음을 작성합니다.

```gitignore
# Python 가상환경 및 캐시
.llm/
.venv/
venv/
__pycache__/
*.py[cod]

# 환경변수 및 비밀키
.env
.env.*

# 로컬 모델 파일
*.gguf
*.safetensors
*.pt
*.pth
*.onnx

# 모델/임베딩 폴더
models/
model/
embeddings/

# 개인 PDF와 출력물
documents/
*.pdf
*.docx
*.xlsx

# 편집기/운영체제 파일
.vscode/
.DS_Store
Thumbs.db
```

`*.bin`은 모델이 아닌 다른 필요한 데이터에도 쓰일 수 있으므로, 무조건
제외하기보다는 실제 프로젝트에서 확인한 후 필요할 때 추가하세요.

### 10-2. 공개할 파일 확인

권장 저장소 구조:

```text
local-rag/
├── README.md
├── requirements.txt
├── .gitignore
├── pdf_rag.py
└── test_llm.py
```

다음은 저장소에 올리지 않습니다.

- `.llm/` 같은 Python 가상환경
- 대용량 GGUF 모델 파일
- Hugging Face 모델 캐시
- 개인 문서 및 저작권상 공개 권한이 없는 PDF
- `.env`와 API 키 또는 비밀번호
- 임시 파일과 개인 데이터

### 10-3. Git 저장소 초기화 및 업로드

GitHub에서 새 저장소를 만들었다고 가정한 기본 예시입니다.
`YOUR_GITHUB_NAME`과 `YOUR_REPOSITORY`는 본인 값으로 바꾸세요.

```powershell
git init
git add .gitignore README.md requirements.txt pdf_rag.py test_llm.py
git status
```

`git status` 결과를 보고 모델, PDF, 가상환경 파일이 포함되지 않았는지
확인합니다. 이상이 없으면 커밋합니다.

```powershell
git commit -m "Add local PDF RAG example"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_NAME/YOUR_REPOSITORY.git
git push -u origin main
```

이미 `origin`이 등록되어 있다면 `git remote add origin`을 다시 실행하지
말고 `git remote -v`로 확인하세요.

### 10-4. 중요: 이미 커밋한 대용량 파일

`.gitignore`는 **아직 Git이 추적하지 않는 파일**을 제외하는 데
사용됩니다. 모델 파일이나 대용량 CSV/MP4가 과거 커밋에 이미 포함되어
있다면 `.gitignore`를 추가하는 것만으로 과거 기록에서 제거되지 않습니다.

이미 추적 중인 파일은 실제 경로를 확인한 뒤 다음과 같이 인덱스에서
제외할 수 있습니다.

```powershell
git rm --cached "경로\파일명"
```

폴더라면:

```powershell
git rm -r --cached "경로\폴더명"
```

이 명령은 인덱스에서 제외할 뿐, 일반적으로 로컬 파일은 그대로 남깁니다.
다만 **이전 커밋에 들어간 대용량 파일은 저장소 기록에서도 정리해야 할 수
있으므로**, 기록을 변경하기 전에 현재 저장소 상태와 백업을 확인하세요.
공동 PC나 다른 사람과 공유하는 저장소에서는 무작정 `git reset --hard`
또는 `git push --force`를 실행하지 마세요.

## 11. 자주 발생하는 문제

### `ModuleNotFoundError: No module named 'fitz'`

```powershell
python -m pip install pymupdf
```

### `ModuleNotFoundError: No module named 'sentence_transformers'`

```powershell
python -m pip install sentence-transformers
```

### 서버 연결 오류

- 서버가 실행 중인지 확인합니다.
- Python 코드의 `http://localhost:9931/v1`과 서버 포트가 일치하는지
  확인합니다.
- 모델이 정상적으로 로딩되었는지 서버 터미널을 확인합니다.

### 모델 다운로드/실행 실패

- 모델 저장소 이름과 양자화 태그가 정확한지 확인합니다.
- 디스크 공간, 메모리, 인터넷 연결을 확인합니다.
- 사용 중인 llama.cpp 버전이 명령 옵션을 지원하는지 공식 문서를
  확인합니다.

### PDF에서 텍스트가 나오지 않음

스캔 이미지 PDF일 수 있습니다. OCR로 텍스트를 추출한 뒤 RAG에 넣어야
합니다.

### GitHub가 파일 크기 오류를 표시함

모델이나 데이터 파일이 커밋 기록에 포함되었을 수 있습니다.
`.gitignore`만 추가하지 말고 현재 Git 기록을 확인한 뒤 대용량 파일을
기록에서 정리하세요.

---

## 참고 링크

- llama.cpp 공식 저장소: https://github.com/ggml-org/llama.cpp
- llama.cpp 릴리스: https://github.com/ggml-org/llama.cpp/releases
- Hugging Face 임베딩 모델:
  https://huggingface.co/intfloat/multilingual-e5-small
- PyMuPDF 문서: https://pymupdf.readthedocs.io/
- OpenAI Python 라이브러리: https://github.com/openai/openai-python
- GitHub의 대용량 파일 안내:
  https://docs.github.com/en/repositories/working-with-files/managing-large-files

## 마무리 체크리스트

- [ ] llama.cpp가 설치되고 실행되는가?
- [ ] 모델 서버가 `localhost:9931`에서 실행되는가?
- [ ] `test_llm.py`가 답변을 출력하는가?
- [ ] PDF에서 텍스트가 추출되는가?
- [ ] RAG가 질문에 관련된 문서 내용을 찾아 답변하는가?
- [ ] `requirements.txt`가 있는가?
- [ ] `.gitignore`에 모델·가상환경·개인 PDF가 제외되어 있는가?
- [ ] `git status`로 공개될 파일을 확인했는가?
- [ ] 모델 파일이나 비밀키를 GitHub에 올리지 않았는가?
