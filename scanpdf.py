import PyPDF2 as p2
import pandas as pd
import os

print("Converting .pdf -> .csv ...")

location = 'C:/Users/Tandin Dorji/Desktop/Mock/pdf'

onlyfiles = next(os.walk(location))[2]

PII_Inventory = []
data_source=[]

for index in range (len(onlyfiles)):
    i = 0
    PDFFile = open('C:/Users/Tandin Dorji/Desktop/Mock/pdf/'+onlyfiles[index], "rb")
    pdfRead = p2.PdfFileReader(PDFFile)
    while i < pdfRead.getNumPages():
        pageinfo = pdfRead.getPage(i)
        info = pageinfo.extractText().split(" ")
        PII_Inventory.append(info)
        i += 1
    index+=1
    data_source.append(onlyfiles[index-1])  

report = pd.DataFrame(PII_Inventory)
report.to_csv('C:/Users/Tandin Dorji/Desktop/Mock/scan/Mock_report(pdf).csv')
print(data_source)
print('[complete]')
os.system("python scanfile2.py")