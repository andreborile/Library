import sqlite3

connection = sqlite3.connect('books.sqlite')

cursor = connection.cursor()

sql_query = """ CREATE TABLE IF NOT EXISTS books (
    id integer PRIMARY KEY,
    author text NOT NULL,
    country text NOT NULL,
    language text NOT NULL,
    pages integer NOT NULL,
    title text NOT NULL,
    year integer NOT NULL
) """

cursor.execute(sql_query)