--lib/db/schema.sql
-- Drop tables if they exist to allow for clean re-creation during development.
-- Order matters: tables with foreign keys must be dropped first.
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;

--Create the authors table
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-increments for new authors
    name VARCHAR(255) NOT NULL  -- Author's name cannot be empty
);
-- Create the magazines table
CREATE TABLE IF NOT EXISTS magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-increments for new magazines
    name VARCHAR(255) NOT NULL,  -- Magazine's name cannot be empty
    category VARCHAR(255) NOT NULL  -- Magazine's category cannot be empty
);
-- Create the articles table, linking to authors and magazines
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-increments for new articles
    title VARCHAR(255) NOT NULL,  -- Article's title cannot be empty
    author_id INTEGER,  -- Foreign key to authors table
    magazine_id INTEGER,  -- Foreign key to magazines table
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,  -- Deletes articles if the author is deleted
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE  -- Deletes articles if the magazine is deleted
);