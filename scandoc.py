import docx
from docx import Document
import pandas as pd
import os

print("Converting .doc -> .csv ...")

location = 'C:/Users/Tandin Dorji/Desktop/Mock/doc'

onlyfiles = next(os.walk(location))[2]

PII_Inventory = []
data_source=[]

for i in range(len(onlyfiles)):
    document = Document('C:/Users/Tandin Dorji/Desktop/Mock/doc/'+onlyfiles[i])
    #index= 0
    for para in document.paragraphs:
        #index+=1
        if (len(para.text)>0):
            info = para.text.split(" ")
            PII_Inventory.append(info)
    i+=1
    data_source.append(onlyfiles[i-1])  
    
report = pd.DataFrame(PII_Inventory)
report.to_csv('C:/Users/Tandin Dorji/Desktop/Mock/scan/Mock_report(docx).csv')
print(data_source)
print('[complete]')
os.system("python scanfile2.py")
