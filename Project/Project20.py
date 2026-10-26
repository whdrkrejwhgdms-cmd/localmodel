import win32com.client

# Excel 애플리케이션 인스턴스 생성
excel = win32com.client.Dispatch("Excel.Application")
# 실행 중인 작업 확인을 위해 True로 설정. (백그라운드 실행을 원하면 False로 변경)
excel.Visible = True

# 엑셀 파일 및 경로 설정
path = "C:\\AutoCoder\\"
wb = excel.Workbooks.Open(path + "sheetSeperation.xlsx")

# 각 시트를 새로운 엑셀 파일로 분리 및 저장 반복
for sheet in wb.Sheets:
    new_wb = excel.Workbooks.Add()

    # 원본 시트를 새로운 엑셀 파일로 복사
    sheet.Copy(Before=new_wb.Worksheets("Sheet1"))

    # 새로운 엑셀 파일이 처음 생성될 때 존재하는 "Sheet1" 시트 삭제
    new_wb.Worksheets("Sheet1").Delete()

    # 시트 이름을 파일 이름으로 하여 엑셀 파일 저장
    new_wb.SaveAs(path + sheet.Name + ".xlsx")

# Excel 애플리케이션 종료
excel.Quit()