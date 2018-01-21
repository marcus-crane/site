import mistune
import mistune_contrib.meta as meta
import os

def get_post(filename, dir):
	def render_md(file):
		data = meta.parse(file)
		post = {}
		post['title'] = data[0]['Title']
		post['date'] = data[0]['Date']
		post['content'] = mistune.markdown(data[1])
		return post

	with open('posts/{}/{}.md'.format(dir, filename), 'r') as file:
		post = file.read()
		return render_md(post)

def get_posts(dir):
	path = os.listdir('posts/{}'.format(dir))
	posts = []
	urls = [post[:-3] for post in path]
	for url in urls:
		post = {}
		post['title'] = url.replace('-', ' ')
		post['slug'] = url
		posts.append(post)
	return posts