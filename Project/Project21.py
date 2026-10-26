import win32com.client

def excel_to_pdf(excel_file_path, pdf_file_path):
    # Excel 애플리케이션 인스턴스 생성
    excel = win32com.client.Dispatch("Excel.Application")

    # Excel 파일 열기
    wb = excel.Workbooks.Open(excel_file_path)

    # PDF로 저장
    wb.ExportAsFixedFormat(0, pdf_file_path)

    # Excel 애플리케이션 종료
    excel.Quit()

# Excel 파일 경로 및 이름 설정
excel_file_path = "C:\\AutoCoder\\sheetSeperation.xlsx"

# PDF로 변환할 파일 경로 및 이름 설정
pdf_file_path = "C:\\AutoCoder\\sheetSeperation.pdf"

# Excel을 PDF로 변환
excel_to_pdf(excel_file_path, pdf_file_path)

print(f"{excel_file_path} 파일이 {pdf_file_path}로 성공적으로 변환되었습니다.")
