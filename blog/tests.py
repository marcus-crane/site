import datetime
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from .models import Post

def create_post(author, title, text, days, draft=True):
  """
  Create a post with the given title, text, date
  and draft
  """
  if days is not None:
    date = timezone.now() + datetime.timedelta(days=days)
  else:
    date = None
  return Post.objects.create(author=author, title=title, text=text, date=date, draft=draft)

class PostIndexViewTests(TestCase):
  def setUp(self):
    """
    Create a test user, required to be submitted with instances of the Post model
    """
    self.factory = RequestFactory()
    self.user = User.objects.create_user(
      username='testuser', email='test@example.com', password='topsykrets')

  def test_no_posts(self):
    """
    If no posts exist, display an appropriate message
    """
    blog = self.client.get(reverse('blog:post_list'))
    self.assertEqual(blog.status_code, 200)
    self.assertContains(blog, 'No posts have been written yet!')
    self.assertQuerysetEqual(blog.context['posts'], [])

  def test_draft_post(self):
    """
    If a post is a draft with no date, it shouldn't appear in the post list but is visible via slug
    """
    draft_post = create_post(author=self.user, title='Draft Post', text='This is a draft post', days=None, draft=True)
    blog = self.client.get(reverse('blog:post_list'))
    self.assertEqual(blog.status_code, 200)
    self.assertQuerysetEqual(blog.context['posts'], [])

    article = self.client.get(reverse('blog:post_detail', kwargs={'slug': draft_post.slug}))
    self.assertEqual(article.status_code, 200)
    self.assertContains(article, draft_post.text)

  def test_published_post(self):
    """
    If a post is not a draft and has a date, it should appear in the post list and visible via slug
    """
    public_post = create_post(author=self.user, title='Public Post', text='This is a public post', days=-2, draft=False)
    blog = self.client.get(reverse('blog:post_list'))
    self.assertEqual(blog.status_code, 200)
    self.assertQuerysetEqual(blog.context['posts'], ['<Post: Public Post>'])

    article = self.client.get(reverse('blog:post_detail', kwargs={'slug': public_post.slug}))
    self.assertEqual(article.status_code, 200)
    self.assertContains(article, public_post.text)

  def test_publish_draft_post(self):
    """
    If a post is created that is a draft, calling the publish method should render it
    visible and change the draft field to false
    """
    draft_post = create_post(author=self.user, title='Draft Post', text='This will be published', days=None, draft=True)
    blog = self.client.get(reverse('blog:post_list'))
    self.assertQuerysetEqual(blog.context['posts'], [])
    self.assertEqual(draft_post.date, None)
    self.assertEqual(draft_post.draft, True)
    
    draft_post.publish() # Post should now have a current date and draft set to False

    blog = self.client.get(reverse('blog:post_list'))
    self.assertNotEqual(draft_post.date, None)
    self.assertEqual(draft_post.draft, False)
    self.assertQuerysetEqual(blog.context['posts'], ['<Post: Draft Post>'])

  def test_published_post_with_future_date(self):
    """
    If a post is not a draft but has a date in the future, it shouldn't appear in the post list
    """
    public_post = create_post(author=self.user, title='Future Post', text='Hello from the future!', days=2, draft=False)
    blog = self.client.get(reverse('blog:post_list'))
    self.assertEqual(blog.status_code, 200)
    self.assertContains(blog, 'No posts have been written yet!')
    self.assertQuerysetEqual(blog.context['posts'], [])