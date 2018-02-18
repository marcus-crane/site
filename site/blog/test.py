from storage import MDStore

import datetime
import os
import unittest

Store = MDStore()

class TestMarkdownStorage(unittest.TestCase):

    def test_save_post(self):
        """
        Test that the Storage class properly saves files
        """
        title = 'a post'
        slug = 'a-post'
        text = 'This is a new post\nHello hi\nBye bye'
        date = datetime.datetime.utcnow()
        safe = True
        Store.save_post(title=title, slug=slug, text=text,
                        date=date, safe=safe)
        path = 'posts/{}.md'.format(slug)
        self.assertEqual(os.path.exists(path), True)
        with open(path) as file:
            contents = file.read()
            self.assertIn(text, contents)
        os.remove(path)

    def test_get_post_by_slug(self):
        """
        Test that the Storage class properly fetch posts
        when given its respective slug
        """
        slug = 'day-xero'
        post = Store.get_post_by_slug(slug)
        self.assertIn('Site Reliability Engineer', post)

    def test_delete_post(self):
        """
        Test that the Storage class properly deletes
        posts given its respective slug
        """
        slug = 'testfile'
        path = 'posts/1970-01-01-{}.md'.format(slug)
        with open(path, 'w') as file:
            file.write('this is a test')
        Store.delete_post(slug)
        self.assertEqual(os.path.exists(path), False)

if __name__ == '__main__':
    unittest.main()
