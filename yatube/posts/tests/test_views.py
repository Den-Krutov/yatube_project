from math import ceil

from django import forms
from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse

from ..forms import PostForm
from ..helpers import LIMIT
from ..models import Group, Post, User


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.other_user = User.objects.create_user(username='other_user')
        cls.group = Group.objects.create(
            title='Test title',
            slug='test-slug',
            description='Test description',
        )
        cls.other_group = Group.objects.create(
            title='Title other group',
            slug='slug-other-group',
            description='Description other group',
        )
        cls.post = Post.objects.create(
            text='word ' * 5,
            author=cls.user,
            group=cls.group
        )
        cls.other_post = Post.objects.create(
            text='Text new post',
            author=cls.other_user,
            group=cls.other_group,
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
        Post.objects.bulk_create(
            Post(
                text=f'Text {i + 2} post',
                author=cls.user,
                group=cls.group
            ) for i in range(LIMIT)
        )

    def setUp(self):
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

    def _test_page_obj_context(self, value, expected):
        self.assertIsInstance(value, Page)
        self.assertEqual(value.object_list, expected)

    def test_index_page_show_correct_context(self):
        expected = list(Post.objects.all()[:LIMIT])
        response = self.client.get(ViewsTest.paths.get('index'))
        self.assertIn(
            'page_obj',
            response.context,
            'Key "page_obj" not found in context page'
        )
        self._test_page_obj_context(response.context.get('page_obj'), expected)

    def test_group_page_show_correct_context(self):
        context = {
            'group': ViewsTest.group,
            'page_obj': list(ViewsTest.group.posts.all()[:LIMIT])
        }
        response = self.client.get(ViewsTest.paths.get('group_list'))
        for key, expected in context.items():
            self.assertIn(
                key,
                response.context,
                f'Key {key} not found in context page'
            )
            value = response.context.get(key)
            if key == 'page_obj':
                self._test_page_obj_context(value, expected)
            else:
                self.assertEqual(value, expected)

    def test_profile_page_show_correct_context(self):
        context = {
            'author': ViewsTest.user,
            'page_obj': list(ViewsTest.group.posts.all()[:LIMIT])
        }
        response = self.client.get(ViewsTest.paths.get('profile'))
        for key, expected in context.items():
            self.assertIn(
                key,
                response.context,
                f'Key {key} not found in context page'
            )
            value = response.context.get(key)
            if key == 'page_obj':
                self._test_page_obj_context(value, expected)
            else:
                self.assertEqual(value, expected)

    def test_post_detail_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('post_detail'))
        self.assertIn(
            'post',
            response.context,
            'Key "post" not found in context page'
        )
        self.assertEqual(response.context.get('post'), ViewsTest.post)

    def _test_form_context(self, form):
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        self.assertIsInstance(form, PostForm)
        for field_name, field_type in form_fields.items():
            with self.subTest(field_name=field_name):
                self.assertIsInstance(form.fields.get(field_name), field_type)

    def test_create_post_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('post_create'))
        self.assertIn(
            'form',
            response.context,
            'Key "form" not found in context page'
        )
        self._test_form_context(response.context.get('form'))

    def test_post_edit_page_show_correct_context(self):
        context = {
            'form': PostForm(instance=ViewsTest.post),
            'is_edit': True
        }
        response = self.client.get(ViewsTest.paths.get('post_edit'))
        for key, expected in context.items():
            self.assertIn(
                key,
                response.context,
                f'Key {key} not found in context page'
            )
            value = response.context.get(key)
            if key == 'form':
                self._test_form_context(response.context.get(key))
            else:
                self.assertEqual(value, expected)

    def test_paginator_pages_contains_correct_number_records(self):
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
                        url, {'page': {i + 1}}
                    )
                    number_objs = posts[i * LIMIT:(i + 1) * LIMIT].count()
                    self.assertEqual(
                        len(response.context['page_obj']),
                        number_objs
                    )

    def test_post_show_on_index_group_profile(self):
        all_posts = [
            Post.objects.first(),
            ViewsTest.group.posts.first(),
            ViewsTest.user.posts.first(),
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

    def test_post_noshow_on_other_group_profile(self):
        self.client.force_login(ViewsTest.other_user)
        all_posts = [
            ViewsTest.group.posts.first(),
            ViewsTest.user.posts.first(),
        ]
        urls_posts = {
            url: posts for url, posts in zip(
                ViewsTest.urls[1:],
                all_posts
            )
        }
        for url, expected in urls_posts.items():
            with self.subTest(url=url):
                post = self.client.get(url).context['page_obj'][0]
                self.assertEqual(post, expected)
