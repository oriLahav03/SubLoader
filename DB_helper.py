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
        return False
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
        return 'no free ip'


def delete_user(username, token, email):
    """
    the function verify the delete of the user from the database.
    :param username: the username
    :param token: the token of the user
    :param email: the email of the user
    :return: None
    """
    sure = input("to verify the delete of the account type the username <" + username + ">: ")
    if sure == username:
        del_user(token, email)
    else:
        print('i guess you not that sure...')


def del_user(token, email):
    """
    the function handle all the user delete
    :param token: the user token
    :param email: the email of the user
    :return: None
    """
    try:
        auth.delete_user_account(token)
        flag = True
    except:
        print("cant delete user")
        flag = False

    if flag is True:
        stats = catch_exception_get_db(db.child('Users').order_by_child('email').equal_to(email).get().val(),
                                       'ERROR: cant get the stats')
        stat = stats.popitem()
        del_user_info = catch_exception_put_db(db.child('Users').child(stat[0]).set(None), 'ERROR: cant delete user')
        ips = catch_exception_get_db(
            db.child('IPS').order_by_child('ip').equal_to(stat[1]['ip']).get().val(),
            'ERROR: cant get ip')
        ip = ips.popitem()
        catch_exception_put_db(db.child('IPS').child(ip[0]).child('used').set(False),
                               'ERROR: cant change ip to not used')
