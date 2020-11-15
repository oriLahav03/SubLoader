def catch_exception_get_db(schema, error):
    values = False
    try:
        values = schema
    except:
        print(error)
    return values


def catch_exception_put_db(schema, error):
    try:
        schema
        return True
    except:
        print(error)
        return False


def get_free_ip(db):
    ips = catch_exception_get_db(db.child('IPS').order_by_child('used').limit_to_first(1).get().val(),
                                 'ERROR: cant get ip...')
    ip = ips.popitem()
    if ip[1]['used'] is False:
        return ip[0], ip[1]['ip']
    else:
        return 'no free ip'


def delete_user(username, token, email):
    sure = input("to verify the delete of the account type the username <" + username + ">: ")
    if sure == username:
        del_user(token, email)
    else:
        print('i guess you not that sure...')


def del_user(db,auth, token, email):
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
