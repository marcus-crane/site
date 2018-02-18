import os

class MDStore:

    def __init__(self):
        self.root = 'posts'

    def save_post(self, title, slug, text, date, safe=True):
        """
        Save the blog post as a markdown file
        """
        with open('{}/{}.md'.format(self.root, slug), 'w') as file:
            post = """
            Title: {0}
            Date: {1}
            SFW: {2}

            {3}
            """.format(title, date, safe, text)
            file.write(post)

    def get_post_by_slug(self, slug):
        """
        Fetch the blog post by its slug
        """
        post = [post for post in os.listdir('posts') if slug in post][0]
        with open('{}/{}'.format(self.root, post)) as post:
            return post.read()

    def delete_post(self, slug):
        """
        Delete a post by its slug
        """
        post = [post for post in os.listdir('posts') if slug in post][0]
        path = '{}/{}'.format(self.root, post)
        os.remove(path)
