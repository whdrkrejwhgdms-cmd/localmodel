import py7zr

# 7zip 파일 해제 (읽기)
with py7zr.SevenZipFile('C:\\AutoCoder\\Archive.7z', mode='r') as z:
    z.extractall('C:\\AutoCoder\\')