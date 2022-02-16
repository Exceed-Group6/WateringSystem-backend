from unittest import result
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

class input(BaseModel):
    tree_id : int
    light : float
    humidity : float
    temp : float

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('mongodb://localhost', 27017)
db = client["watering"]
robot_collection = db["robot_status"]
tree_collection = db["default_tree"]
record_collection = db["data_list"]

@app.put("/updatetree")
def update(input:input):
    s = jsonable_encoder(input)

    tree_id = s["tree_id"]
    light = s["light"]
    humidity = s["humidity"]
    temp = s["temp"]

    query = {"tree_id" : tree_id}

    record = record_collection.find_one(query)
    old_light = record["light"]
    old_humidity = record["humidity"]
    old_temp= record["temp"]

    old_light.pop(0)
    old_light.append(light)

    old_humidity.pop(0)
    old_humidity.append(humidity)
    
    old_temp.pop(0)
    old_temp.append(temp)

    up = {"$set" : {
        "light" : old_light,
        "humidity" : old_humidity,
        "temp" : old_temp
    }}

    record_collection.update_one(query, up)
    return{
        "result" : "success"
    }