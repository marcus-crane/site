from flask import Flask, render_template
import mistletoe

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

@app.route('/blog/test')
def blog_detail():
	with open('test.md', 'r') as post:
		render = mistletoe.markdown(post)
		print(render)
	return render_template('blog/detail.html', post=render)

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')