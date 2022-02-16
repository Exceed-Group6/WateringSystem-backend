from unittest import result
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
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

@app.get("/getbyid/{tree_id}")
def returnbyid(tree_id : int):
    robot = robot_collection.find_one({"tree_id" : tree_id})
    find = tree_collection.find_one({"tree_id" : tree_id})
    tree = record_collection.find_one({"tree_id":tree_id})
    light = tree["light"][41]
    humidity = tree["humidity"][41]
    temp = tree["temp"][41]
    return{
        "tree_name" : find["name"],
        "tree_desc" : find["desc"],
        "cur_bot_status": robot["mode_status"],
        "cur_bot_duration" : robot["duration"],
        "base_light" : {
                "set" : find["base_light"],
                "curret" : light
                },
        "base_humidity" : {
            "set" : find["base_humidity"],
            "current" : humidity
            },
        "base_temp" : {
            "set" : find["base_temp"],
            "current" : temp
            },
    }