from costumExeptions import *


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


def get_free_ip(db):
    """
    the function give the first free to use ip from the database
    :param db: the database with the ips
    :return: the ip
    """
    ips = catch_exception_get_db(db.child('IPS').order_by_child('used').limit_to_first(1).get().val(),
                                 'ERROR: cant get ip...')
    ip = ips.popitem()
    if ip[1]['used'] is False:
        return ip[0], ip[1]['ip']
    else:
        raise get_ip_err()
