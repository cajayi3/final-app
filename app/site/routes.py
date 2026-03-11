from flask import Blueprint, render_template, request

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/books')
def books():
    return render_template('books.html')

@site.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    return render_template('search_results.html', query=query)