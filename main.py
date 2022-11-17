from flask import Flask, render_template, request, jsonify
import pymongo
import datetime
from enum import Enum

app = Flask(__name__)
client = pymongo.MongoClient("localhost", 27017)

class PondMaterial(Enum):
    Tanah = 1
    Beton = 2
    Terpal = 3

class PondShape(Enum):
    PersegiPanjang = 1
    Elips = 2

pond = {
    'name': "Alpha",
    'location': "Jakarta",
    'material': PondMaterial.Beton,
    'shape': PondShape.PersegiPanjang
    }
activation = {
    'pond_name': "Alpha",
    'fish_species': "Lele",
    'fish_count': 200,
    'total_weight': 50,
    'water_depth': 1,
    'is_active': False,
    'activation_date': datetime.datetime(2022, 1, 19)
    }
db = client.fishdb
db.ponds.insert_one(pond)
db.ponds_activation.insert_one(activation)

@app.route("/api/v1/ponds/registration", methods=["POST"])
def register_pond():
    getdata = request.form()
    result = db.ponds.insert_one(jsonify(getdata))
    if result:
        return True
    return False

@app.route("/api/v1/ponds/activation/<pond_name>", methods=["POST"])
def activation(pond_name):
    data = db.ponds_activation.find_one({"name": pond_name})
    getdata = request.form()
    data["pond_name"] = getdata["pond_name"]
    data["fish_species"] = getdata["fish_species"]
    data["fish_count"] = getdata["fish_count"]
    data["water_depth"] = getdata["water_depth"]
    data["is_active"] = getdata["is_active"]
    data["activation_date"] = getdata["activation_date"]
    db.ponds_activation.update_one({"name": pond_name}, {"$set": data})

@app.route("/api/v1/ponds/info", methods=["GET"])
def pondinfo():
    data = db.ponds.find()
    return data

@app.route("/api/v1/ponds/info/<pond_name>", methods=["GET"])
def pondstatus(pond_name):
    data = db.ponds.find_one({"name": pond_name}, {})
    return data
