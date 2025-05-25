from lib.db.connection import get_connection
from lib.models.author import Author # Import Author
from lib.models.magazine import Magazine # Import Magazine

class Article:
    CONN = get_connection()
    CURSOR = CONN.cursor()

    _all_articles = {} # Cache for all articles

    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        # Use setters for validation
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value # ID is set by the database, no strong validation here

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters, inclusive.")
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError("Content must be a string.")
        if len(value) == 0:
            raise ValueError("Content must be a non-empty string.")
        self._content = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise TypeError("author_id must be an integer.")
        if value <= 0:
            raise ValueError("author_id must be a positive integer.")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise TypeError("magazine_id must be an integer.")
        if value <= 0:
            raise ValueError("magazine_id must be a positive integer.")
        self._magazine_id = value

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """
            Article.CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
            self.id = Article.CURSOR.lastrowid
            Article._all_articles[self.id] = self
        else:
            sql = """
                UPDATE articles
                SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """
            Article.CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
            Article._all_articles[self.id] = self
        Article.CONN.commit()

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        article = cls(title, content, author_id, magazine_id)
        article.save()
        return article

    def delete(self):
        sql = "DELETE FROM articles WHERE id = ?"
        Article.CURSOR.execute(sql, (self.id,))
        Article.CONN.commit()
        if self.id in Article._all_articles:
            del Article._all_articles[self.id]
        self.id = None # Invalidate the object's ID

    @classmethod
    def find_by_id(cls, id):
        if id in cls._all_articles:
            return cls._all_articles[id]

        sql = "SELECT * FROM articles WHERE id = ?"
        Article.CURSOR.execute(sql, (id,))
        row = Article.CURSOR.fetchone()
        if row:
            article = cls(row['title'], row['content'], row['author_id'], row['magazine_id'], row['id'])
            cls._all_articles[article.id] = article
            return article
        return None

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM articles"
        Article.CURSOR.execute(sql)
        rows = Article.CURSOR.fetchall()
        return [cls(row['title'], row['content'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def author(self):
        from lib.models.author import Author # Local import to avoid circular dependency
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine # Local import to avoid circular dependency
        return Magazine.find_by_id(self.magazine_id)

    def __repr__(self):
        return f"<Article ID: {self.id}, Title: {self.title}, Author ID: {self.author_id}, Magazine ID: {self.magazine_id}>"
