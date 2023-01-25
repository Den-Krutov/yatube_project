from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def test_responce_templates(self):
        post = PostsViewsTest.post
        url_templates = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:group_list', args=[PostsViewsTest.group.slug]):
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
        for url, template in url_templates.items():
            with self.subTest(url=url):
                responce = PostsViewsTest.author_auth_client.get(url)
                self.assertTemplateUsed(responce, template)

    def test_views_show_correct_context(self):
        pass
