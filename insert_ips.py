def create_ip_table():
    counter = 1
    while counter <= 255:
        db.child("IPS").child("ip" + str(counter)).set({
            'ip': '25.200.0.' + str(counter),
            'used': False})
        counter += 1