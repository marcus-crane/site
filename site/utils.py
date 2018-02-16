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

    def pull_attribution(self, lines):
        print(lines)
        quote = {}
        # Cuts out the starting <p> tag
        if '~' in lines[-1:][0]:
            # Selects between the ~ and the left over </p> tag
            quote['author'] = lines[-1:][0][2:-4]
        else:
            quote['author'] = None
        if quote['author'] is None:
            quote['text'] = '\n'.join(lines)[3:-4]
        else:
            quote['text'] = '\n'.join(lines[:-1])[3:]
        return quote

    def block_quote(self, text):
        # Hideous code -> swap text split for just regex and clean up
        contents = text.split('\n')[:-1]
        quote = self.pull_attribution(contents)
        html = self.build_quote(quote)
        return html

    def build_quote(self, quote):
        html = ''
        text_html = '''
        <p class="f5 f4-m f3-l lh-copy measure mt0">
            {}
        </p>
        '''.format(quote['text'])
        html = html + text_html

        if quote['author'] is not None:
            author_html = '''
            <cite class="f6 ttu tracked fs-normal">
                ― {}
            </cite>
            '''.format(quote['author'])
            html = html + author_html

        blockquote = '''
        <blockquote class="athelas ml0 mt0 pl4 black-90 bl bw2 b--blue">
            {}
        </blockquote>
        '''.format(html)
        return blockquote

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
