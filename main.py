from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.json.sort_keys = False

# estabelecendo conexao com database
def db_connection():
    connection = None
    try:
        connection = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return connection

# definindo metodos get e post no endpoint "/books"
@app.route('/books', methods=['GET', 'POST'])
def books():
    connection = db_connection()
    cursor = connection.cursor()

    if request.method == 'GET':
        cursor = connection.execute("SELECT * FROM books")
        books = [
            dict(id=row[0], author=row[1], country=row[2], language=row[3], pages=row[4], title=row[5], year=row[6])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
        
    if request.method == 'POST':
        new_author = request.json['author']
        new_country = request.json['country']
        new_language = request.json['language']
        new_pages = request.json['pages']
        new_title = request.json['title']
        new_year = request.json['year']

        sql = """ INSERT INTO books (author, country, language, pages, title, year)
            VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql, (new_author, new_country, new_language, new_pages, new_title, new_year))
        connection.commit()
        return f'Book with the id: {cursor.lastrowid} created sucessfully.'

# definindo metodos get e post no endpoint "/books/<int:id>"
@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    connection = db_connection()
    cursor = connection.cursor()
    book = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
            if book is not None:
                return jsonify(book), 201
            else:
                return "Something wrong", 404
            
    if request.method == 'PUT':
            sql = """ UPDATE books
            SET
                author = ?,
                country = ?,
                language = ?, 
                pages = ?, 
                title = ?, 
                year = ?
            WHERE id = ? """

            author = request.json['author'] 
            country = request.json['country'] 
            language = request.json['language'] 
            pages = request.json['pages'] 
            title = request.json['title'] 
            year = request.json['year']

            updated_book = {
                'id': id,
                'author': author, 
                'country': country, 
                'language': language, 
                'pages': pages, 
                'title': title, 
                'year': year 
            }

            cursor.execute(sql, (author, country, language, pages, title, year, id))
            connection.commit()
            
            return jsonify(updated_book), 201
            
    if request.method == 'DELETE':
        sql = """ DELETE FROM books WHERE id=?"""
        cursor.execute(sql, (id,))
        connection.commit()
        return f'The book with id: {id} has been deleted.', 201

app.run(debug=True)