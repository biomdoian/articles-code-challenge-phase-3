import pytest
import sqlite3
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

# Fixture to set up a clean database for each test
@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()
    yield # This allows the test to run
    # Teardown (optional): Clean up after each test if necessary
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_creation(setup_db):
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine", "Tech")
    article = Article("Title A", "Content A", author.id, magazine.id)
    assert article.title == "Title A"
    assert article.content == "Content A"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id
    assert article.id is None # ID should be None before saving

def test_article_save(setup_db):
    author = Author.create("Save Author")
    magazine = Magazine.create("Save Magazine", "Science")
    article = Article("Saved Article", "Some content here.", author.id, magazine.id)
    article.save()
    assert article.id is not None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    saved_article = cursor.fetchone()
    conn.close()
    assert saved_article is not None
    assert saved_article['title'] == "Saved Article"
    assert saved_article['content'] == "Some content here."
    assert saved_article['author_id'] == author.id
    assert saved_article['magazine_id'] == magazine.id

def test_article_create_class_method(setup_db):
    author = Author.create("Create Author")
    magazine = Magazine.create("Create Magazine", "Culture")
    article = Article.create("Created Article", "Content for created.", author.id, magazine.id)
    assert article.id is not None
    assert article.title == "Created Article"
    assert article.content == "Content for created."
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id
    # Verify it's in the DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    saved_article = cursor.fetchone()
    conn.close()
    assert saved_article is not None

def test_article_find_by_id(setup_db):
    author = Author.create("Find Author")
    magazine = Magazine.create("Find Magazine", "Art")
    article = Article.create("Found Article", "Its content.", author.id, magazine.id)
    found_article = Article.find_by_id(article.id)
    assert found_article is not None
    assert found_article.title == "Found Article"
    assert found_article.id == article.id

def test_article_find_by_id_not_found(setup_db):
    assert Article.find_by_id(999) is None

def test_article_get_all(setup_db):
    author = Author.create("Get All Author")
    magazine = Magazine.create("Get All Magazine", "News")
    article1 = Article.create("Article 1", "Content 1", author.id, magazine.id)
    article2 = Article.create("Article 2", "Content 2", author.id, magazine.id)
    all_articles = Article.get_all()
    assert len(all_articles) == 2
    assert any(a.title == "Article 1" for a in all_articles)
    assert any(a.title == "Article 2" for a in all_articles)

def test_article_title_validation(setup_db):
    author = Author.create("Val Author")
    magazine = Magazine.create("Val Magazine", "Sport")
    with pytest.raises(ValueError):
        Article("", "Content", author.id, magazine.id) # Too short
    with pytest.raises(ValueError):
        Article("A", "Content", author.id, magazine.id) # Too short
    with pytest.raises(ValueError):
        Article("This title is extremely long and definitely exceeds the fifty character limit for an article", "Content", author.id, magazine.id) # Too long
    with pytest.raises(TypeError):
        Article(123, "Content", author.id, magazine.id) # Not a string

def test_article_content_validation(setup_db):
    author = Author.create("Val Author 2")
    magazine = Magazine.create("Val Magazine 2", "Food")
    with pytest.raises(ValueError):
        Article("Valid Title", "", author.id, magazine.id) # Empty content
    with pytest.raises(TypeError):
        Article("Valid Title", 123, author.id, magazine.id) # Not a string

def test_article_author_id_validation(setup_db):
    author = Author.create("Val Author 3")
    magazine = Magazine.create("Val Magazine 3", "Tech")
    with pytest.raises(TypeError):
        Article("Valid Title", "Valid Content", "not_an_int", magazine.id) # Not an integer
    with pytest.raises(ValueError):
        Article("Valid Title", "Valid Content", None, magazine.id) # Cannot be None
    with pytest.raises(ValueError):
        Article("Valid Title", "Valid Content", 0, magazine.id) # Must be positive

def test_article_magazine_id_validation(setup_db):
    author = Author.create("Val Author 4")
    magazine = Magazine.create("Val Magazine 4", "Cars")
    with pytest.raises(TypeError):
        Article("Valid Title", "Valid Content", author.id, "not_an_int") # Not an integer
    with pytest.raises(ValueError):
        Article("Valid Title", "Valid Content", author.id, None) # Cannot be None
    with pytest.raises(ValueError):
        Article("Valid Title", "Valid Content", author.id, 0) # Must be positive

def test_article_author_property(setup_db):
    author = Author.create("Property Author")
    magazine = Magazine.create("Prop Mag", "Travel")
    article = Article.create("Prop Article", "Content", author.id, magazine.id)
    retrieved_author = article.author()
    assert retrieved_author.name == "Property Author"
    assert retrieved_author.id == author.id
    assert isinstance(retrieved_author, Author)

def test_article_magazine_property(setup_db):
    author = Author.create("Prop Author 2")
    magazine = Magazine.create("Prop Mag 2", "History")
    article = Article.create("Prop Article 2", "Content 2", author.id, magazine.id)
    retrieved_magazine = article.magazine()
    assert retrieved_magazine.name == "Property Magazine 2"
    assert retrieved_magazine.id == magazine.id
    assert isinstance(retrieved_magazine, Magazine)

def test_article_update(setup_db):
    author = Author.create("Update Author")
    magazine = Magazine.create("Update Magazine", "Gaming")
    article = Article.create("Original Title", "Original Content", author.id, magazine.id)

    article.title = "Updated Title"
    article.content = "Updated Content"

    # Verify in memory
    assert article.title == "Updated Title"
    assert article.content == "Updated Content"

    # Verify in DB
    updated_article = Article.find_by_id(article.id)
    assert updated_article.title == "Updated Title"
    assert updated_article.content == "Updated Content"

def test_article_delete(setup_db):
    author = Author.create("Delete Author")
    magazine = Magazine.create("Delete Magazine", "Cars")
    article = Article.create("Article to Delete", "Content to delete", author.id, magazine.id)

    article_id = article.id
    article.delete()

    assert Article.find_by_id(article_id) is None
    # Ensure it's removed from cache
    assert article_id not in Article._all_articles
