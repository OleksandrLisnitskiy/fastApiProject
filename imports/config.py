create_table = """CREATE TABLE IF NOT EXISTS classmates(
                    classmate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classmate_name CHAR(25), 
                    last_name CHAR(30), 
                    age INTEGER , 
                    major CHAR(40))"""

select_all = """SELECT * FROM classmates """

select_by_name = """SELECT * FROM classmates WHERE classmate_name = ?"""

select_by_age = """SELECT * FROM classmates WHERE age = ?"""

add_new_classmate = """INSERT INTO classmates(classmate_name, last_name, age, major) VALUES (?, ?, ?, ?)"""

change_existing_user = """UPDATE classmates SET 
                          classmate_name = ?,
                          last_name = ?,
                          age = ?,
                          major = ?
                          WHERE classmate_id = ?
                          """

delete_user = """DELETE FROM classmates WHERE classmate_id = ?"""

deleted_user_data = """SELECT * FROM classmates WHERE classmate_id = ?"""
