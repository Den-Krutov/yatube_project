from django.test import Client, TestCase

from ..models import Group, Post, User


class PostsUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_user = Client()
        cls.user = User.objects.create_user(username='UserNoName')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            text='word ' * 5,
            author=cls.user,
            group=cls.group
        )

    def test_url_guest_user(self):
        url_patterns = [
            '/',
            f'/group/{PostsUrlTests.group.slug}/',
            f'/profile/{PostsUrlTests.user.username}/',
            f'/posts/{PostsUrlTests.post.pk}/'
        ]
        for url in url_patterns:
            with self.subTest(url=url):
                responce = PostsUrlTests.guest_user.get(url)
                self.assertEqual(responce.status_code, 200)
