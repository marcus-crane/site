import datetime
import re

from django.db import models
from django.utils.text import slugify
import mistune
import mistune_contrib.meta as meta
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class Post(models.Model):
    POST_STATUS = (
        ('D', u'✍︎ Draft'),
        ('U', u'⏏︎ Unlisted'),
        ('P', u'✔ Published'),
    )
    title = models.CharField("Post title", max_length=200)
    slug = models.SlugField("Slug", max_length=40, blank=True, unique=True)
    sfw = models.BooleanField("Safe for work?", default=True)
    text = models.TextField("Post content")
    head = models.TextField("CSS/JS to include in the <head> of this post", blank=True)
    foot = models.TextField("CSS/JS to include in the bottom of this post", blank=True)
    created_at = models.DateTimeField("First created")
    published_at = models.DateTimeField("Publication Date", blank=True, null=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)
    status = models.CharField(max_length=1, choices=POST_STATUS)

    def save(self, *args, **kwargs):
        """
        When saving, automatically generate the slug from the title
        """
        # TODO: Trigger RSS rebuild
        self.slug = slugify(self.title)
        self.last_modified = datetime.datetime.now()
        # Check if publication date is in the past ie; importing old posts
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        if self.published_at < self.created_at:
            self.created_at = self.published_at
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        """
        Convert a draft or unlisted post to be visible with the current date
        """
        self.published_at = datetime.datetime.now()
        self.status = 'P'
        self.save()

    def render(self):
        """
        Render post markdown to HTML with code highlighting included.
        """
        renderer = PostRenderer(escape=True, hard_wrap=True)
        markdown = mistune.Markdown(renderer=renderer)
        return markdown(self.text)

    def __str__(self):
        return self.title

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
                - {}
            </cite>
            '''.format(quote['author'])
            html = html + author_html

        blockquote = '''
        <blockquote class="athelas ml0 mt0 pl4 black-90 bl bw2 b--blue">
            {}
        </blockquote>
        '''.format(html)
        return blockquote