from flask import Flask, render_template

import json
from utils import get_post, get_posts, load_stats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog_list():
	posts = get_posts('blog')
	return render_template('blog/list.html', posts=posts)

@app.route('/blog/<file>')
def blog_detail(file):
	post = get_post(file, 'blog')
	return render_template('blog/detail.html', post=post)

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/stats')
def stats():
    books = load_stats('books')
    movies = load_stats('movies', 5)
    music = load_stats('music', 5)
    shows = load_stats('shows', 5)
    return render_template('stats.html', books=books, movies=movies,
        music=music, shows=shows)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
