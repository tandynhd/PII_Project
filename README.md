# PII_Project
STEP 0: BASICS

Personally identifiable information (PII) broadly is any data that can be used to identify a specific individual. 
Identity card numbers, names, email address, and phone numbers have most commonly been considered PII, but technology has expanded the scope of PII considerably. 
It can now include locations, domain names, dates and more.
This project aims at scanning for PII data in various file formats and websites. 
Further, it lists all the data in a report along with its sensitivity.

STEP 1: INSTALLATION

1) Download the files in the repository
2) Install the following python libraries:
    - python -m spacy download en
    - python -m spacy download en_core_web_lg
    - pip install openpyxl
    - pip install PyPDF2
    - pip install bs4
    - pip install python-docx
    - pip install sqlalchemy
    - pip install MySQL
    - pip install pymongo
3) Go to the following py files and change the location to your file's path:
    - app.py (line 17)
    - scancsv.py (APP_FOLDER: line 14)
    - scandb.py (line 21)
    - scandoc.py (line 10)
    - scanpdf.py (line 9)
    - scantxt.py (line 9)
    - scanweb.py (APP_FOLDER: line 15)
    
STEP 2: RUNNING

1) Run app.py
2) Now head over to http://127.0.0.1:5000/

STEP 3: APPLICATION

1) PII Scanner Home
    - Lists all the files in the report folder and the number of PII data found in each of those files
    
2) Scan File
    - Radio buttons to choose what the user wants to scan (file or website)
    - Under file scanning the user has the ability to scan files of various extensions including csv, xlsx, db, docx, doc, pdf, txt
    - The other option is for the user to scan websites by just providing the website's link
    - After selecting the file to be scanned or entering the url of the website click on the scan button
    - The user is now redirected back to the Home page

3) PII Report
    - The user can select a file from the Report folder to view its report
