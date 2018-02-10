import couchdb
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import mistune_contrib.meta as meta
import PyRSS2Gen

from datetime import datetime
import re
import os

class PostRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(mistune.escape(code))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

    def block_quote(self, text):
        # Hideous code -> swap text split for just regex and clean up
        contents = text.split('<br>\n[')
        quote = re.compile("<p>(.|[\n])*\[").match(text).group(0)[:-1]
        author = contents[1].split(']</p>\n')[0]
        return '''
        <blockquote class="athelas ml0 mt0 pl4 black-90 bl bw2 b--blue">
            <p class="f5 f4-m f3-l lh-copy measure mt0">
                {0}
            </p>
            <cite class="f6 ttu tracked fs-normal">― {1}</cite>
        </blockquote>
        '''.format(quote, author)

renderer = PostRenderer(escape=True, hard_wrap=True)
markdown = mistune.Markdown(renderer=renderer)

def get_post(filename, directory):
    def render_md(post_file):
        data = meta.parse(post_file)
        content = markdown(data[1])
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
                pubDate=datetime.strptime(item['date'], '%B %d, %Y')
            )
        )
    rss = PyRSS2Gen.RSS2(
        title='Things I Made',
        link='https://thingsima.de/blog/',
        description='Writing about things I find interesting!',
        lastBuildDate=datetime.now(),
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
