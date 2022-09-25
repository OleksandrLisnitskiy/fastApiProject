from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_find_by_age():
    response = client.get("/get_by_age?age=18")
    assert response.status_code == 200


def test_find_by_age_wrong():
    response = client.get("/get_by_age?age=1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No classmates with such age"}


def test_find_by_name():
    response = client.get("/get_by_name?name=Sarthak")
    assert response.status_code == 200
    assert type(response.json()[0][3]) == int
    assert response.json()[0][3] == 28


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
