import PyPDF2
import os

def merge_pdfs(input_folder, output_file):
    # 새로운 PDF 생성
    pdf_writer = PyPDF2.PdfWriter()

    # 입력 폴더에서 PDF 파일 목록 가져오기
    pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.pdf')]

    # 각 PDF 파일을 순회하면서 병합
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        with open(pdf_path, 'rb') as pdf:
            pdf_reader = PyPDF2.PdfReader(pdf)
            # 현재 PDF 파일의 모든 페이지를 새로운 PDF에 추가
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

    # 병합된 PDF를 새로운 파일로 저장
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    # 입력 폴더와 출력 파일을 지정
    input_folder_path = 'C:\\AutoCoder'
    output_file_path = 'C:\\AutoCoder\\mergedPDFfiles.pdf'

    # PDF 병합 함수 호출
    merge_pdfs(input_folder_path, output_file_path)