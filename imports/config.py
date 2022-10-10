# SQL Requests

create_table = """CREATE TABLE IF NOT EXISTS classmates(
                    classmate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classmate_name CHAR(25), 
                    last_name CHAR(30), 
                    age INTEGER , 
                    major CHAR(40),
                    country CHAR(25),
                    city CHAR(25),
                    street CHAR(30),
                    apartment CHAR(5))
                    """

select_all = """SELECT * FROM classmates ORDER BY classmate_name"""

select_by_id = """SELECT * FROM classmates WHERE classmate_id = ?"""

select_by_name = """SELECT * FROM classmates WHERE classmate_name = ? ORDER BY classmate_name"""

select_by_age = """SELECT * FROM classmates WHERE age = ? ORDER BY classmate_name"""

add_new_classmate = """INSERT INTO classmates(classmate_name, last_name, age, major, country, city, street, apartment) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

change_existing_user = """UPDATE classmates SET 
                          classmate_name = ?,
                          last_name = ?,
                          age = ?,
                          major = ?,
                          country = ?,
                          city = ?,
                          street = ?,
                          apartment = ?
                          WHERE classmate_id = ?
                          """

delete_user = """DELETE FROM classmates WHERE classmate_id = ?"""

deleted_user_data = """SELECT * FROM classmates WHERE classmate_id = ?"""


# Examples of extra data for Pydantic Data Models

examples_of_extra_schema = {
                    "normal": {
                        "summary": "Example of normal data 1",
                        "description": "A **normal** input works correctly",
                        "value": {
                            "name": "Oleksandr",
                            "last_name": "Lisnytskyi",
                            "age": 18,
                            "major": "Computer Science",
                            "location": {
                                "country": "Ukraine",
                                "city": "Rivne",
                                "street": "Haidamatska",
                                "apartment": "122"
                            },
                        },
                    },
                    "normal_2": {
                        "summary": "Example of valid data 2",
                        "description": "A **normal** input without major",
                        "value": {
                            "name": "Oleksandr",
                            "last_name": "Lisnytskyi",
                            "age": 18,
                            "location": {
                                "country": "Ukraine",
                                "city": "Rivne"
                            },
                        },
                    },
                    "invalid": {
                        "summary": "Example of invalid data 1",
                        "description": "An **invalid** input without name and country Fields",
                        "value": {
                            "last_name": "Lisnytskyi",
                            "age": 18,
                            "major": "Computer Science",
                            "location": {
                                "city": "Rivne",
                                "street": "Haidamatska",
                                "apartment": "122"
                            },
                        },
                    },
                    "invalid_2": {
                        "summary": "Example of invalid data 2",
                        "description": "An **invalid** input without age and city Fields",
                        "value": {
                            "name": "Oleksandr",
                            "last_name": "Lisnytskyi",
                            "major": "Computer Science",
                            "location": {
                                "country": "Ukraine",
                                "street": "Haidamatska",
                                "apartment": "122"
                            },
                        },
                    },

                }

