from flask import Flask, Response, render_template, request, jsonify
import pymongo
import json
#from bson.objectid import ObjectId

app = Flask(__name__)
#app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.pdf']
#app.config['MONGO_URI'] = 'mongodb+srv://anyta:025914313@pii-inventory.ushbd.mongodb.net/test'
try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.CMS
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print("ERROR - Cannot connect to DB")
################################
# @app.route("/")
# def index():
#     return render_template('main.html')
################################ 
@app.route("/file-cs-check", methods=["POST"])
def file_check_ul():
    try:
        fileName = {"file_name" : request.form["filename"]}
        dbRespose = db.CMS_file.insert_one(fileName)
        print(dbRespose.inserted_id)
        # for attr in dir(dbRespose):
        #     print(attr)
        # error_message = json.dumps({"message":"%s haven’t get consent yet"%(fileName)})
        
        return Response(
            response = json.dumps(
                {"message":"%s got consent already"%(fileName),
                 "id":f"{dbRespose.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
        # return Response(
        #     response = json.dumps(
        #         {"message":"%s haven’t get consent yet"%(fileName),
        #          "id":f"{dbRespose.inserted_id}"
        #         }),
        #     status=404,
        #     mimetype="application/json"
        # )
    except Exception as ex:
        print("**************")
        print(ex)
        print("**************")
################################
# @app.route("/file-cs-status", methods=["GET"])
# def file_cs_status():
#     try:
#         data = list(db.CSM_file.find())
#         print(data)
#         return Response(
#             response = json.dumps(data),
#             status=200,
#             mimetype="application/json"
#         )
#     except Exception as ex:
#         print(ex)
#         return Response(
#             response = json.dumps({"message":"plese try again"}),
#             status=200,
#             mimetype="application/json"
#         )
################################
if __name__ == "__main__":
    app.run(port=8080, debug=True)
