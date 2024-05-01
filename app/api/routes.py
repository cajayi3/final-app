from flask import Blueprint, request, jsonify, render_template
from ..helpers import token_required
from ..models import db, Book, books_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {''}

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    pages = request.json['pages']
    cover = request.json['cover']
    ISBN_number = request.json['ISBN_number']
    genre = request.json['genre']
    user_token = user_token.token

    print(f'TEST: {current_user_token.token}')

    book = Book(title, author, pages, cover, ISBN_number, genre, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book.schema.dump(book)
    return jsonify(response)


@api.route('/books', methods = ['GET']) 
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)


@api.route('books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book =  Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.pages = request.json['pages']
    book.cover = request.json['cover']
    book.ISBN_number = request.json['ISBN_number']
    book.genre = request.json['genre']
    book.user_token = current_user_token.token

    db.session.commit()
    response = books_schema.dump(book)
    return jsonify(response)


@api.route('books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book =  Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = books_schema.dump(book)
    return jsonify(response)