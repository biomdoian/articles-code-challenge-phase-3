import random
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()

    print("Clearing existing data...")
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    print("Existing data cleared.")

    #create authors
    print("Creating authors...")
    author1 = Author.create("Biomdo Ian")
    author2 = Author.create("Mary Muthoni")
    author3 = Author.create("George Mungai")
    author4 = Author.create("Tracy Chemutai")
    author5 = Author.create("Josiah Mwalimu")
    authors = [author1, author2, author3, author4, author5]
    print(f"Created {len(authors)}authors.")

    #create magazines
    print("Creating magazines...")
    mag1 = Magazine.create("Tech Today", "Technology")
    mag2 = Magazine.create("Health Weekly", "Health")
    mag3 = Magazine.create("Travel Explorer", "Travel")
    mag4 = Magazine.create("Football Mag", "Soccer")
    mag5 = Magazine.create("Cars Daily", "Luxury")
    mags = [mag1, mag2, mag3, mag4, mag5]
    print(f"Created {len(mags)} magazines.")

    #create articles
    print("Creating articles...")
    titles = [
        "The Future of AI", "Quantum Computing Explained", "New Fashion Trends",
        "Exploring Ancient Ruins", "Top 10 Video Games",
        "Space Tourism Boom", "Sustainable Living Tips", "Blockchain Beyond Crypto",
        "Ethical AI Dev", "Smart Home Gadgets", "Culinary Delights", 
        "Vintage Wheels", "Hidden Gems Asia", 
        "Next-Gen Consoles Review", "Mind-Bending Physics", "Art of Scoring",
        "Healthy Eating Habits", "The Rise of Football", "Cyber Threats", 
        "Ocean Conservation", "Digital Art Revolution", "Classic Lit" 
    ]
    contents = [
        "An in-depth look at...", "Discover the secrets of...", "Tips and tricks for...",
        "A comprehensive guide to...", "Exploring the depths of..."
    ]
   # Author 1 writes 3 articles for Magazine 1
    Article.create(random.choice(titles), random.choice(contents), author1.id, mag1.id)
    Article.create(random.choice(titles), random.choice(contents), author1.id, mag1.id)
    Article.create(random.choice(titles), random.choice(contents), author1.id, mag1.id)
   
    # Author 2 writes 3 articles for Magazine 2
    Article.create(random.choice(titles), random.choice(contents), author2.id, mag2.id)
    Article.create(random.choice(titles), random.choice(contents), author2.id, mag2.id)
    Article.create(random.choice(titles), random.choice(contents), author2.id, mag2.id)
    
     # Author 3 writes 3 articles for Magazine 3
    Article.create(random.choice(titles), random.choice(contents), author3.id, mag3.id)
    Article.create(random.choice(titles), random.choice(contents), author3.id, mag3.id)
    Article.create(random.choice(titles), random.choice(contents), author3.id, mag3.id)

    # Author 4 writes 3 articles for Magazine 4
    Article.create(random.choice(titles), random.choice(contents), author4.id, mag4.id)
    Article.create(random.choice(titles), random.choice(contents), author4.id, mag4.id)
    Article.create(random.choice(titles), random.choice(contents), author4.id, mag4.id)

    # Author 5 writes 3 articles for Magazine 5
    Article.create(random.choice(titles), random.choice(contents), author5.id, mag5.id)
    Article.create(random.choice(titles), random.choice(contents), author5.id, mag5.id)
    Article.create(random.choice(titles), random.choice(contents), author5.id, mag5.id)

    # Creates many more random articles
    num_articles = 50 
    created_articles_count = 0
    for _ in range(num_articles):
        try:
            author = random.choice(authors)
            magazine = random.choice(mags)
            title = random.choice(titles)
            content = random.choice(contents)
            Article.create(title, content, author.id, magazine.id)
            created_articles_count += 1
        except Exception as e:
            print(f"Error creating article: {e}")
    print(f"Created {created_articles_count} articles.")

    conn.close()
    print("\nDatabase seeding complete!")

if __name__ == '__main__':
    seed_database()