from pydoc import doc
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

class input(BaseModel):
    tree_id : int
    light : float
    humidity : float
    temp : float

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

class input_tree(BaseModel):
    name: str
    desc: str
    base_light: list
    base_humidity: list
    base_temp: list
    mode_status :  int
    duration : int

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
def postnewtree(def_tree: input_tree):
    count = tree_collection.count_documents({}) + 1
    t = jsonable_encoder(def_tree)
    tree = {
        "tree_id" : count,
        "name" : t["name"],
        "desc" : t["desc"],
        "base_light" : t["base_light"],
        "base_humidity" : t["base_humidity"],
        "base_temp" : t["base_temp"]
    }
    robot = {
        "tree_id" : count,
        "mode_status" : t["mode_status"],
        "duration" : t["duration"]
    }
    record = {
        "tree_id" : count,
        "light" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "humidity" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        "temp" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    }
    tree_collection.insert_one(tree)
    robot_collection.insert_one(robot)
    record_collection.insert_one(record)

    return {
        "result" : "success"
    }

@app.get("/getall")
def returnall():
    all_tree = record_collection.find()
    all = []
    for tree in all_tree:
        id = tree["tree_id"]
        tree_info = tree_collection.find_one({"tree_id":id})
        robot_info = robot_collection.find_one({"tree_id":id})

        light = tree["light"][41]
        humidity = tree["humidity"][41]
        temp = tree["temp"][41]
        
        tmp = {
            "id" : id,
            "name" : tree_info["name"],
            "mode_status" : robot_info["mode_status"],
            "duration" : robot_info["duration"],
            "base_light" : {
                "set" : tree_info["base_light"],
                "current" : light
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
                "current" : light
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

@app.delete("/deletetree/{tree_id}")
def delete_tree(tree_id : int):
    query = {"tree_id" : tree_id}
    test = robot_collection.find_one(query)
    if test == None:
        return{
            "result" : "not found"
        }
    else:
        robot_collection.delete_one(query)
        tree_collection.delete_one(query)
        record_collection.delete_one(query)

        update1 = robot_collection.find({"tree_id" : {"$gt":tree_id}})
        update2 = tree_collection.find({"tree_id" : {"$gt":tree_id}})
        update3 = record_collection.find({"tree_id" : {"$gt":tree_id}})

        # robot_collection.update_many({"tree_id" : {"$gt":tree_id}}, {"tree_id" : {"$toInt":"$tree_id"}-1})
        # tree_collection.update_many({"tree_id" : {"$gt":tree_id}}, {"tree_id" : {"$toInt":"$tree_id"}-1})
        # record_collection.update_many({"tree_id" : {"$gt":tree_id}}, {"tree_id" : {"$toInt":"$tree_id"}-1})

        for document in update1:
            cur_id = document["tree_id"]
            set_id = document["tree_id"] -1
            robot_collection.update_one({"tree_id" : cur_id},{"$set" : { "tree_id" : set_id}})
            tree_collection.update_one({"tree_id" : cur_id},{"$set" : { "tree_id" : set_id}})
            record_collection.update_one({"tree_id" : cur_id},{"$set" : { "tree_id" : set_id}})

        return{
            "result" : "success"
        }

@app.get("/command/{tree_id}")
def returnrobotcommand(tree_id : int):
    cur = robot_collection.find_one({"tree_id" : tree_id})
    tree = tree_collection.find_one({"tree_id":tree_id})
    if cur == None:
        return{
            "tree_id" : tree_id,
            "user_info" : 0
        }
    return {
        "tree_id" : tree_id,
        "user_info" : 1,
        "humidity" : tree["base_humidity"][1],
        "mode_status" : cur["mode_status"],
        "duration" : cur["duration"],
        "user_water" : cur["user_water"]
    }

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

@app.put("/water/{tree_id}")
def startwatering(tree_id : int):
    cur = robot_collection.find_one({"tree_id" : tree_id})
    if cur == None:
        return{
            "result" : "no tree found"
        }
    else:
        robot_collection.update_one({"tree_id": tree_id}, {"$set" : {"user_water" : 1}})
        return{
            "result" : "success"
        }

@app.put("/watered/{tree_id}")
def donewatering(tree_id : int):
    cur = robot_collection.find_one({"tree_id" : tree_id})
    if cur == None:
        return{
            "result" : "no tree found"
        }
    else:
        robot_collection.update_one({"tree_id": tree_id}, {"$set" : {"user_water" : 0}})
        return{
            "result" : "success"
        }