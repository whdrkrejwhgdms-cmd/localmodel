import py7zr

# 7zip 파일 생성 및 비밀번호 설정 (압축)
with py7zr.SevenZipFile('C:\\AutoCoder\\Archive.7z', mode='w',
                        password='autocoder') as z:
    z.writeall('C:\\AutoCoder\\')