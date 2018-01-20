from flask import Flask, render_template

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

@app.route('/contact')
def contact():
	return render_template('contact.html')
