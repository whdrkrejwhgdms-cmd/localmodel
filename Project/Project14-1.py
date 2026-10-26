import py7zr

# 7zip 파일 생성 (압축)
with py7zr.SevenZipFile('C:\\AutoCoder\\Archive.7z', mode='w') as z:
    z.writeall('C:\\AutoCoder\\')