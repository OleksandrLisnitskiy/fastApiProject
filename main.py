from fastapi import FastAPI, Query, HTTPException, Body, Header, status, Depends

import sqlite3

from imports.config import *
from imports.funcs import *
from imports.models import *

app = FastAPI()


async def open_connection() -> dict:
    """
    Open the connection with SQLite database
    :return:
    """
    try:
        con = sqlite3.connect('classmates.db', check_same_thread=False)
        cur = con.cursor()
        res = cur.execute(create_table)
        res.fetchone()
        return {"connection": con, "cursor": cur}
    except Exception as _Ex:
        print("Please try again! Something wrong with database.")
        print(_Ex)


@app.get("/", status_code=status.HTTP_200_OK, response_model=list[ClassmateOut])
async def root(dbData: dict = Depends(open_connection)) -> list[dict]:
    """
    Shows all the students from database

    - **return:** return information about all existing classmates
    """
    response = convertor_db_to_list(dbData["cursor"].execute(select_all).fetchall())
    dbData["connection"].close()
    return response


@app.get('/get_by_name', status_code=status.HTTP_200_OK, response_model=list[ClassmateOut])
async def get_by_name(dbData: dict = Depends(open_connection), name: str = Query(default=...,
                                                                         description='Name of classmate to search')) -> \
        list[dict]:
    """
    Shows all the students with the requested name

    - **name:**  name of the classmate to find (required)
    - **return:** information about all classmates with entered name
    """
    res = dbData["cursor"].execute(select_by_name, (name,)).fetchall()
    dbData["connection"].close()
    if res:
        return convertor_db_to_list(res)
    raise HTTPException(status_code=404, detail="No classmates with such name")


@app.get("/get_by_age", status_code=status.HTTP_200_OK, response_model=list[ClassmateOut])
async def get_by_age(dbData: dict = Depends(open_connection), age: int = Query(default=...,
                                                                       description='age of classmates you want to search')
                     ) -> list[dict]:
    """
    Shows all the students with the requested age

    - **age:** age of the classmates to find (required)
    - **return** list[list,...] list of lists with
    """
    classmates = dbData["cursor"].execute(select_by_age, (age,)).fetchall()
    dbData["connection"].close()
    if classmates:
        return convertor_db_to_list(classmates)
    raise HTTPException(status_code=404, detail="No classmates with such age")


@app.post("/add_classmate", status_code=status.HTTP_201_CREATED, response_model=ClassmateOut)
async def add_classmate(dbData: dict = Depends(open_connection),
                        classmate: ClassmateIn = Body(default=..., description="Data about classmate to add",
                                                      examples=examples_of_extra_schema)) -> dict:
    """
    Add classmate to database
    Send JSON with data (name and age are required fields)

    - **classmate:** Classmate type variable with all the data
    - **return:** Classmate type with added classmate
    """
    try:
        dbData["cursor"].execute(add_new_classmate,
                                 (classmate.name,
                                  classmate.last_name,
                                  classmate.age,
                                  classmate.major,
                                  classmate.location.country,
                                  classmate.location.city,
                                  classmate.location.street,
                                  classmate.location.apartment))
        dbData["connection"].commit()
    except Exception as _Ex:
        print(_Ex)
        raise HTTPException(status_code=501, detail="Database issues")
    classmate = classmate.dict()
    classmate["classmate_id"] = dbData["cursor"].lastrowid
    dbData["connection"].close()
    return classmate


@app.put("/update", status_code=status.HTTP_201_CREATED, response_model=ClassmateOut)
async def update_classmate(dbData: dict = Depends(open_connection), classmate: ClassmateUpdate = Body(default=...,
                                                                                              description="Data about classmate to change"),
                           classmate_id: int = Query(default=..., description="ID of classmate you want to change")
                           ) -> dict:
    """
    Function to update existing classmate info
    Send JSON with data that should be updated (no required fields)

    - **classmate:**  class Classmate_Update with data to update classmate info (only values that requires changes)
    - **classmate_id:**  ID of classmate to change, Query parameter in URL like http//x:8000?classmate_id=...
    - **return:**  updated classmate info, return list of dict [{"id": ,"name": , "last_name": ,"age": , "major": }]
    """

    try:
        mate = list(dbData["cursor"].execute(select_by_id, (classmate_id,)).fetchall()[0])

        mate[1] = classmate.name if classmate.name is not None else mate[1]
        mate[2] = classmate.last_name if classmate.last_name is not None else mate[2]
        mate[3] = classmate.age if classmate.age is not None and classmate.age > 0 else mate[3]
        mate[4] = classmate.major if classmate.major is not None else mate[4]

        if classmate.location:
            mate[5] = classmate.location.country if classmate.location.country is not None else mate[5]
            mate[6] = classmate.location.city if classmate.location.city is not None else mate[6]
            mate[7] = classmate.location.street if classmate.location.street is not None else mate[7]
            mate[8] = classmate.location.apartment if classmate.location.apartment is not None else mate[8]
        dbData["cursor"].execute(change_existing_user,
                    (mate[1], mate[2], mate[3], mate[4], mate[5], mate[6], mate[7], mate[8], classmate_id,))
        dbData["connection"].commit()
        dbData["connection"].close()
        return convertor_db_to_list([mate])
    except Exception as _Ex:
        print(_Ex)
        raise HTTPException(status_code=404, detail="No such classmate in list")


@app.delete("/delete_classmate", status_code=status.HTTP_200_OK, response_model=ClassmateOut)
async def delete_classmate(dbData: dict = Depends(open_connection), classmate_id: int = Query(default=..., description="Classmate ID to delete")
                           ) -> dict:
    """
    Function to delete classmate from database by his ID

    - **classmate_id:** int: classmate ID to be deleted
    - **return:** all data about deleted user list of dict [{"id": ,"name": , "last_name": ,"age": , "major": }]
    """
    try:
        deleted_classmate = dbData["cursor"].execute(deleted_user_data, (classmate_id,)).fetchall()

        dbData["cursor"].execute(delete_user, (classmate_id,))
        dbData["connection"].commit()
        dbData["connection"].close()
    except Exception as _EX:
        raise HTTPException(status_code=404, detail=f"No user with ID {classmate_id}")
    return convertor_db_to_list(deleted_classmate)


@app.get('/test_header', status_code=status.HTTP_200_OK, deprecated=True)
async def test_header(user_agent: str | None = Header(default=None), host: str | None = Header(default=None)):
    return {'User-agent': user_agent,
            'Host': host}
