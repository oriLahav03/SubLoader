def catch_exception_put_db(schema, error):
    try:
        schema
    except:
        print(error)


def create_ip_table():
    counter = 1
    while counter <= 255:
        catch_exception_put_db(db.child("IPS").child("ip" + str(counter)).set({
            'ip': '25.200.0.' + str(counter), 'used': False}),
            'ERROR: cant create ip table')
        counter += 1