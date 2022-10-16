def convertor_db_to_list(classmate) -> list[dict] | dict:
    """
    function to convert data that comes from Database to readable one

    :param classmate: data from class Classmate to be converted to dict
    :return: list[dict]
    """
    classmates_list = []
    for i in classmate:
        classmates_list.append({'classmate_id': i[0],
                                'name': i[1],
                                'last_name': i[2],
                                'age': i[3],
                                'major': i[4],
                                'location': {
                                    'country': i[5],
                                    'city': i[6],
                                    'street': i[7],
                                    'apartment': i[8]
                                }})
    return classmates_list[0] if len(classmates_list) == 1 else classmates_list


def convertor_json_to_list(classmate) -> list[dict] | dict:
    """
    function to convert data from JSON to list of dicts

    :param classmate: data from class Classmate to be converted to dict
    :return: list[dict]
    """
    classmates_list = [{'name': classmate["name"],
                        'last_name': classmate["last_name"],
                        'age': classmate["age"],
                        'major': classmate["major"],
                        'location': {
                            'country': classmate["location"]["country"],
                            'city': classmate["location"]["city"],
                            'street': classmate["location"]["street"],
                            'apartment': classmate["location"]["apartment"],
                        },
                        }]
    return classmates_list[0] if len(classmates_list) == 1 else classmates_list
