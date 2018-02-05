import couchdb
import mistune
import mistune_contrib.meta as meta
import PyRSS2Gen

import datetime
import os

def get_post(filename, dir):
    def render_md(file):
        data = meta.parse(file)
        post = {}
        post['title'] = data[0]['Title']
        post['date'] = data[0]['Date']
        post['sfw'] = data[0]['SFW']
        post['content'] = mistune.markdown(data[1], escape=False)
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

def generate_rss(section):
    posts = get_posts(section)
    entries = []
    for post in posts:
        slug = post['slug']
        item = get_post(slug, section)
        entries.append(
            PyRSS2Gen.RSSItem(
                title = item['title'],
                link = 'https://thingsima.de/blog/{}'.format(slug),
                description = item['content'],
                guid = 'https://thingsima.de/blog/{}'.format(slug),
                pubDate = datetime.datetime(2003, 9, 6, 12, 00)))
    rss = PyRSS2Gen.RSS2(
        title = 'Things I Made',
        link = 'https://thingsima.de/blog/',
        description = 'Writing about things I find interesting!',
        lastBuildDate = datetime.datetime.now(),
        items = entries)
    rss.write_xml(open('static/rss.xml', 'w'))

def load_stats(type, limit=None):
    couch = couchdb.Server('http://couchdb:5984/')
    media = couch[type]
    items = []

    for item in media:
        items.append(media[item])

    if limit:
        return items[:limit]
    else:
        return items
