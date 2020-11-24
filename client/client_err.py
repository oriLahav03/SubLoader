class get_data_err(Exception):
    def __init__(self, what, value):
        super(get_data_err, self).__init__()
        self.w = what
        self.val = value

    def __str__(self):
        return 'error getting data of ' + self.w + '\n values: ' + str(self.val) 