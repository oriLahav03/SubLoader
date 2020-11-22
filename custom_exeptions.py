class get_ip_err(Exception):
    """
    get ip error: not free ip to use
    """
    def __init__(self, msg='no free ip'):
        super().__init__(msg)
        self.err = msg

    def __str__(self):
        return self.err


class join_room_err(Exception):
    """
    can't join to room for many reasons
    according to msg
    """
    def __init__(self, room_name, msg="can't join to room"):
        super().__init__(msg)
        self.err = msg
        self.room_err = room_name

    def __str__(self):
        return 'room ' + self.room_err + ' error: ' + self.err


class update_table_err(Exception):
    """
    can't update table on google DB
    """
    def __init__(self, table_name, msg="can't update table"):
        super().__init__(msg)
        self.err = msg
        self.table = table_name

    def __str__(self):
        return 'error update ' + self.table + " " + self.err

class room_not_exist(Exception):
    """
    room not exist expetion
    """
    def __init__(self, room_name, msg=''):
        super().__init__(msg)
        self.room = room_name
    
    def __str__(self):
        return 'room \'' + self.room + "' not exist "

class name_taken(Exceptions):
    """name taken in same place as zone
    """
    def __init__(self, name, zone):
        super(name_taken, self).__init__(name)
        self.name = name         
        self.zone = zone

    def __str__(self):
        return self.name + ' already exists in ' + self.zone

class get_userinfo_err(Exceptions):
    """can't get userinfo
    """
    def __init__(self, zone, val):
        super(get_userinfo_err, self).__init__()
        self.z = zone
        self.v = val
    
    def __str__(self):
        return 'can\'t find user with value ' + self.v + ' in ' + self.z  

class password_not_match(Exception):
    """password not match to object
    """
    def __init__(self, pw, room):
        super(password_not_match, self).__init__()
        self.pw = pw
        self.room = room

    def __str__(self):
        return 'password ' + self.pw + ' not match to ' + self.room