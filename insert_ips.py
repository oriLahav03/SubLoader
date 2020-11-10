def create_ip_table():
    counter = 1
    while counter <= 255:
        try:
            db.child("IPS").child("ip" + str(counter)).set({
                'ip': '25.200.0.' + str(counter),
                'used': False})
        except:
            print('ERROR: cant create ip table')
        counter += 1