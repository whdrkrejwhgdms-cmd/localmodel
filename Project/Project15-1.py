from docx2pdf import convert

# 변환시킬 워드 문서.docx
inputDocs = 'C:/AutoCoder/testWord.docx'

# PDF로 변환된 워드 문서.pdf
outputPDF = 'C:/AutoCoder/testPDF.pdf'

# 변환 작업
convert(inputDocs, outputPDF)