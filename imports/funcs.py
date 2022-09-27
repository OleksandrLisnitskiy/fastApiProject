def convertor(classmate) -> list[dict]:
    res = []
    for i in classmate:
        res.append({'id': i[0],
                    'name': i[1],
                    'last_name': i[2],
                    'age': i[3],
                    'major': i[4]})
    return res
