from flask import Flask, render_template

from utils import fetch_post

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog_list():
	posts = [
		{ 'title': 'Testing', 'slug': 'testing' }
	]
	return render_template('blog/list.html', posts=posts)

@app.route('/blog/<file>')
def blog_detail(file):
	post = fetch_post(file)
	return render_template('blog/detail.html', post=post)

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')