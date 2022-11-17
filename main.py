from flask import Flask, render_template,request, jsonify
import pymongo
app= Flask(__name__)
client=pymongo.MongoClient("localhost",27017)
pond={"name": "alpha", "location":"jakarta", "material": "beton", "shape":"bundar"}
activation={"name":"alpha","ikan":"lele","jumlah":"200","berat":"50","ketinggian":"1","isactive":False,"tanggal":"19-01-2022"}
db=client.fishdb
db.pond.insert_one(pond)
db.activation.insert_one(activation)

@app.route("/api/v1/registrasi",methods=["POST"])
def regis():
    getdata=request.form()
    result=db.pond.insert_one(jsonify(getdata))
    if result:
        return True
    return False
