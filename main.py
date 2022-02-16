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

@app.get("/command/{tree_id}/")
def returnrobotcommand(tree_id : int):
    cur = robot_collection.find_one({"tree_id" : tree_id})
    return {
        "tree_id" : tree_id,
        "mode_status" : cur["mode_status"],
        "duration" : cur["duration"]
    }