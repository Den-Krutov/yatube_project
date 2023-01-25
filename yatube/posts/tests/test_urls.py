from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User


class PostsUrlsTest(TestCase):
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
        guest_client = PostsUrlsTest.guest_client
        post = PostsUrlsTest.post
        url_patterns = {
            '/': guest_client,
            f'/group/{PostsUrlsTest.group.slug}/': guest_client,
            f'/profile/{post.author.username}/': guest_client,
            f'/posts/{post.pk}/': guest_client,
            '/create/': PostsUrlsTest.auth_client,
            f'/posts/{post.pk}/edit/': PostsUrlsTest.author_auth_client,
        }
        for url, client in url_patterns.items():
            with self.subTest(url=url, obj=PostsUrlsTest.client_names[client]):
                responce = client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK.value)

    def test_url_unexisting_page(self):
        responce = PostsUrlsTest.guest_client.get('/unexisting_page/')
        self.assertEqual(responce.status_code, HTTPStatus.NOT_FOUND.value)

    def test_redirect_urls_users(self):
        guest_client = PostsUrlsTest.guest_client
        auth_client = PostsUrlsTest.auth_client
        post = PostsUrlsTest.post
        url_patterns = {
            guest_client: ['/create/', f'/posts/{post.pk}/edit/',],
            auth_client: [f'/posts/{post.pk}/edit/',],
        }
        expected_url_patterns = {
            guest_client: '/auth/login/?next={url}',
            auth_client: f'/posts/{post.pk}/',
        }
        for obj, url_list in url_patterns.items():
            for url in url_list:
                with self.subTest(obj=PostsUrlsTest.client_names[obj],
                                  url=url):
                    responce = obj.get(url, follow=True)
                    self.assertRedirects(
                        responce,
                        expected_url_patterns.get(obj).format(url=url)
                    )

    def test_responce_templates(self):
        post = PostsUrlsTest.post
        templates = {
            '/': 'posts/index.html',
            f'/group/{PostsUrlsTest.group.slug}/': 'posts/group_list.html',
            f'/profile/{post.author.username}/': 'posts/profile.html',
            f'/posts/{post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{post.pk}/edit/': 'posts/create_post.html',
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                responce = PostsUrlsTest.author_auth_client.get(url)
                self.assertTemplateUsed(responce, template)
