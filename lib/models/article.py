from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    _all_articles= {}
    def __init__(self, title, content, author_id, magazine_id, id=None):
        # Validate title, content, author_id, and magazine_id upon initialization
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters, inclusive.")
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string.")
        if not isinstance(author_id, int):
            raise TypeError("author_id must be an integer.")
        if not isinstance(magazine_id, int):
            raise TypeError("magazine_id must be an integer.")
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._id = id

         # If an ID is provided, add the instance to _all_articles cache
        if id is not None:
            Article._all_articles[id] = self
    @property
    def id(self):
        return self._id
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters, inclusive.")
        self._title = value
        if self.id is not None:  
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET title = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()
    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Content must be a non-empty string.")
        self._content = value
        if self.id is not None:  
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET content = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()
    @property
    def author_id(self):
        return self._author_id
    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise TypeError("author_id must be an integer.")
        self._author_id = value
        if self.id is not None:  
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET author_id = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()
    @property
    def magazine_id(self):
        return self._magazine_id
    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise TypeError("magazine_id must be an integer.")
        self._magazine_id = value
        if self.id is not None:  
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET magazine_id = ? WHERE id = ?", (value, self._id))
            conn.commit()
            conn.close()
    def save(self):
         """Saves the current Article instance to the database."""
         conn = get_connection()
         cursor = conn.cursor()
         if self.id is None:
            cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                           (self.title, self.content, self.author_id, self.magazine_id))
            self._id = cursor.lastrowid
            Article._all_articles[self.id] = self
         else:
            cursor.execute("UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                           (self.title, self.content, self.author_id, self.magazine_id, self.id))
         conn.commit()
         conn.close()

    def delete(self):
        """Deletes the current Article instance from the database."""
        if self.id is None:
            raise ValueError("Cannot delete article not yet saved to database.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        if self.id in Article._all_articles:
            del Article._all_articles[self.id]
        self._id = None

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        """Convenience method to create and save a new article."""
        article = cls(title, content, author_id, magazine_id)
        article.save()
        return article

    @classmethod
    def get_all(cls):
        """Retrieves all articles from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        articles = []
        for row in rows:
            if row['id'] in cls._all_articles:
                articles.append(cls._all_articles[row['id']])
            else:
                article = cls(title=row['title'], content=row['content'],
                              author_id=row['author_id'], magazine_id=row['magazine_id'],
                              id=row['id'])
                articles.append(article)
        return articles

    @classmethod
    def find_by_id(cls, id):
        """Finds an article by its ID."""
        if id in cls._all_articles:
            return cls._all_articles[id]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            article = cls(title=row['title'], content=row['content'],
                          author_id=row['author_id'], magazine_id=row['magazine_id'],
                          id=row['id'])
            return article
        return None

    
    def author(self):
        """Returns the Author instance for this article."""
        from lib.models.author import Author 
        return Author.find_by_id(self.author_id)

    def magazine(self):
        """Returns the Magazine instance for this article."""
        from lib.models.magazine import Magazine 
        return Magazine.find_by_id(self.magazine_id)