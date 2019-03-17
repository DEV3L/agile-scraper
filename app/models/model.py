class Model:
    _id = ''

    def to_json(self):
        return self.__dict__
