from django.test import TestCase
from django.utils.text import slugify

from blog.models import Post
from blog.tests.test_urls import User


class TestPostModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='Boris', password='qwerty')
        cls.post_instance = Post.objects.create(
            title='Title',
            slug=slugify('Title'),
            author=cls.user,
            status='published',
        )

    def test_str_method_is_equal_to_the_title_field(self):
        self.assertEqual(self.post_instance.title, str(self.post_instance))

    def test_str_method_is_not_equal_to_the_wrong_string(self):
        self.assertNotEqual(self.post_instance.title, 'it is not a title field!')

    def test_get_absolute_url_method_200_status(self):
        response = self.client.get(self.post_instance.get_absolute_url())
        self.assertEqual(response.status_code, 200)
