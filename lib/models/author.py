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
    # Retrieves an author by ID from the cache or database.
    @classmethod
    def create(cls, name):
        """Convenience method to create and save a new author."""
        author = cls(name)
        author.save()
        return author

    @classmethod
    def get_all(cls):
        """Retrieves all authors from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        authors = []
        for row in rows:
            if row['id'] not in cls._all_authors:
                authors.append(cls._all_authors[row['id']])
            else:
                author = cls(name=row['name'], id=row['id'])
                authors.append(author)
        return authors 
    @classmethod
    def find_by_id(cls, id):
        """Finds an author by their ID."""
        if id in cls._all_authors:
            return cls._all_authors[id]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            author = cls(name=row['name'], id=row['id'])
            return author
        return None
    # Finds an author by their name (case-insensitive).
    @classmethod
    def find_by_name(cls, name):
        """Finds an author by their name (case-insensitive)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name LIKE ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            if row['id'] in cls._all_authors:
                return cls._all_authors[row['id']]
            else:
                author = cls(name=row['name'], id=row['id'])
                return author
        return None
    def articles(self):
        """Returns a list of Articles written by the author."""
        from lib.models.article import Article
        conn= get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return[Article(row['title'], row['content'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
    def magazines(self):
        """Returns a list of Magazines that the author has contributed to."""
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT DISTINCT magazines. id, magazines.name, magazines. category
                        FROM magazines 
                       INNER JOIN articles ON magazines.id = articles.magazine_id 
                       WHERE articles.author_id = ?""", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(name=row['name'], category=row['category'], id=row['id']) for row in rows]
    
    def topic_areas(self):
        """Returns a list of unique categories of magazines the author has contributed to."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT M.category
            FROM magazines M
            INNER JOIN articles A ON M.id = A.magazine_id
            WHERE A.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows if row['category']]