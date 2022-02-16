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

@app.delete("/deletetree/{tree_id}")
def delete_tree(tree_id : int):
    query = {"tree_id" : tree_id}
    test = robot_collection.find_one(query)
    if test == None:
        return{
            "result" : "not found"
        }
    robot_collection.delete_one(query)
    tree_collection.delete_one(query)
    record_collection.delete_one(query)
    return{
        "result" : "success"
    }

@app.get("/command/{tree_id}")
def returnrobotcommand(tree_id : int):
    cur = robot_collection.find_one({"tree_id" : tree_id})
    return {
        "tree_id" : tree_id,
        "mode_status" : cur["mode_status"],
        "duration" : cur["duration"]
    }

@app.get("/getrecord/{tree_id}")
def returnrecord(tree_id : int):
    tree = record_collection.find_one({"tree_id":tree_id})
    light = tree["light"]
    humidity = tree["humidity"]
    temp = tree["temp"]
    return{
        "tree_id" : tree_id,
        "light" : light,
        "humidity" : humidity,
        "temp" : temp
    }
  
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

@app.get("/getall")
def returnall():
    all_tree = record_collection.find()
    all = []
    for tree in all_tree:
        id = tree["tree_id"]
        tree_info = tree_collection.find_one({"tree_id":id})

        light = tree["light"][41]
        humidity = tree["humidity"][41]
        temp = tree["temp"][41]
        
        tmp = {
            "tree_id" : id,
            "base_light" : {
                "set" : tree_info["base_light"],
                "curret" : light
                },
            "base_humidity" : {
                "set" : tree_info["base_humidity"],
                "current" : humidity
                },
            "base_temp" : {
                "set" : tree_info["base_temp"],
                "current" : temp
                },
        }
        all.append(tmp)
    return {
        "res_amount" : len(all),
        "result" : all
    }
