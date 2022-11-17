from flask import Flask, render_template, request, jsonify
import pymongo
app = Flask(__name__)
client = pymongo.MongoClient("localhost",27017)

pond = {
    'name': "alpha", 
    'location': "jakarta", 
    'material': "beton", 
    'shape': "bundar"
    }
activation = {
    'name': "alpha",
    'ikan': "lele",
    'jumlah': "200",
    'berat': "50",
    'ketinggian': "1",
    'isactive': False,
    'tanggal': "19-01-2022"
    }
db = client.fishdb
db.pond.insert_one(pond)
db.activation.insert_one(activation)

@app.route("/api/v1/registrasi", methods=["POST"])
def register():
    getdata = request.form()
    result = db.pond.insert_one(jsonify(getdata))
    if result:
        return True
    return False

@app.route("/api/v1/aktifasi/<pondname>", methods=["POST"])
def activation(pondname):
    data = db.activation.find_one({"name":pondname})
    getdata = request.form()
    data["name"] = getdata["name"]
    data["ikan"] = getdata["ikan"]
    data["jumlah"] = getdata["jumlah"]
    data["ketinggian"] = getdata["ketinggian"]
    data["isactive"] = getdata["isactive"]
    data["tanggal"] = getdata["tanggal"]
    db.activation.update_one({"name": pondname}, {"$set": data})

@app.route("/api/v1/pondinfo", methods=["GET"])
def pondinfo():
    data = db.pond.find()
    return data

@app.route("/api/v1/pondinfo/<pondname>", methods=["GET"])
def pondstatus(pondname):
    data = db.pond.find_one({"name": pondname}, {})
    return data
