from flask import Flask, render_template, request, jsonify
import pymongo
app = Flask(__name__)
client = pymongo.MongoClient("localhost", 27017)

pond = {
    'name': "alpha", 
    'location': "jakarta", 
    'material': "beton", 
    'shape': "bundar"
    }
activation = {
    'pond_name': "alpha",
    'fish_species': "lele",
    'fish_count': "200",
    'total_weight': "50",
    'water_depth': "1",
    'is_active': False,
    'activation_date': "19-01-2022"
    }
db = client.fishdb
db.pond.insert_one(pond)
db.activation.insert_one(activation)

@app.route("/api/v1/ponds/registration", methods=["POST"])
def register_pond():
    getdata = request.form()
    result = db.pond.insert_one(jsonify(getdata))
    if result:
        return True
    return False

@app.route("/api/v1/ponds/activation/<pondname>", methods=["POST"])
def activation(pondname):
    data = db.activation.find_one({"name": pondname})
    getdata = request.form()
    data["pond_name"] = getdata["pond_name"]
    data["fish_species"] = getdata["fish_species"]
    data["fish_count"] = getdata["fish_count"]
    data["water_depth"] = getdata["water_depth"]
    data["is_active"] = getdata["is_active"]
    data["activation_date"] = getdata["activation_date"]
    db.activation.update_one({"name": pondname}, {"$set": data})

@app.route("/api/v1/ponds/info", methods=["GET"])
def pondinfo():
    data = db.pond.find()
    return data

@app.route("/api/v1/ponds/info/<pondname>", methods=["GET"])
def pondstatus(pondname):
    data = db.pond.find_one({"name": pondname}, {})
    return data
