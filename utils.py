from classes import Book
import settings

import mistune
import mistune_contrib.meta as meta
import requests

import os
import xml.etree.ElementTree as ET

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
    # Remove the '.md' bit from the end of each file
	urls = [post[:-3] for post in path]
	for url in urls:
		post = {}
		post['title'] = url.replace('-', ' ')
		post['slug'] = url
		posts.append(post)
	return posts

def update_books(key):
    def query_goodreads(key):
        url = ('https://www.goodreads.com/review/list?key={}'
               '&v%3D2&shelf=currently-reading'.format(key))
        r = requests.get(url, headers=settings.USER_AGENT)
        return r.text

    def save_titles(books):
        for book in books:
            title = book[6].text
            cover = book[7].text
            link = book[10].text
            overview = book[20].text
            author = book[21][0][1].text
            
            entry = Book(title=title, cover=cover, link=link,
                         overview=overview, author=author)
            entry.save()
            print('Saved {}'.format(title))

    if os.path.exists('data/books.json'):
        os.remove('data/books.json')
    data = query_goodreads(key)
    root = ET.fromstring(data)
    save_titles(root[1])