import pytest
import sqlite3
from lib.models.author import Author
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
    # Teardown: Clean up after each test if necessary (optional for simple cases)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()


def test_author_creation(setup_db):
    author = Author("J.K. Rowling")
    assert author.name == "J.K. Rowling"
    assert author.id is None # ID should be None before saving

def test_author_save(setup_db):
    author = Author("Stephen King")
    author.save()
    assert author.id is not None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (author.id,))
    saved_author = cursor.fetchone()
    conn.close()
    assert saved_author is not None
    assert saved_author['name'] == "Stephen King"

def test_author_find_by_id(setup_db):
    author = Author("Agatha Christie")
    author.save()
    found_author = Author.find_by_id(author.id)
    assert found_author is not None
    assert found_author.name == "Agatha Christie"
    assert found_author.id == author.id

def test_author_find_by_id_not_found(setup_db):
    assert Author.find_by_id(999) is None

def test_author_find_by_name(setup_db):
    author = Author("George Orwell")
    author.save()
    found_author = Author.find_by_name("George Orwell")
    assert found_author is not None
    assert found_author.name == "George Orwell"
    assert found_author.id == author.id

def test_author_find_by_name_not_found(setup_db):
    assert Author.find_by_name("NonExistent Author") is None

def test_author_get_all(setup_db):
    author1 = Author("Author A")
    author1.save()
    author2 = Author("Author B")
    author2.save()
    all_authors = Author.get_all()
    assert len(all_authors) == 2
    assert any(a.name == "Author A" for a in all_authors)
    assert any(a.name == "Author B" for a in all_authors)

def test_author_name_validation(setup_db):
    with pytest.raises(ValueError):
        Author("") # Too short
    with pytest.raises(ValueError):
        Author("A") # Too short
    with pytest.raises(ValueError):
        Author("This name is way too long for the author validation") # Too long
    with pytest.raises(TypeError):
        Author(123) # Not a string

def test_author_name_update(setup_db):
    author = Author("Old Name")
    author.save()
    author.name = "New Name"
    assert author.name == "New Name"
    updated_author = Author.find_by_id(author.id)
    assert updated_author.name == "New Name"

def test_author_delete(setup_db):
    author = Author("Author to Delete")
    author.save()
    author_id = author.id
    author.delete()
    assert Author.find_by_id(author_id) is None
    # Ensure it's removed from cache
    assert author_id not in Author._all_authors

def test_author_articles(setup_db):
    from lib.models.magazine import Magazine
    from lib.models.article import Article

    author = Author.create("Test Author For Articles")
    magazine1 = Magazine.create("Test Mag 1", "Tech")
    magazine2 = Magazine.create("Test Mag 2", "Fashion")

    article1 = Article.create("Title 1", "Content 1", author.id, magazine1.id)
    article2 = Article.create("Title 2", "Content 2", author.id, magazine2.id)

    author_articles = author.articles()
    assert len(author_articles) == 2
    assert any(a.title == "Title 1" for a in author_articles)
    assert any(a.title == "Title 2" for a in author_articles)

def test_author_magazines(setup_db):
    from lib.models.magazine import Magazine
    from lib.models.article import Article

    author = Author.create("Test Author For Magazines")
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Fashion Weekly", "Fashion")
    magazine3 = Magazine.create("Tech Weekly", "Technology") # Same category, different mag

    Article.create("Article 1", "Content 1", author.id, magazine1.id)
    Article.create("Article 2", "Content 2", author.id, magazine2.id)
    Article.create("Article 3", "Content 3", author.id, magazine3.id)


    author_magazines = author.magazines()
    assert len(author_magazines) == 3 # Should get 3 distinct magazines
    assert any(m.name == "Tech Today" for m in author_magazines)
    assert any(m.name == "Fashion Weekly" for m in author_magazines)
    assert any(m.name == "Tech Weekly" for m in author_magazines)
    # Check that they are Magazine objects
    assert all(isinstance(m, Magazine) for m in author_magazines)

def test_author_topic_areas(setup_db):
    from lib.models.magazine import Magazine
    from lib.models.article import Article

    author = Author.create("Test Author For Topics")
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Fashion Weekly", "Fashion")
    magazine3 = Magazine.create("Science Monthly", "Science")
    magazine4 = Magazine.create("Gaming News", "Entertainment")
    magazine5 = Magazine.create("Another Tech Mag", "Technology") # Duplicate category

    Article.create("Article 1", "Content 1", author.id, magazine1.id) # Technology
    Article.create("Article 2", "Content 2", author.id, magazine2.id) # Fashion
    Article.create("Article 3", "Content 3", author.id, magazine3.id) # Science
    Article.create("Article 4", "Content 4", author.id, magazine5.id) # Technology (duplicate)

    topic_areas = author.topic_areas()
    assert sorted(topic_areas) == sorted(["Technology", "Fashion", "Science"])
    assert len(topic_areas) == 3 # Should return unique topics

    # Test with no articles
    author_no_articles = Author.create("No Articles Author")
    assert author_no_articles.topic_areas() == []
