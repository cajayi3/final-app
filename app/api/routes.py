from flask import Blueprint, request, jsonify
from models import db, Book, book_schema, books_schema
from flask_login import current_user, login_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return jsonify({})

@api.route('/books', methods = ['POST'])
@login_required
def create_book():
    try:
        data = request.json
        required_fields = ['title', 'author', 'pages', 'cover', 'ISBN_number', 'genre']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            pages=data['pages'],
            ISBN_number=data['ISBN_number'],
            cover=data['cover'],
            genre=data['genre'],
            user_token=current_user.token
        )
        
        db.session.add(book)
        db.session.commit()
        
        books = Book.query.filter_by(user_token=current_user.token).all()
        response = books_schema.dump(books)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/books', methods = ['GET'])
@login_required
def get_book():
    a_user = current_user.token
    books = Book.query.filter_by(user_token = a_user).all()

    print("DEBUG: Book retrieved:", books)

    response = books_schema.dump(books)
    print("DEBUG: Serialized response:", response)

    return jsonify(response)


@api.route('/books/<id>', methods = ['GET'])
@login_required
def get_single_book(id):
    try:
        book = Book.query.get(id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Verify user owns this book
        if book.user_token != current_user.token:
            return jsonify({'error': 'Unauthorized'}), 403
        
        response = book_schema.dump(book)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/books/<id>', methods = ['PUT'])
@login_required
def update_book(id):
    try:
        book = Book.query.get(id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Verify user owns this book
        if book.user_token != current_user.token:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'pages' in data:
            book.pages = data['pages']
        if 'ISBN_number' in data:
            book.ISBN_number = data['ISBN_number']
        if 'genre' in data:
            book.genre = data['genre']
        
        db.session.commit()
        response = book_schema.dump(book)
        return jsonify(response), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api.route('/books/<id>', methods = ['DELETE'])
@login_required
def delete_book(id):
    try:
        book = Book.query.get(id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Verify user owns this book
        if book.user_token != current_user.token:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500