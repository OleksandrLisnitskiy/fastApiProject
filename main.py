from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import sqlite3
from config import *

app = FastAPI()


# CONNECT SQLITE3 DATABASE
con = sqlite3.connect('classmates.db')
cur = con.cursor()
res = cur.execute(create_table)
res.fetchone()


# Inherits from BaseModel class from Pydantic
# Used to add/create new user
class Classmate(BaseModel):
    name: str
    last_name: Optional[str] = None
    age: int
    major: Optional[str] = None


# Inherits from BaseModel class from Pydantic
# Used to change existing user
class Classmate_Update(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    major: Optional[str] = None



@app.get("/")
async def root():
    """
    Function that is called after sending the request to root path 127.0.0.1:8000/

    :return: return information about all existing classmates
    """
    return cur.execute(select_all).fetchall()


@app.get('/get_by_name')
async def get_by_name(name: str = Query(None, description='Name of classmate to search')):
    """

    :param name: name of the classmate to find
    :return: information about all classmates with entered name
    """
    res = cur.execute(select_by_name, (name, ))
    return res.fetchall()



@app.get("/get_by_age")
async def get_by_age(age: int = Query(None, description='age of classmates you want to search')):
    res = cur.execute(select_by_age, (age,))
    return res.fetchall()
    # if res else HTTPException(status_code=404, detail="No classmates with such age")

    # return [classmates[item_id] for item_id in classmates if classmates[item_id].age == age]


@app.post("/add_classmate")
async def add_classmate(classmate: Classmate):
    cur.execute(add_new_classmate,
                (classmate.name,
                 classmate.last_name,
                 classmate.age,
                 classmate.major))
    con.commit()
    return classmate


"""
Send JSON with keys which you need to change
{
    "age": 23
}
"""
@app.put("/update")
async def update_classmate(classmate: Classmate_Update,
                           classmate_id: int = Query(None, description="ID of classmate you want to change")):

    classmates = cur.execute(select_all).fetchall()
    print(classmate)
    for mate in classmates:
        if mate[0] == classmate_id:
            name = classmate.name if classmate.name is not None else mate[1]
            last_name = classmate.last_name if classmate.last_name is not None else mate[2]
            age = classmate.age if classmate.age is not None and classmate.age > 0 else mate[3]
            major = classmate.major if classmate.major is not None else mate[4]
            cur.execute(change_existing_user, (name, last_name, age, major, classmate_id))
            con.commit()
            return mate
    return HTTPException(status_code=404, detail="No such classmate in list")

