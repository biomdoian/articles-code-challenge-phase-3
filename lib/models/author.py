from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        #Validate the name upon initialization
        if not isinstance(name,str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self.name = name
        self._id = id
        #if id is not None add to cache
        if id is not None:
             Author._all_authors[id] = self

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0: # Validate the name if its being updated
            raise ValueError("Name must be a non-empty string")
        self._name = value