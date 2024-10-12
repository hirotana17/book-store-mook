from flask import Blueprint, request, jsonify

from models import Book, db

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/book')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    all_books = Book.query.all()
    result = [book.serialize() for book in all_books]
    response = {"result": result}
    return jsonify(response)


@book_blueprint.route('/create', methods=['POST'])
def create_book():
    try:
        book = Book()
        book.name = request.form['name']
        book.slug = request.form['slug']
        book.image = request.form['image']
        book.price = request.form['price']

        db.session.add(book)
        db.session.commit()

        response = {'Message': 'Book Create', 'result': book.serialize()}
    except Exception as e:
        print(str(e))
        response = {'message': 'Book creation failed'}

    return jsonify(response)


@book_blueprint.route('/<slug>', methods=['GET'])
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first()

    if book:
        response = {'result': book.serialize()}
    else:
        response = {'message': 'No books found'}

    return jsonify(response)


@book_blueprint.route('/<book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        if 'name' in request.form:
            book.name = request.form['name']
        if 'slug' in request.form:
            book.slug = request.form['slug']
        if 'image' in request.form:
            book.image = request.form['image']
        if 'price' in request.form:
            book.price = request.form['price']

        db.session.commit()

        response = {'message': 'Book updated', 'result': book.serialize()}
        return jsonify(response), 200
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return jsonify({'message': 'Book updated failed'}), 500