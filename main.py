from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import sqlite3
from imports.config import *
from imports.funcs import convertor
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# CONNECT SQLITE3 DATABASE
try:
    con = sqlite3.connect('classmates.db', check_same_thread=False)
    cur = con.cursor()
    res = cur.execute(create_table)
    res.fetchone()
except Exception as _ex:
    print("Please try again! Something wrong with database.")
    print(_ex)


class Classmate(BaseModel):
    """
    Inherits from BaseModel class from Pydantic
    Used to add/create new user in POST request
    """
    name: str
    last_name: Optional[str] = None
    age: int
    major: Optional[str] = None


class Classmate_Update(BaseModel):
    """
    Inherits from BaseModel class from Pydantic
    Used as type of value to change existing user in UPDATE request
    """
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    major: Optional[str] = None


@app.get("/", status_code=200)
async def root():
    """
    Function that is called after sending the request to root path 127.0.0.1:8000/

    :return: return information about all existing classmates
    """
    return convertor(cur.execute(select_all).fetchall())


@app.get('/get_by_name', status_code=200)
async def get_by_name(name: str = Query(default=...,
                                        description='Name of classmate to search')) -> list:
    """
    called after sending the request 127.0.0.1:8000/get_by_name

    :param name: name of the classmate to find (required)
    :return: information about all classmates with entered name
    """
    res = cur.execute(select_by_name, (name,)).fetchall()
    if res:
        return convertor(res)
    raise HTTPException(status_code=404, detail="No classmates with such name")


@app.get("/get_by_age", status_code=200)
async def get_by_age(age: int = Query(default=...,
                                      description='age of classmates you want to search')
                     ) -> list:
    """
    called after sending the request 127.0.0.1:8000/get_by_age

    :param age: age of the classmates to find (required)
    :return: list[list,...] list of lists with
    """
    res = cur.execute(select_by_age, (age,)).fetchall()
    if res:
        return convertor(res)
    raise HTTPException(status_code=404, detail="No classmates with such age")


@app.post("/add_classmate", status_code=201)
async def add_classmate(classmate: Classmate) -> str:
    """
    Add classmate to database
    Send JSON with data (name and age are required fields)

    :param classmate: Classmate type variable with all the data
    :return: Classmate type with added classmate
    """
    try:
        cur.execute(add_new_classmate,
                    (classmate.name,
                     classmate.last_name,
                     classmate.age,
                     classmate.major))
        con.commit()
    except:
        raise HTTPException(status_code=501, detail="Database issues")
    return jsonable_encoder(classmate)


@app.put("/update", status_code=201)
async def update_classmate(classmate: Classmate_Update,
                           classmate_id: int = Query(default=..., description="ID of classmate you want to change")) \
        -> list[dict]:
    """
    Function to update existing classmate info
    Send JSON with data that should be updated (no required fields)

    :param classmate: class Classmate_Update with data to update classmate info (only values that requires changes)
    :param classmate_id: ID of classmate to change, Query parameter in URL like http//x:8000?classmate_id=...
    :return: updated classmate info, return list of dict [{"id": ,"name": , "last_name": ,"age": , "major": }]
    """
    classmates = cur.execute(select_all).fetchall()
    for mate in classmates:
        if mate[0] == classmate_id:
            name = classmate.name if classmate.name is not None else mate[1]
            last_name = classmate.last_name if classmate.last_name is not None else mate[2]
            age = classmate.age if classmate.age is not None and classmate.age > 0 else mate[3]
            major = classmate.major if classmate.major is not None else mate[4]
            cur.execute(change_existing_user, (name, last_name, age, major, classmate_id))
            con.commit()
            return convertor([mate])
    raise HTTPException(status_code=404, detail="No such classmate in list")
