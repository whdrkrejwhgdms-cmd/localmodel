import win32com.client
import itertools

# 엑셀 암호 걸린 파일 절대경로
filePath = 'C:/AutoCoder/encrypedExcel.xlsx'

# 패스워드 일치 여부 확인 함수 (엑셀 절대경로, 패스워드)
def check(path, password):
    try:
        # 엑셀 애플리케이션 열기
        excel = win32com.client.Dispatch("Excel.Application")
        # 엑셀 오픈 여부 확인
        excel.Visible = True
        print('start password with ' + password)
        # True는 read_only 기준으로 열람 의미
        excel.Workbooks.Open(path, False, True, None, password)
        print(password + ' is correct.')
        print('='*100)
        # 정상적으로 파일 오픈되면 True 반환
        return True

    except Exception:
        # 암호가 불일치하면 엑셀 애플리케이션 닫기
        excel.Quit()
        print(password + ' is not correct.')
        print('-'*100)
        # 정상적으로 열리지 않을 시 False 반환
        return False


# 무차별 대입 공격을 위해 대입 숫자/문자 조합 대상 나열
password_binding = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+"
# 첫번째 자리부터 4번째 자리까지 조합되도록 반복문 진행
for i in range(1, 5):
    # itertools.product(조합 숫자/문자 대상, 조합 바인딩 열)로써,
    # i가 1~4까지 변화하며 이에 조합도 1자리~4자리까지 변화
    string = itertools.product(password_binding, repeat=i)
    # 정렬하여 반환된 문자의 수만큼 반복
    for j in string:
        # 리스트로 반환된 값을 문자열로 변환 (''.join(리스트)는 문자열 변환 처리)
        pwd = ''.join(j)

        # 액셀 패스워드가 일치한다면 첫 번째 for j in string 반복문을 빠져나온다.
        if check(filePath, pwd) == True:
            break

    # 액셀 패스워드가 일치한다면 두 번째 for i in range(1,5) 반복문을 빠져나오며 모든 반복문을 종료한다.
    if check(filePath, pwd) == True:
        break