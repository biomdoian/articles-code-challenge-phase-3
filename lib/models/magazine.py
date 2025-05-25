from lib.db.connection import get_connection

class Magazine:
    _all_magazines = {} 

    # Validate name and category upon initialization
    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters, inclusive.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._name = name
        self._category = category
        self._id = id

        # If id is not None, add to cache
        if id is not None:
            Magazine._all_magazines[id] = self

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters, inclusive.")
        self._name = value
        if self._id is not None: # Update DB if already saved
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE magazines SET name = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value
        if self._id is not None: 
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE magazines SET category = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()

    def save(self):
        """Saves the current Magazine instance to the database."""
        conn = get_connection()
        cursor = conn.cursor()
        if self._id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self._id = cursor.lastrowid
            Magazine._all_magazines[self._id] = self
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self._id))
        conn.commit()
        conn.close()

    def delete(self):
        """Deletes the current Magazine instance from the database."""
        if self._id is None:
            raise ValueError("Cannot delete a magazine not saved to the database.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM magazines WHERE id = ?", (self._id,))
        conn.commit()
        conn.close()
       
        if self._id in Magazine._all_magazines:
            del Magazine._all_magazines[self._id]
        self._id = None  # Clear the ID after deletion

    @classmethod
    def create(cls, name, category):
        """Creates a new Magazine instance and saves it."""
        magazine = cls(name, category)
        magazine.save()
        return magazine

    # Retrieves all magazines from the database.
    @classmethod
    def get_all(cls):
        """Returns all magazines from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()
        magazines_list = []
        for row in rows:
            if row['id'] in cls._all_magazines:
                magazines_list.append(cls._all_magazines[row['id']])
            else:
                magazine_instance = cls(name=row['name'], category=row['category'], id=row['id']) # Use a clear variable for the instance
                magazines_list.append(magazine_instance)
        return magazines_list 

    # Retrieves a magazine by its ID from the database.
    @classmethod
    def find_by_id(cls, id):
        """Finds a magazine by its ID."""
        if id in cls._all_magazines:
            return cls._all_magazines[id]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            magazine = cls(name=row['name'], category=row['category'], id=row['id'])
            return magazine
        return None

    # Retrieves a magazine by its name from the database.
    @classmethod
    def find_by_name(cls, name):
        """Finds a magazine by its name (case-insensitive)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name LIKE ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            if row['id'] in cls._all_magazines:
                return cls._all_magazines[row['id']]
            else:
                magazine = cls(name=row['name'], category=row['category'], id=row['id'])
                return magazine
        return None