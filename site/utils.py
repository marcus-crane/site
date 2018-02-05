import couchdb
import mistune
import mistune_contrib.meta as meta
import PyRSS2Gen

import datetime
import os


def get_post(filename, directory):
    def render_md(post_file):
        data = meta.parse(post_file)
        content = mistune.markdown(data[1], escape=False)
        post_data = dict(title=data[0]['Title'], date=data[0]['Date'],
                         sfw=data[0]['SFW'], content=content)
        return post_data

    with open('posts/{}/{}.md'.format(directory, filename), 'r') as file:
        post = file.read()
        return render_md(post)


def get_posts(directory):
    path = os.listdir('posts/{}'.format(directory))
    posts = []
    # Remove the '.md' bit from the end of each file
    urls = [post[:-3] for post in path]
    for url in urls:
        post = {'title': url.replace('-', ' '), 'slug': url}
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
                title=item['title'],
                link='https://thingsima.de/blog/{}'.format(slug),
                description=item['content'],
                guid='https://thingsima.de/blog/{}'.format(slug),
                pubDate=datetime.datetime(2003, 9, 6, 12, 00)))
    rss = PyRSS2Gen.RSS2(
        title='Things I Made',
        link='https://thingsima.de/blog/',
        description='Writing about things I find interesting!',
        lastBuildDate=datetime.datetime.now(),
        items=entries)
    rss.write_xml(open('static/rss.xml', 'w'))


def load_stats(media_type, limit=None):
    couch = couchdb.Server('http://couchdb:5984/')
    media = couch[media_type]
    items = []

    for item in media:
        items.append(media[item])

    if limit:
        return items[:limit]
    else:
        return items
