import PyPDF2

def pdf_splitter(input_pdf, output_folder):
    # PDF 파일 열기
    with open(input_pdf, 'rb') as pdf_file:
        # PyPDF2의 PdfReader로 PDF 파일 읽기
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # 각 페이지별로 반복
        for page_num in range(len(pdf_reader.pages)):
            # 새로운 PDF 생성
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            # 새로운 PDF 파일로 저장
            output_filename = f"{output_folder}/page_{page_num + 1}.pdf"
            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

if __name__ == "__main__":
    # 입력 PDF 파일 경로와 출력 폴더를 지정
    input_pdf_path = 'C:\\AutoCoder\\sheetSeperation.pdf'
    output_folder_path = 'C:\\AutoCoder'

    # PDF 분리 함수 호출
    pdf_splitter(input_pdf_path, output_folder_path)