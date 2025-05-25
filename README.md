# Articles Code Challenge - Phase 3

## Project Overview

This project implements a robust backend system for managing articles, authors, and magazines using Python and SQLite. It demonstrates key Object-Relational Mapping (ORM) concepts, including:

* One-to-many and many-to-many relationships
* Data validation to ensure data integrity
* Clean Python class design
* Seamless database interaction with SQLite

This challenge focused on building out the core models and their relationships, tested with a provided `pytest` suite.

## Features

The implemented models provide the following functionalities:

### Article Model

* **Initialization & Persistence:** Create, save, find, and delete articles in the database.
* **Data Validation:**
    * `title`: Must be a string between 5 and 50 characters (inclusive).
    * `content`: Must be a non-empty string.
    * `author_id` and `magazine_id`: Must be positive integers.
* **Relationships:**
    * `.author()`: Returns the `Author` instance associated with the article.
    * `.magazine()`: Returns the `Magazine` instance associated with the article.

### Author Model

* **Initialization & Persistence:** Create, save, find, and delete authors.
* **Data Validation:**
    * `name`: Must be a string between 2 and 50 characters (inclusive).
* **Relationships:**
    * `.articles()`: Returns a list of all `Article` instances written by the author.
    * `.magazines()`: Returns a list of all `Magazine` instances the author has contributed to.
    * `.topic_areas()`: Returns a list of unique categories of magazines the author has written for.

### Magazine Model

* **Initialization & Persistence:** Create, save, find, and delete magazines.
* **Data Validation:**
    * `name`: Must be a string between 2 and 16 characters (inclusive).
    * `category`: Must be a non-empty string.
* **Relationships & Aggregations:**
    * `.articles()`: Returns a list of all `Article` instances published in the magazine.
    * `.authors()`: Returns a list of all `Author` instances who have written for the magazine.
    * `.article_titles()`: Returns a list of titles of all articles published in the magazine.
    * `.contributing_authors()`: Returns a list of `Author` instances who have written **3 or more articles** for that specific magazine. Returns `None` if no such authors exist.

## Technologies Used

* **Python 3.8.13**
* **SQLite3**
* **Pipenv** (for dependency & environment management)
* **Pytest** (for running tests)

## Setup and Installation

Follow these steps to get the project up and running on your local machine:

* `Clone the Repository`
Bash

git clone <your-repository-url>
cd articles-code-challenge-phase-3
(Replace <your-repository-url> with the actual URL of your Git repository.)

* `Install Dependencies`
Make sure you have Pipenv installed. If not, install it globally:

Bash

pip install pipenv
Then, install the project dependencies:

Bash

pipenv install
* `Activate the Virtual Environment`
Bash

pipenv shell
Your terminal prompt should change to something like: (articles-code-challenge-phase-3), indicating you're in the virtual environment.

* `Set Up the Database`
Run the following commands to create tables and seed initial data:

Bash

python lib/db/create_tables.py
python lib/db/seed.py
Running Tests
Run the complete test suite to verify everything works:

Bash

* `pytest`
You should see output indicating "43 passed in X.XXs":

================================= 43 passed in X.XXs =================================
* That means all features are implemented correctly!

Using the Models Interactively
After setup, you can experiment with your models directly in a Python shell:

Activate the shell:

Bash

pipenv shell
Start Python:

Bash

python
Sample Interaction:

Python

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Create records
author = Author.create("Biomdo Ian")
magazine = Magazine.create("Tech Today", "Technology")

# Create articles
article1 = Article.create("Python Tips", "Learn advanced Python.", author.id, magazine.id)
article2 = Article.create("Django Basics", "Web development with Django.", author.id, magazine.id)

# Explore relationships
print(author.articles())
print(magazine.authors())
print(magazine.article_titles())
print(magazine.contributing_authors())


# Author
Biomdo Ian