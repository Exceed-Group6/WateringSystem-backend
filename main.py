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

@app.get("/getall/")
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
        