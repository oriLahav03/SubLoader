def catch_exception_put_db(schema, error):
    """
    the function manage all the schemas to the firebase database that related to put data in the database
    :param schema: the command that put the data in the database
    :param error: the error that the schema can cuz
    :return: None
    """
    try:
        schema
    except:
        print(error)


def create_ip_table(db):
    """
    the function create table with all the available ips in the database
    :param db: the database
    :return: None
    """
    counter = 1
    while counter <= 255:
        catch_exception_put_db(db.child("IPS").child("ip" + str(counter)).set({
            'ip': '25.200.0.' + str(counter), 'used': False}),
            'ERROR: cant create ip table')
        counter += 1
