from http import HTTPStatus

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostsUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_user = Client()
        cls.user = User.objects.create_user(username='authUser')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.author_user = User.objects.create_user(username='authorAuthUser')
        cls.author_auth_user = Client()
        cls.author_auth_user.force_login(cls.author_user)
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
            cls.guest_user: 'guestClient',
            cls.auth_user: 'noauthorAuthClient',
            cls.author_auth_user: 'authorAuthClient',
        }

    def test_accept_urls_users(self):
        guest_user = PostsUrlTests.guest_user
        auth_user = PostsUrlTests.auth_user
        author_auth_user = PostsUrlTests.author_auth_user
        group = PostsUrlTests.group
        post = PostsUrlTests.post
        url_patterns = {
            reverse('posts:index'): guest_user,
            reverse('posts:group_list', args=[group.slug]): guest_user,
            reverse('posts:profile', args=[post.author.username]): guest_user,
            reverse('posts:post_detail', args=[post.pk]): guest_user,
            reverse('posts:post_create'): auth_user,
            reverse('posts:post_edit', args=[post.pk]): author_auth_user,
        }
        for url, obj in url_patterns.items():
            with self.subTest(url=url, obj=PostsUrlTests.client_names[obj]):
                responce = obj.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK.value)

    def test_url_unexisting_page(self):
        responce = PostsUrlTests.guest_user.get('/unexisting_page/')
        self.assertEqual(responce.status_code, HTTPStatus.NOT_FOUND.value)

    def test_redirect_urls_users(self):
        guest_user = PostsUrlTests.guest_user
        auth_user = PostsUrlTests.auth_user
        post = PostsUrlTests.post
        url_patterns = {
            guest_user: [
                reverse('posts:post_create'),
                reverse('posts:post_edit', args=[post.pk]),
            ],
            auth_user: [reverse('posts:post_edit', args=[post.pk]),],
        }
        expected_url_patterns = {
            guest_user: reverse(settings.LOGIN_URL) + '?next={url}',
            auth_user: reverse('posts:post_detail', args=[post.pk]),
        }
        for obj, url_list in url_patterns.items():
            for url in url_list:
                with self.subTest(obj=PostsUrlTests.client_names[obj],
                                  url=url):
                    responce = obj.get(url, follow=True)
                    self.assertRedirects(
                        responce,
                        expected_url_patterns.get(obj).format(url=url)
                    )

    def test_responce_templates(self):
        author_auth_user = PostsUrlTests.author_auth_user
        group = PostsUrlTests.group
        post = PostsUrlTests.post
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
                responce = author_auth_user.get(url)
                self.assertTemplateUsed(responce, template)
