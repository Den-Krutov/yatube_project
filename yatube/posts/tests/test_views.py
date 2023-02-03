from math import ceil

from django.core.paginator import Page
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..helpers import LIMIT
from ..models import Group, Post, User


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
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

    def setUp(self):
        self.client = Client()
        self.client.force_login(ViewsTest.user)

    def test_pages_uses_correct_template(self):
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
                ViewsTest.path_names, templates
            )
        }
        for path_name, url in ViewsTest.paths.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(
                    response,
                    path_templates.get(path_name)
                )

    def test_pages_show_correct_context(self):
        context_pages = [
            {'page_obj': list(Post.objects.all()[:LIMIT])},
            {'group': ViewsTest.group,
             'page_obj': list(ViewsTest.group.posts.all()[:LIMIT])},
            {'author': ViewsTest.user,
             'page_obj': list(ViewsTest.user.posts.all()[:LIMIT])},
            {'post': ViewsTest.post},
            {'form': PostForm()},
            {'form': PostForm(instance=ViewsTest.post),
             'is_edit': True},
        ]
        path_context_pages = {
            name: context for name, context in zip(
                ViewsTest.path_names, context_pages
            )
        }
        for path_name, context in path_context_pages.items():
            response = self.client.get(ViewsTest.paths.get(path_name))
            for key, expected in context.items():
                with self.subTest(url=ViewsTest.paths.get(path_name), key=key):
                    self.assertIn(
                        key,
                        response.context,
                        f'Key {key} not found in context page'
                    )
                    value = response.context.get(key)
                    if key == 'form':
                        self.assertIsInstance(value, PostForm)
                        for field in PostForm.declared_fields.keys():
                            self.assertEqual(value.field, expected.field)
                    else:
                        if key == 'page_obj':
                            self.assertIsInstance(value, Page)
                            value = value.object_list
                        self.assertEqual(value, expected)

    def test_paginator_pages_contains_correct_number_records(self):
        for i in range(LIMIT):
            Post.objects.create(
                text=f'Text {i + 2} post',
                author=ViewsTest.user,
                group=ViewsTest.group
            )
        all_posts = [
            Post.objects.all(),
            ViewsTest.group.posts.all(),
            ViewsTest.user.posts.all(),
        ]
        urls_posts = {
            url: posts for url, posts in zip(
                ViewsTest.paths.values(),
                all_posts
            )
        }
        for url, posts in urls_posts.items():
            for i in range(ceil(posts.count() / LIMIT)):
                with self.subTest(url=url, page=(i + 1)):
                    response = self.client.get(
                        url + f'?page={i + 1}'
                    )
                    number_objs = posts[i * LIMIT:(i + 1) * LIMIT].count()
                    self.assertEqual(
                        len(response.context['page_obj']),
                        number_objs
                    )

    def test_create_post_show_pages(self):
        form_data = {
            'text': 'Text new post',
            'group': ViewsTest.group.pk,
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
        )
        all_posts = [
            Post.objects.all()[0],
            ViewsTest.group.posts.all()[0],
            ViewsTest.user.posts.all()[0],
        ]
        urls_posts = {
            url: posts for url, posts in zip(
                ViewsTest.urls,
                all_posts
            )
        }
        for url, expected in urls_posts.items():
            with self.subTest(url=url):
                post = self.client.get(url).context['page_obj'][0]
                self.assertEqual(post, expected)

    def test_create_post_noshow_pages(self):
        other_user = User.objects.create_user(username='other_user')
        client = self.client
        client.force_login(other_user)
        other_group = Group.objects.create(
            title='Title other group',
            slug='Slug other group',
            description='Description other group',
        )
        post = Post.objects.create(
            text='Text new post',
            author=other_user,
            group=other_group,
        )
        all_posts = [
            ViewsTest.group.posts.all()[0],
            ViewsTest.user.posts.all()[0],
        ]
        urls_posts = {
            url: posts for url, posts in zip(
                ViewsTest.urls[1:],
                all_posts
            )
        }
        for url, expected in urls_posts.items():
            with self.subTest(url=url):
                post = client.get(url).context['page_obj'][0]
                self.assertEqual(post, expected)
