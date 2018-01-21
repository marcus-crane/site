import mistune
import mistune_contrib.meta as meta

def fetch_post(filename):
	with open('{}.md'.format(filename), 'r') as file:
		post = file.read()
		return render_md(post)

def render_md(file):
	data = meta.parse(file)
	post = {}
	
	post['title'] = data[0]['Title']
	post['date'] = data[0]['Date']
	post['content'] = mistune.markdown(data[1])

	return post