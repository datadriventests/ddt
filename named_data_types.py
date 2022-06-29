class NamedDataList(list):
    """ This is a helper class for @named_data that allows ddt tests to have meaningful names. """
    def __init__(self, name, *args):
        super(NamedDataList, self).__init__(args)
        self.name = name

    def __str__(self):
        return str(self.name)


class NamedDataDict(dict):
    """ This is a helper class for @named_data that allows ddt tests to have meaningful names. """
    def __init__(self, name, **kwargs):
        super(NamedDataDict, self).__init__(kwargs)
        self.name = name

    def __str__(self):
        return str(self.name)
