# Phase 3 Code Challenge: Articles

This project implements a system to model the relationship between Authors, Articles, and Magazines, with data persisted in a SQL database (SQLite).

## Problem Domain:
- An `Author` can write many `Articles`
- A `Magazine` can publish many `Articles`
- An `Article` belongs to both an `Author` and a `Magazine`
- The `Author-Magazine` relationship is many-to-many

## Setup Instructions

1.  **Clone the repository:**
    `git clone <your-repo-url>`
    `cd code-challenge`

2.  **Install dependencies (using Pipenv):**
    `pipenv install pytest sqlite3`

3.  **Activate the virtual environment:**
    `pipenv shell`

4.  **Set up the database:**
    `python scripts/setup_db.py`

5.  **Seed the database with sample data:**
    `python lib/db/seed.py`

## Project Structure
code-challenge/
├── lib/
│   ├── models/
│   │   ├── author.py
│   │   ├── article.py
│   │   └── magazine.py
│   ├── db/
│   │   ├── connection.py
│   │   ├── seed.py
│   │   └── schema.sql
│   ├── debug.py
│   └── __init__.py
├── tests/
│   ├── test_author.py
│   ├── test_article.py
│   └── test_magazine.py
├── scripts/
│   ├── setup_db.py
│   └── run_queries.py
└── README.md

## Running Tests

From the root directory of the project:
`pytest`

## Debugging

From the root directory of the project, activate your pipenv shell and then run:
`python lib/debug.py`