from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from ..helpers import LIMIT
from ..models import Group, Post, User


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.client = Client()
        cls.client.force_login(cls.user)
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
        cls.path_names = [
            'index',
            'group_list',
            'profile',
            'post_detail',
            'post_create',
            'post_edit',
        ]
        cls.urls = [
            reverse('posts:index'),
            reverse('posts:group_list', args=[cls.group.slug]),
            reverse('posts:profile', args=[cls.user.username]),
            reverse('posts:post_detail', args=[cls.post.pk]),
            reverse('posts:post_create'),
            reverse('posts:post_edit', args=[cls.post.pk]),
        ]
        cls.paths = {
            name: url for name, url in zip(cls.path_names, cls.urls)
        }

    def test_responce_templates(self):
        templates = [
            'posts/index.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
        ]
        path_templates = {
            name: template for name, template in zip(
                PostsViewsTest.path_names, templates
            )
        }
        for path_name, url in PostsViewsTest.paths.items():
            with self.subTest(url=url):
                responce = PostsViewsTest.client.get(url)
                self.assertTemplateUsed(
                    responce,
                    path_templates.get(path_name)
                )

    def test_no_form_pages_show_correct_context(self):
        context_pages = [
            {'page_obj': list(Post.objects.all()[:LIMIT])},
            {'group': PostsViewsTest.group,
             'page_obj': list(PostsViewsTest.group.posts.all()[:LIMIT])},
            {'author': PostsViewsTest.user,
             'page_obj': list(PostsViewsTest.user.posts.all()[:LIMIT])},
            {'post': Post.objects.get()},
        ]
        path_context_pages = {
            name: context for name, context in zip(
                PostsViewsTest.path_names[:len(context_pages)], context_pages
            )
        }
        for path_name, context in path_context_pages.items():
            for key, expected in context.items():
                responce = PostsViewsTest.client.get(
                    PostsViewsTest.paths.get(path_name)
                )
                with self.subTest(url=PostsViewsTest.paths.get(path_name),
                                  key=key):
                    self.assertTrue(responce.context.get(key))
                    if key == 'page_obj':
                        self.assertEqual(
                            responce.context.get(key).object_list,
                            expected
                        )
                    else:
                        self.assertEqual(responce.context.get(key), expected)
