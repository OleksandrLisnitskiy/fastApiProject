from fastapi import FastAPI, Query, HTTPException, Body, Header
from fastapi.encoders import jsonable_encoder

import sqlite3

from imports.config import *
from imports.funcs import *
from imports.models import *


app = FastAPI()

# CONNECT SQLITE3 DATABASE
try:
    con = sqlite3.connect('classmates.db', check_same_thread=False)
    cur = con.cursor()
    res = cur.execute(create_table)
    res.fetchone()
except Exception as _Ex:
    print("Please try again! Something wrong with database.")
    print(_Ex)


@app.get("/", status_code=200, response_model=list[ClassmateOut])
async def root() -> list[dict]:
    """
    Function that is called after sending the request to root path 127.0.0.1:8000/

    :return: return information about all existing classmates
    """
    response = convertor_db_to_list(cur.execute(select_all).fetchall())
    return response


@app.get('/get_by_name', status_code=200, response_model=list[ClassmateOut])
async def get_by_name(name: str = Query(default=...,
                                        description='Name of classmate to search')) -> list[dict]:
    """
    called after sending the request 127.0.0.1:8000/get_by_name

    :param name: name of the classmate to find (required)
    :return: information about all classmates with entered name
    """
    res = cur.execute(select_by_name, (name,)).fetchall()
    if res:
        return convertor_db_to_list(res)
    raise HTTPException(status_code=404, detail="No classmates with such name")


@app.get("/get_by_age", status_code=200, response_model=list[ClassmateOut])
async def get_by_age(age: int = Query(default=...,
                                      description='age of classmates you want to search')
                     ) -> list[dict]:
    """
    called after sending the request 127.0.0.1:8000/get_by_age

    :param age: age of the classmates to find (required)
    :return: list[list,...] list of lists with
    """
    classmates = cur.execute(select_by_age, (age,)).fetchall()
    if classmates:
        return convertor_db_to_list(classmates)
    raise HTTPException(status_code=404, detail="No classmates with such age")


@app.post("/add_classmate", status_code=201, response_model=ClassmateOut)
async def add_classmate(classmate: ClassmateIn = Body(default=..., description="Data about classmate to add",
                                                      examples=examples_of_extra_schema)) -> dict:
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
                     classmate.major,
                     classmate.location.country,
                     classmate.location.city,
                     classmate.location.street,
                     classmate.location.apartment))
        con.commit()
    except Exception as _Ex:
        print(_Ex)
        raise HTTPException(status_code=501, detail="Database issues")
    classmate = convertor_json_to_list(jsonable_encoder(classmate))
    classmate["classmate_id"] = cur.lastrowid
    return classmate


@app.put("/update", status_code=201, response_model=ClassmateOut)
async def update_classmate(classmate: Classmate_Update = Body(default=...,
                                                              description="Data about classmate to change"),
                           classmate_id: int = Query(default=..., description="ID of classmate you want to change")
                           ) -> dict:
    """
    Function to update existing classmate info
    Send JSON with data that should be updated (no required fields)

    :param classmate: class Classmate_Update with data to update classmate info (only values that requires changes)
    :param classmate_id: ID of classmate to change, Query parameter in URL like http//x:8000?classmate_id=...
    :return: updated classmate info, return list of dict [{"id": ,"name": , "last_name": ,"age": , "major": }]
    """

    try:
        mate = list(cur.execute(select_by_id, (classmate_id,)).fetchall()[0])

        mate[1] = classmate.name if classmate.name is not None else mate[1]
        mate[2] = classmate.last_name if classmate.last_name is not None else mate[2]
        mate[3] = classmate.age if classmate.age is not None and classmate.age > 0 else mate[3]
        mate[4] = classmate.major if classmate.major is not None else mate[4]

        if classmate.location:
            mate[5] = classmate.location.country if classmate.location.country is not None else mate[5]
            mate[6] = classmate.location.city if classmate.location.city is not None else mate[6]
            mate[7] = classmate.location.street if classmate.location.street is not None else mate[7]
            mate[8] = classmate.location.apartment if classmate.location.apartment is not None else mate[8]
        cur.execute(change_existing_user, (mate[1], mate[2], mate[3], mate[4], mate[5], mate[6], mate[7], mate[8], classmate_id,))
        con.commit()
        return convertor_db_to_list([mate])
    except Exception as _Ex:
        print(_Ex)
        raise HTTPException(status_code=404, detail="No such classmate in list")


@app.delete("/delete_classmate", status_code=200, response_model=ClassmateOut)
async def delete_classmate(classmate_id: int = Query(default=..., description="Classmate ID to delete")
                           ) -> dict:
    """
    Function to delete classmate from database by his ID

    :param classmate_id: int: classmate ID to be deleted
    :return: all data about deleted user list of dict [{"id": ,"name": , "last_name": ,"age": , "major": }]
    """
    try:
        deleted_classmate = cur.execute(deleted_user_data, (classmate_id,)).fetchall()

        cur.execute(delete_user, (classmate_id,))
        con.commit()
    except Exception as _EX:
        raise HTTPException(status_code=404, detail=f"No user with ID {classmate_id}")
    return convertor_db_to_list(deleted_classmate)


@app.get('/test_header', status_code=200)
async def test_header(user_agent: str | None = Header(default=None), host: str | None = Header(default=None)):
    return {'User-agent': user_agent,
            'Host': host}
