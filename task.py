class Task:
    def __init__(self,name,description,situation,id=None,date=None):
        self._id = id
        self._date = date
        self._name = name
        self._description = description
        self._situation = situation
