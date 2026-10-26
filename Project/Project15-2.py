from pathlib import Path
from docx2pdf import convert

# 특정 폴더 아래 모든 파일을 찾는다.
dir_path = Path('C:\\AutoCoder')

# 확장자가 docx인 파일만 찾는다.
for file in dir_path.glob('**/*.docx'):
    # 해당 확장자를 변환 대상 파일로 지정
    input_docs = file

    # 어떤 폴더에 있든 마지막 폴더 이름만 추출 후 pdf 파일로 변환할 절대경로로 지정
    filename = file.parts[-1][:-5]
    output_docs = f'C:\\AutoCoder\\{filename}.pdf'

    # 파일 변환 처리
    print(f'파일 변환 : {input_docs} -> {output_docs}')
    convert(input_docs, output_docs)
    print('변환된 파일 위치 :', output_docs)