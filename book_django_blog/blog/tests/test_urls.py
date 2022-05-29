from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify

from blog.models import Post, Comment


User = get_user_model()


class TestRequestStatuses(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='Boris', password='qwerty')
        cls.post_instance = Post.objects.create(
            title='Title',
            slug=slugify('Title'),
            author=cls.user,
            status='published',
        )
        cls.comment = Comment.objects.create(
            post=cls.post_instance,
            name=cls.user.username,
            email='email@email.com',
            body='Some awesome text',
        )

    def test_post_list_page_200_status(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_404_status_with_wrong_data(self):
        response = self.client.get(
            reverse(
                'blog:post_detail',
                args=['2006', '11', '3', 'very-rare-slug']
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_post_detail_200_status_with_correct_data(self):
        response = self.client.get(
            reverse(
                'blog:post_detail',
                args=[
                    self.post_instance.publish.year,
                    self.post_instance.publish.month,
                    self.post_instance.publish.day,
                    self.post_instance.slug,
                ]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_404_status_without_some_positional_argument(self):
        response = lambda: self.client.get(
            reverse(
                'blog:post_detail',
                args=[
                    self.post_instance.publish.year,
                    self.post_instance.publish.day,
                    self.post_instance.slug,
                ]
            )
        )
        self.assertRaises(NoReverseMatch, response)

    def test_get_post_share_page_200_status(self):
        response = self.client.get(reverse('blog:post_share', args=[self.post_instance.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_share_page_302_status_with_correct_data(self):
        response = self.client.post(
            reverse('blog:post_share', args=[self.post_instance.pk]),
            data={
                'name': 'User',
                'email': 'correct@email.com',
                'to': 'correct.receiver@email.com'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_post_share_page_200_status_with_incorrect_data(self):
        response = self.client.post(
            reverse('blog:post_share', args=[self.post_instance.pk]),
            data={
                'name': 'User',
                'email': 'correct@email.com',
                'to': 'correct.receiver_email.com'
            }
        )
        self.assertEqual(response.status_code, 200)
