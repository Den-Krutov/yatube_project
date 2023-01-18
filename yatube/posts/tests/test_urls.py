from http import HTTPStatus

from django.test import Client, TestCase

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

    def test_accept_urls_users(self):
        guest_user = PostsUrlTests.guest_user
        auth_user = PostsUrlTests.auth_user
        author_auth_user = PostsUrlTests.author_auth_user
        group = PostsUrlTests.group
        post = PostsUrlTests.post
        url_list_any = [
            '/',
            f'/group/{group.slug}/',
            f'/profile/{auth_user.username}/',
            f'/posts/{post.pk}/',
        ]
        url_patterns = {
            (str('guestUser'), guest_user): url_list_any.copy(),
            (str('authUser'), auth_user): url_list_any.copy() + ['/create/',],
            (str('authorAuthUser'), author_auth_user):
                [f'/posts/{post.pk}/edit/',],
        }
        for obj, url_list in url_patterns.items():
            for url in url_list:
                with self.subTest(obj=obj[0], url=url):
                    responce = obj[1].get(url)
                    self.assertEqual(responce.status_code, HTTPStatus.OK.value)

    def test_redirect_urls_users(self):
        guest_user = PostsUrlTests.guest_user
        auth_user = PostsUrlTests.auth_user
        post = PostsUrlTests.post
        url_patterns = {
            (str('guestUser'), guest_user):
                ['/create/',
                 f'/posts/{post.pk}/edit/',],
            (str('noauthorAuthUser'), auth_user):
                [f'/posts/{post.pk}/edit/',],
        }
        expected_url_patterns = {
            (str('guestUser'), guest_user): '/auth/login/?next={url}',
            (str('noauthorAuthUser'), auth_user):
                f'/posts/{post.pk}/',
        }
        for obj, url_list in url_patterns.items():
            for url in url_list:
                with self.subTest(obj=obj[0], url=url):
                    responce = obj[1].get(url, follow=True)
                    self.assertRedirects(
                        responce,
                        expected_url_patterns.get(obj).format(url=url)
                    )
