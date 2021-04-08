from custom_exeptions import *


def catch_exception_get_db(schema, error):
    """
    the function manage all the schemas to the firebase database that related to get data from the database
    :param schema: the command that gives the data from the database
    :param error: the error that the schema can cuz
    :return: the data from the database
    """
    values = False
    try:
        values = schema
    except:
        print(error)
    return values


def catch_exception_put_db(schema, error):
    """
    the function manage all the schemas to the firebase database that related to put data in the database
    :param schema: the command that put the data in the database
    :param error: the error that the schema can cuz
    :return: if the schema worked good
    """
    try:
        schema
    except:
        print(error)
        raise update_table_err('', str(error))
    return True



