from lib.db.connection import get_connection

class Author:
    _all_authors = {} 
    def __init__(self, name, id=None):
        #Validate the name upon initialization
        if not isinstance(name,str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = name
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
            
            # Update the database if the author already exists
        if self._id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()

    def save(self):
        """Saves the current Author instance to the database."""
        conn = get_connection()
        cursor = conn.cursor()
         # Insert new author if id is not set
        if self._id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self._id = cursor.lastrowid
            Author._all_authors[self._id] = self
              # Update existing author if id is set 
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self._id))
        conn.commit()
        conn.close()

        #Adds Delete method to the Author class
    def delete(self):
        """Deletes the current Author instance from the database."""
        if self._id is None:
                raise ValueError("Cannot delete an author not saved to the database.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM authors WHERE id = ?", (self._id,))
        conn.commit()
        conn.close()

        # Remove from cache
        if self._id in Author._all_authors:
            del Author._all_authors[self._id]
        self._id = None
