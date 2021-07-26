import csv, os

location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files/report'

onlyfiles = next(os.walk(location))[2]
PII_Data = []
for i in range(len(onlyfiles)):
    file = open("C:/Users/Tandin Dorji/Desktop/PII_Project/files/report/"+onlyfiles[i])
    reader = csv.reader(file)
    lines = len(list(reader))
    PII_Data.append("There are "+str(lines-1)+" PII data in "+onlyfiles[i])

for index in range (len(PII_Data)):
    print(PII_Data[index])