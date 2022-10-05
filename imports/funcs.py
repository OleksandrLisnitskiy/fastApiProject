def convertor_db_to_list(classmate) -> list[dict]:
    """
    function to convert data that comes from Database to readable one

    :param classmate: data from class Classmate to be converted to dict
    :return: list[dict]
    """
    classmates_dict = []
    for i in classmate:
        classmates_dict.append({'id': i[0],
                                'name': i[1],
                                'last_name': i[2],
                                'age': i[3],
                                'major': i[4]})
    return classmates_dict


def convertor_json_to_list(classmate) -> list[dict]:
    """
    function to convert data from JSON to list of dicts

    :param classmate: data from class Classmate to be converted to dict
    :return: list[dict]
    """
    return [{'name': classmate["name"],
             'last_name': classmate["last_name"],
             'age': classmate["age"],
             'major': classmate["major"]}]
