import pytest
import sqlite3
from lib.models.magazine import Magazine
from lib.models.author import Author 
from lib.models.article import Article 
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()
    yield 
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_magazine_creation(setup_db):
    magazine = Magazine("Vogue", "Fashion")
    assert magazine.name == "Vogue"
    assert magazine.category == "Fashion"
    assert magazine.id is None 

def test_magazine_save(setup_db):
    magazine = Magazine("Nat Geographic", "Science") 
    magazine.save()
    assert magazine.id is not None
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine.id,))
    saved_magazine = cursor.fetchone()
    conn.close()
    assert saved_magazine is not None
    assert saved_magazine['name'] == "Nat Geographic" 
    assert saved_magazine['category'] == "Science"

def test_magazine_find_by_id(setup_db):
    magazine = Magazine("TechCrunch", "Technology")
    magazine.save()
    found_magazine = Magazine.find_by_id(magazine.id)
    assert found_magazine is not None
    assert found_magazine.name == "TechCrunch"
    assert found_magazine.id == magazine.id

def test_magazine_find_by_id_not_found(setup_db):
    assert Magazine.find_by_id(999) is None

def test_magazine_find_by_name(setup_db):
    magazine = Magazine("Sports Illus", "Sports") 
    magazine.save()
    found_magazine = Magazine.find_by_name("Sports Illus")
    assert found_magazine is not None
    assert found_magazine.name == "Sports Illus" 
    assert found_magazine.id == magazine.id

def test_magazine_find_by_name_not_found(setup_db):
    assert Magazine.find_by_name("NonExistent Magazine") is None

def test_magazine_get_all(setup_db):
    mag1 = Magazine("Mag A", "Cat A")
    mag1.save()
    mag2 = Magazine("Mag B", "Cat B")
    mag2.save()
    all_magazines = Magazine.get_all()
    assert len(all_magazines) == 2
    assert any(m.name == "Mag A" for m in all_magazines)
    assert any(m.name == "Mag B" for m in all_magazines)

def test_magazine_name_validation(setup_db):
    with pytest.raises(ValueError):
        Magazine("A", "Category") 
    with pytest.raises(ValueError):
        Magazine("", "Category") 
    with pytest.raises(ValueError):
        Magazine("This Name Is Way Too Long", "Category") 
    with pytest.raises(TypeError):
        Magazine(123, "Category") 

def test_magazine_category_validation(setup_db):
    with pytest.raises(ValueError):
        Magazine("Valid Name", "") 
    with pytest.raises(TypeError):
        Magazine("Valid Name", 123)

def test_magazine_name_update(setup_db):
    magazine = Magazine("Old Mag Name", "Old Cat")
    magazine.save()
    magazine.name = "New Mag Name"
    assert magazine.name == "New Mag Name"
    updated_magazine = Magazine.find_by_id(magazine.id)
    assert updated_magazine.name == "New Mag Name"

def test_magazine_category_update(setup_db):
    magazine = Magazine("Mag Name", "Old Cat")
    magazine.save()
    magazine.category = "New Cat"
    assert magazine.category == "New Cat"
    updated_magazine = Magazine.find_by_id(magazine.id)
    assert updated_magazine.category == "New Cat"

def test_magazine_delete(setup_db):
    magazine = Magazine("Mag to Delete", "Category")
    magazine.save()
    magazine_id = magazine.id
    magazine.delete()
    assert Magazine.find_by_id(magazine_id) is None
    
    assert magazine_id not in Magazine._all_magazines

def test_magazine_articles(setup_db):
    author = Author.create("Test Author for Mag Articles")
    magazine = Magazine.create("Test Mag Arts", "Tech") 

    article1 = Article.create("Mag Article 1", "Content 1", author.id, magazine.id)
    article2 = Article.create("Mag Article 2", "Content 2", author.id, magazine.id)

    magazine_articles = magazine.articles()
    assert len(magazine_articles) == 2
    assert any(a.title == "Mag Article 1" for a in magazine_articles)
    assert any(a.title == "Mag Article 2" for a in magazine_articles)
    assert all(isinstance(a, Article) for a in magazine_articles)

def test_magazine_authors(setup_db):
    author1 = Author.create("Author 1 for Magazine")
    author2 = Author.create("Author 2 for Magazine")
    author3 = Author.create("Author 3 for Magazine") 
    magazine = Magazine.create("Test Mag Auth", "Tech") 

    Article.create("Article A", "Content A", author1.id, magazine.id)
    Article.create("Article B", "Content B", author2.id, magazine.id)
    Article.create("Article C", "Content C", author1.id, magazine.id) 

    magazine_authors = magazine.authors()
    assert len(magazine_authors) == 2
    assert any(a.name == "Author 1 for Magazine" for a in magazine_authors)
    assert any(a.name == "Author 2 for Magazine" for a in magazine_authors)
    assert not any(a.name == "Author 3 for Magazine" for a in magazine_authors)
    assert all(isinstance(a, Author) for a in magazine_authors)

def test_magazine_article_titles(setup_db):
    author = Author.create("Test Author for Titles")
    magazine = Magazine.create("Test Mag Titles", "Tech") 

    Article.create("Title One", "Content 1", author.id, magazine.id)
    Article.create("Title Two", "Content 2", author.id, magazine.id)
    Article.create("Title Three", "Content 3", author.id, magazine.id)

    titles = magazine.article_titles()
    assert sorted(titles) == sorted(["Title One", "Title Two", "Title Three"])
    assert len(titles) == 3

def test_magazine_contributing_authors(setup_db):
    author1 = Author.create("Contributor 1")
    author2 = Author.create("Contributor 2")
    author3 = Author.create("Contributor 3")
    
    magazine = Magazine.create("Contr. Mag", "Tech")
    
    # Author 1: 3 articles (should be contributing)
    Article.create("Art 1-1", "Cont", author1.id, magazine.id)
    Article.create("Art 1-2", "Cont", author1.id, magazine.id)
    Article.create("Art 1-3", "Cont", author1.id, magazine.id)
    
    # Author 2: 2 articles (should NOT be contributing)
    Article.create("Art 2-1", "Cont", author2.id, magazine.id)
    Article.create("Art 2-2", "Cont", author2.id, magazine.id)

    # Author 3: 1 article (should NOT be contributing)
    Article.create("Art 3-1", "Cont", author3.id, magazine.id)

    contributing = magazine.contributing_authors()
    assert len(contributing) == 1
    assert contributing[0].name == "Contributor 1"
    assert isinstance(contributing[0], Author)

    # Test case: No contributing authors
    magazine_no_contributors = Magazine.create("No Contr. Mag", "Science")
    author_only_one = Author.create("Only One Article")
    Article.create("One Article", "Content", author_only_one.id, magazine_no_contributors.id)
    
    assert magazine_no_contributors.contributing_authors() is None