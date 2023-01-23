from http import HTTPStatus

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostsUrlsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='authUser')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.author_user = User.objects.create_user(username='authorAuthUser')
        cls.author_auth_client = Client()
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

    def test_accept_urls_users(self):
        guest_client = PostsUrlsTests.guest_client
        auth_client = PostsUrlsTests.auth_client
        author_auth_client = PostsUrlsTests.author_auth_client
        group = PostsUrlsTests.group
        post = PostsUrlsTests.post
        url_patterns = {
            reverse('posts:index'): guest_client,
            reverse('posts:group_list', args=[group.slug]): guest_client,
            reverse('posts:profile', args=[post.author.username]): (
                guest_client
            ),
            reverse('posts:post_detail', args=[post.pk]): guest_client,
            reverse('posts:post_create'): auth_client,
            reverse('posts:post_edit', args=[post.pk]): author_auth_client,
        }
        for url, obj in url_patterns.items():
            with self.subTest(url=url, obj=PostsUrlsTests.client_names[obj]):
                responce = obj.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK.value)

    def test_url_unexisting_page(self):
        responce = PostsUrlsTests.guest_client.get('/unexisting_page/')
        self.assertEqual(responce.status_code, HTTPStatus.NOT_FOUND.value)

    def test_redirect_urls_users(self):
        guest_client = PostsUrlsTests.guest_client
        auth_client = PostsUrlsTests.auth_client
        post = PostsUrlsTests.post
        url_patterns = {
            guest_client: [
                reverse('posts:post_create'),
                reverse('posts:post_edit', args=[post.pk]),
            ],
            auth_client: [reverse('posts:post_edit', args=[post.pk]),],
        }
        expected_url_patterns = {
            guest_client: reverse(settings.LOGIN_URL) + '?next={url}',
            auth_client: reverse('posts:post_detail', args=[post.pk]),
        }
        for obj, url_list in url_patterns.items():
            for url in url_list:
                with self.subTest(obj=PostsUrlsTests.client_names[obj],
                                  url=url):
                    responce = obj.get(url, follow=True)
                    self.assertRedirects(
                        responce,
                        expected_url_patterns.get(obj).format(url=url)
                    )

    def test_responce_templates(self):
        author_auth_client = PostsUrlsTests.author_auth_client
        group = PostsUrlsTests.group
        post = PostsUrlsTests.post
        templates = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list', args=[group.slug]):
                'posts/group_list.html',
            reverse('posts:profile', args=[post.author.username]):
                'posts/profile.html',
            reverse('posts:post_detail', args=[post.pk]):
                'posts/post_detail.html',
            reverse('posts:post_create'):
                'posts/create_post.html',
            reverse('posts:post_edit', args=[post.pk]):
                'posts/create_post.html',
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                responce = author_auth_client.get(url)
                self.assertTemplateUsed(responce, template)
