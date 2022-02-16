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

class robot_status(BaseModel):
    tree_id: int
    mode_status :  int
    duration : int

class default_tree(BaseModel):
    tree_id: int
    name: str
    desc: str
    base_light: list
    base_humidity: list
    base_temp: list

@app.put("/updatecommand")
def update_robot_status(ro_status : robot_status):
    r = jsonable_encoder(ro_status)
    query = {"tree_id": r["tree_id"]}
    update_status = {"$set" :{"mode_status" :r["mode_status"],"duration" :r["duration"]}}
    robot_collection.update_one(query, update_status)
    return {
        "result" : "update success"
    }
@app.post("/postnewtree")
def postnewtree(def_tree: default_tree):
    t = jsonable_encoder(def_tree)
    tree_collection.insert_one(t)
    return {
        "result" : "success"
    }