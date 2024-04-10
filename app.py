from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample books data
books_data = [
    { 'id': 1, 'title': 'Book 1', 'author': 'Author 1', 'category': 'Category 1' },
    { 'id': 2, 'title': 'Book 2', 'author': 'Author 2', 'category': 'Category 2' }
]

# Home route
@app.route('/')
def home():
    return render_template('index.html', content='<h2>Welcome to our Library</h2><p>This is a simple Library Management System website.</p>')

# Books route
@app.route('/books')
def books():
    return render_template('index.html', content=render_books_table())

# Add Book route
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        new_book = { 'id': len(books_data) + 1, 'title': title, 'author': author, 'category': category }
        books_data.append(new_book)
        return redirect(url_for('books'))
    return render_template('index.html', content=render_add_book_form())

# Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term'].lower()
        search_results = [book for book in books_data if search_term in book['title'].lower() or search_term in book['author'].lower()]
        return render_template('index.html', content=render_search_results(search_results))
    return render_template('index.html', content=render_search_form())

# Helper functions to render HTML content
def render_books_table():
    html_content = '<h2>List of Books</h2><table><thead><tr><th>Book ID</th><th>Title</th><th>Author</th><th>Category</th></tr></thead><tbody>'
    for book in books_data:
        html_content += f'<tr><td>{book["id"]}</td><td>{book["title"]}</td><td>{book["author"]}</td><td>{book["category"]}</td></tr>'
    html_content += '</tbody></table>'
    return html_content

def render_add_book_form():
    return '<h2>Add New Book</h2><form action="/add_book" method="post"><label for="title">Title:</label><br><input type="text" id="title" name="title" required><br><label for="author">Author:</label><br><input type="text" id="author" name="author" required><br><label for="category">Category:</label><br><input type="text" id="category" name="category" required><br><br><input type="submit" value="Add Book" class="button"></form>'

def render_search_form():
    return '<h2>Search for a Book</h2><form action="/search" method="post"><input type="text" id="search_term" name="search_term" placeholder="Enter book title or author..."><input type="submit" value="Search" class="button"></form>'

def render_search_results(search_results):
    html_content = '<h2>Search Results</h2>'
    if search_results:
        html_content += '<ul>'
        for book in search_results:
            html_content += f'<li>{book["title"]} by {book["author"]}</li>'
        html_content += '</ul>'
    else:
        html_content += '<p>No results found.</p>'
    return html_content

if __name__ == '__main__':
    app.run(debug=True)

