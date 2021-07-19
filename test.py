from flask import Flask, render_template, request, redirect, url_for
import os

global weblink


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

app.config["FILE_UPLOADS"] = "C:/Users/Tandin Dorji/Desktop/PII_Project/Mock"

@app.route("/upload", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":
        if request.files:

            try:
                for file in request.files.getlist('file'):
                    file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
                    print("file saved: "+file.filename)
    
 
            except:
                weblink = request.form["web-scan"]
                print(weblink)
                return(weblink)
                os.system("python scanweb.py")
            

            return redirect(request.url)


    return render_template("upload.html")

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