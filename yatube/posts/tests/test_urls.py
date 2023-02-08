from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post, User


class UrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.auth_client = Client()
        cls.author_auth_client = Client()
        cls.user = User.objects.create_user(username='authUser')
        cls.author_user = User.objects.create_user(username='authorAuthUser')
        cls.auth_client.force_login(cls.user)
        cls.author_auth_client.force_login(cls.author_user)
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            text='word ' * 5,
            author=cls.author_user,
            group=cls.group
        )
        cls.client_names = {
            cls.guest_client: 'guestClient',
            cls.auth_client: 'noauthorAuthClient',
            cls.author_auth_client: 'authorAuthClient',
        }

    def setUp(self):
        cache.clear()

    def test_accept_urls_users(self):
        guest_client = UrlsTest.guest_client
        post = UrlsTest.post
        url_patterns = {
            '/': guest_client,
            '/follow/': UrlsTest.auth_client,
            f'/group/{UrlsTest.group.slug}/': guest_client,
            f'/profile/{post.author.username}/': guest_client,
            f'/posts/{post.pk}/': guest_client,
            '/create/': UrlsTest.auth_client,
            f'/posts/{post.pk}/edit/': UrlsTest.author_auth_client,
        }
        for url, client in url_patterns.items():
            with self.subTest(url=url, obj=UrlsTest.client_names[client]):
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_guest_correct(self):
        post = UrlsTest.post
        urls = [
            '/follow/',
            '/create/',
            f'/posts/{post.pk}/edit/',
            f'/posts/{post.pk}/comment/',
            f'/profile/{post.author.username}/follow/',
            f'/profile/{post.author.username}/unfollow/',
        ]
        expected = '/auth/login/?next={url}'
        for url in urls:
            with self.subTest(url=url):
                response = UrlsTest.guest_client.get(url, follow=True)
                self.assertRedirects(
                    response,
                    expected.format(url=url)
                )

    def test_redirect_auth_user_correct(self):
        post = UrlsTest.post
        url_expected = {
            f'/posts/{post.pk}/edit/': f'/posts/{post.pk}/',
            f'/posts/{post.pk}/comment/': f'/posts/{post.pk}/',
            f'/profile/{post.author.username}/follow/':
                f'/profile/{post.author.username}/',
            f'/profile/{post.author.username}/unfollow/':
                f'/profile/{post.author.username}/',
        }
        expected = '/auth/login/?next={url}'
        for url, expected in url_expected.items():
            with self.subTest(url=url):
                response = UrlsTest.auth_client.get(url, follow=True)
                self.assertRedirects(
                    response,
                    expected,
                )

    def test_response_templates(self):
        post = UrlsTest.post
        templates = {
            '/': 'posts/index.html',
            f'/group/{UrlsTest.group.slug}/': 'posts/group_list.html',
            f'/profile/{post.author.username}/': 'posts/profile.html',
            f'/posts/{post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{post.pk}/edit/': 'posts/create_post.html',
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                response = UrlsTest.author_auth_client.get(url)
                self.assertTemplateUsed(response, template)
