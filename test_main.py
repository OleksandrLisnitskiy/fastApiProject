
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_find_by_age():
    response = client.get("/get_by_age?age=10")
    assert response.status_code == 200
    assert response.json()[0] == {"id": 1, "name": "string", "last_name": "string", "age": 10, "major": "string"}


def test_find_by_age_wrong():
    response = client.get("/get_by_age?age=1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No classmates with such age"}


def test_find_by_name():
    response = client.get("/get_by_name?name=string")
    assert response.status_code == 200
    assert type(response.json()[0]["age"]) == int
    assert response.json()[0]["age"] == 10


def test_find_by_name_wrong():
    response = client.get("/get_by_name?name=Sarthakbuil")
    assert response.status_code == 404
    assert response.json() == {"detail": "No classmates with such name"}


def test_adding_classmate():
    data = {
        "name": "Bogdam",
        "last_name": "Kugel",
        "age": 18,
        "major": "Physics"
    }
    response = client.post("/add_classmate", json=data)
    assert response.status_code == 201
    assert response.json() == data


def test_adding_wrong_classmate_name():
    data = {
        "last_name": "Kugel",
        "age": 18,
        "major": "Physics"
    }
    response = client.post("/add_classmate", json=data)
    assert response.status_code == 422


def test_adding_wrong_classmate_age():
    data = {
        "name": "Ndffwsfsd",
        "last_name": "Kugel",
        "major": "Physics"
    }
    response = client.post("/add_classmate", json=data)
    assert response.status_code == 422


def test_updating_classmate():
    data = {
        "name": "Sasha",
        "last_name":  "Lisnytskyi",
        "age": 18
    }
    response = client.put("/update?classmate_id=3", json=data)
    assert response.status_code == 201
    assert response.json()[0]["name"] == "Sasha"
    assert response.json()[0]["last_name"] == "Lisnytskyi"
    assert response.json()[0]["age"] == 18