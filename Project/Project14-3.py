import py7zr

# 7zip 파일에 파일 추가 (추가)
with py7zr.SevenZipFile('C:\\AutoCoder\\Archive.7z', mode='a') as z:
    z.write('C:\\AutoCoder\\append_file.txt')