class get_ip_err(Exception):
    def __init__(self, msg='no free ip'):
        super().__init__(msg)
        self.err = msg

    def __str__(self):
        return self.err


class join_room_err(Exception):
    def __init__(self, room_name, msg="can't join to room"):
        super().__init__(msg)
        self.err = msg
        self.room_err = room_name

    def __str__(self):
        return 'room ' + self.room_err + ' error: ' + self.err


class update_table_err(Exception):
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
    def __init__(self, name, zone):
        super(name_taken, self).__init__(name)
        self.name = name         
        self.zone = zone

    def __str__(self):
        return self.name + ' already exists in ' + self.zone