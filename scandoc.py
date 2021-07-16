import docx
from docx import Document
import pandas as pd
import os

print("Converting .doc -> .csv ...")

location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/doc'

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
report.to_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/doc/scan/Mock_report(docx).csv')
print(data_source)
print('[complete]')

##################################################################################
##################################################################################

from pandas import *
from presidio_analyzer.analyzer_engine import AnalyzerEngine
import customreg

engine = AnalyzerEngine()
print('Scanning for PII data...')

engine.registry.add_recognizer(customreg.Th_passport_recognizer())
engine.registry.add_recognizer(customreg.Th_phone_recognizer())
engine.registry.add_recognizer(customreg.Th_ID_recognizer())

APP_FOLDER = 'C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/doc/scan'

onlyfiles = next(os.walk(APP_FOLDER))[2] #dir is your directory path as string

#text = 'citizen id  083-0174456 AA1254846 1-2001-01756-87-5'
df = read_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/doc/scan/'+onlyfiles[0]) 
columns = list(df)
pii_inventory = []
#d=[]
pii_categories =[]
data_source=[]
pii_type = []
for i in range(len(onlyfiles)):
    if ((onlyfiles[i][-5:]) != '.xlsx'):
        if (os.stat(APP_FOLDER +'/'+onlyfiles[i]).st_size) == 0:
            continue
        df = read_csv(APP_FOLDER +'/'+onlyfiles[i])
        for col in columns: 
            for index in df.index: 
                response = engine.analyze(correlation_id=0,
                                        text = str(df[col][index]),
                                        entities=[],language='en',
                                        #all_fields=True,
                                        score_threshold=0.6,)
                if (response != []):
                    pii_inventory.append({'type': response[0].entity_type,
                    'context':str(df[col][index]),
                    'position': "col: {}, row: {}".format(col,index),
                    'confidence': response[0].score,
                    'File': onlyfiles[i]})
    elif ((onlyfiles[i][-4:]) != '.csv'): 
        df = read_excel(APP_FOLDER +'/'+onlyfiles[i])
        for col in columns: 
            for index in df.index: 
                response = engine.analyze(correlation_id=0,
                                        text = str(df[col][index]),
                                        entities=[],language='en',
                                        #all_fields=True,
                                        score_threshold=0.6,)
                if (response != []):
                    pii_inventory.append({'type': response[0].entity_type,
                    'context':str(df[col][index]),
                    'position': "col: {}, row: {}".format(col,index),
                    'confidence': response[0].score,
                    'File': onlyfiles[i]})
    
    data_source.append(onlyfiles[i])        
report = DataFrame(pii_inventory)

report.to_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/report/mock_report(doc).csv')

print(data_source)
print('[complete]')

