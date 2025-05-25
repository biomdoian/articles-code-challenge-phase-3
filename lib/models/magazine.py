from lib.db.connection import get_connection

class Magazine:
    CONN = get_connection()
    CURSOR = CONN.cursor()

    _all_magazines = {} # Cache for all magazines

    def __init__(self, name, category, id=None):
        self.id = id
        # Use setters for validation
        self.name = name
        self.category = category

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
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters, inclusive.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string.")
        if len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO magazines (name, category)
                VALUES (?, ?)
            """
            Magazine.CURSOR.execute(sql, (self.name, self.category))
            self.id = Magazine.CURSOR.lastrowid
            Magazine._all_magazines[self.id] = self
        else:
            sql = """
                UPDATE magazines
                SET name = ?, category = ?
                WHERE id = ?
            """
            Magazine.CURSOR.execute(sql, (self.name, self.category, self.id))
            Magazine._all_magazines[self.id] = self
        Magazine.CONN.commit()

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    def delete(self):
        sql = "DELETE FROM magazines WHERE id = ?"
        Magazine.CURSOR.execute(sql, (self.id,))
        Magazine.CONN.commit()
        if self.id in Magazine._all_magazines:
            del Magazine._all_magazines[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, id):
        if id in cls._all_magazines:
            return cls._all_magazines[id]

        sql = "SELECT * FROM magazines WHERE id = ?"
        Magazine.CURSOR.execute(sql, (id,))
        row = Magazine.CURSOR.fetchone()
        if row:
            magazine = cls(row['name'], row['category'], row['id'])
            cls._all_magazines[magazine.id] = magazine
            return magazine
        return None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM magazines WHERE name = ?"
        Magazine.CURSOR.execute(sql, (name,))
        row = Magazine.CURSOR.fetchone()
        if row:
            magazine = cls(row['name'], row['category'], row['id'])
            cls._all_magazines[magazine.id] = magazine
            return magazine
        return None

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM magazines"
        Magazine.CURSOR.execute(sql)
        rows = Magazine.CURSOR.fetchall()
        return [cls(row['name'], row['category'], row['id']) for row in rows]

    def articles(self):
        from lib.models.article import Article # Local import to avoid circular dependency
        sql = "SELECT * FROM articles WHERE magazine_id = ?"
        Magazine.CURSOR.execute(sql, (self.id,))
        rows = Magazine.CURSOR.fetchall()
        return [Article(row['title'], row['content'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def authors(self):
        from lib.models.author import Author # Local import to avoid circular dependency
        sql = """
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """
        Magazine.CURSOR.execute(sql, (self.id,))
        rows = Magazine.CURSOR.fetchall()
        return [Author(row['name'], row['id']) for row in rows]

    def article_titles(self):
        articles_in_magazine = self.articles()
        return [article.title for article in articles_in_magazine] if articles_in_magazine else None


    def contributing_authors(self):
        from lib.models.author import Author # Local import to avoid circular dependency
        sql = """
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id, authors.name
            HAVING article_count >= 2
        """
        Magazine.CURSOR.execute(sql, (self.id,))
        rows = Magazine.CURSOR.fetchall()
        
        if not rows:
            return None # Return None if no authors contribute >= 2 articles
        
        return [Author(row['name'], row['id']) for row in rows]

    def __repr__(self):
        return f"<Magazine ID: {self.id}, Name: {self.name}, Category: {self.category}>"
