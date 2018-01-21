from flask import Flask, render_template

import utils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog_list():
	posts = utils.get_posts('blog')
	return render_template('blog/list.html', posts=posts)

@app.route('/blog/<file>')
def blog_detail(file):
	post = utils.get_post(file, 'blog')
	return render_template('blog/detail.html', post=post)

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')