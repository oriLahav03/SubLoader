class get_data_err(Exception):
    """
    The class handle the data receiving error
    """
    def __init__(self, what, value):
        super(get_data_err, self).__init__()
        self.w = what
        self.val = value

    def __str__(self):
        return 'error getting data of ' + self.w + '\n values: ' + str(self.val)


class pw_err(Exception):
    """
    The class handle all the passwords errors
    """
    def __init__(self, err, val):
        super(pw_err, self).__init__()
        self.w = err
        self.v = val

    def __str__(self):
        return 'Invalid Password: ' + self.w


class email_err(Exception):
    """
    The function handle all the email errors
    """
    def __init__(self, err, val):
        super(email_err, self).__init__()
        self.w = err
        self.v = val

    def __str__(self):
        return 'Invalid Email: ' + self.w


class un_err(Exception):
    """
    The class handle all the username errors
    """
    def __init__(self, err, val):
        super(un_err, self).__init__()
        self.w = err
        self.v = val

    def __str__(self):
        return 'Invalid Username: ' + self.w
