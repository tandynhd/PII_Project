from flask import Flask, render_template, request, redirect, url_for
import os
from pandas import *

global weblink


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

app.config["FILE_UPLOADS"] = "C:/Users/Tandin Dorji/Desktop/PII_Project/Mock"
app.config["FILE_EXTENSIONS"] = ["CSV", "XLSX", "DB", "DOCX", "DOC", "PDF", "TXT"]

def allowed_files(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if request.files:
            
            #scanweb
            weblink = request.form["web-scan"]
            if weblink != "":
                print("Scan Web")
                file2 = open(r"C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/html/weblink.txt","w+") 
                file2.write(weblink)
                print("weblink saved")  
                os.system("python scanweb.py")

            #scanfiles
            else:
                # test = request.files["file"]
                for file in request.files.getlist('file'):
                    if not allowed_files(file.filename):
                        print(file.filename+" has an unsupported extension")
                        continue
                    else:                    
                        file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
                        print("file saved: "+file.filename)
                os.system("python main.py")

            # os.system("python main.py")
            # print(request.url)
            return redirect("http://127.0.0.1:5000/")
    
    return render_template('upload.html')

# @app.route('/home')
# def home():
#     return render_template('home2.html')
@app.route('/view-report')
def piiView():

    
    return render_template('ViewReport.html')

# @app.route('/view-report2')
# def piiView2():
#     return render_template('ViewReport2.html')

# @app.route('/pii_report')
# def piiReport():
#     return render_template('report.html')

# @app.route('/file-cs-check', methods=['POST'])
# def fileCheck():
#     uploaded_file = request.files['file']
#     if uploaded_file != '':
#         data_name = uploaded_file.save(uploaded_file.filename)
#     return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)