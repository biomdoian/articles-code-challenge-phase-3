from lib.db.connection import get_connection

class Author:
    CONN = get_connection()
    CURSOR = CONN.cursor()

    _all_authors = {} 

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
       # Initialize the class with the database connection and cursor
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value # ID is set by the database

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not (2 <= len(value) <= 50):
            raise ValueError("Name must be a string between 2 and 50 characters, inclusive.")
        self._name = value
     # Property for name with validation
    def save(self):
        if self.id is None:
            sql = "INSERT INTO authors (name) VALUES (?)"
            Author.CURSOR.execute(sql, (self.name,))
            self.id = Author.CURSOR.lastrowid
            Author._all_authors[self.id] = self
        else:
            sql = "UPDATE authors SET name = ? WHERE id = ?"
            Author.CURSOR.execute(sql, (self.name, self.id))
            Author._all_authors[self.id] = self
        Author.CONN.commit()
   # Save the author to the database, either inserting or updating
    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
# Class method to create a new author and save it to the database
    def delete(self):
        sql = "DELETE FROM authors WHERE id = ?"
        Author.CURSOR.execute(sql, (self.id,))
        Author.CONN.commit()
        if self.id in Author._all_authors:
            del Author._all_authors[self.id]
        self.id = None 
    @classmethod
    def find_by_id(cls, id):
        if id in cls._all_authors:
            return cls._all_authors[id]

        sql = "SELECT * FROM authors WHERE id = ?"
        Author.CURSOR.execute(sql, (id,))
        row = Author.CURSOR.fetchone()
        if row:
            author = cls(row['name'], row['id'])
            cls._all_authors[author.id] = author
            return author
        return None
  # Find an author by ID, either from the cache or the database
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM authors WHERE name = ?"
        Author.CURSOR.execute(sql, (name,))
        row = Author.CURSOR.fetchone()
        if row:
            author = cls(row['name'], row['id'])
            cls._all_authors[author.id] = author
            return author
        return None

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM authors"
        Author.CURSOR.execute(sql)
        rows = Author.CURSOR.fetchall()
        return [cls(row['name'], row['id']) for row in rows]
   # Get all authors from the database
    def articles(self):
        from lib.models.article import Article 
        sql = "SELECT * FROM articles WHERE author_id = ?"
        Author.CURSOR.execute(sql, (self.id,))
        rows = Author.CURSOR.fetchall()
        return [Article(row['title'], row['content'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
# Get all articles written by the author
    def magazines(self):
        from lib.models.magazine import Magazine 
        sql = """
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        Author.CURSOR.execute(sql, (self.id,))
        rows = Author.CURSOR.fetchall()
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]
    # Get all magazines written by the author
    def topic_areas(self):
        magazines_by_author = self.magazines()
        if not magazines_by_author:
            return []
        
        
        topic_set = set(magazine.category for magazine in magazines_by_author)
        return list(topic_set)

    def __repr__(self):
        return f"<Author ID: {self.id}, Name: {self.name}>"