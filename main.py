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

@app.delete("/deletetree/{tree_id}/")
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