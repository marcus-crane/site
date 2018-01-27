from classes import Book
import settings

import mistune
import mistune_contrib.meta as meta
import requests

import json
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

def update_books():
    def query_goodreads():
        url = ('https://www.goodreads.com/review/list?'
               'shelf=currently-reading&key={0}&id={1}'
               'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
        r = requests.get(url, headers=settings.USER_AGENT)
        return r.text

    def fetch_titles(books):
        titles = []
        for book in books:
            name = book[6].text
            image = book[7].text
            link = book[10].text
            author = book[21][0][1].text
            
            entry = Book(name, image, link, author)
            entry = entry.export()
            titles.append(entry)
        return titles

    if os.path.exists('data/books.json'):
        os.remove('data/books.json')
    data = query_goodreads()
    root = ET.fromstring(data)
    currently_reading = fetch_titles(root[1])
    with open('data/books.json', 'w') as f:
        json.dump(currently_reading, f, indent=2)