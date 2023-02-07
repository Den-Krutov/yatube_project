import shutil
import tempfile
from math import ceil

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from django.test import TestCase, override_settings
from django.urls import reverse

from ..forms import CommentForm, PostForm
from ..helpers import LIMIT
from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='word ' * 5,
            author=cls.user,
            group=cls.group,
            image=uploaded,
        )
        cls.other_post = Post.objects.create(
            text='Text new post',
            author=cls.other_user,
            group=cls.other_group,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Text new comment',
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
        cls.key_error_message = 'Key "{key}" not found in context page'
        Post.objects.bulk_create(
            Post(
                text=f'Text {i + 2} post',
                author=cls.user,
                group=cls.group
            ) for i in range(LIMIT)
        )
        cls.form_fields = {
            PostForm: (
                {
                    'text': forms.fields.CharField,
                    'group': forms.fields.ChoiceField,
                    'image': forms.fields.ImageField,
                }
            ),
            CommentForm: (
                {
                    'text': forms.fields.CharField,
                }
            ),
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

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

    def _test_page_obj_context(self, response, expected):
        self.assertIn(
            'page_obj',
            response.context,
            ViewsTest.key_error_message.format(key='page_obj')
        )
        value = response.context.get('page_obj')
        self.assertIsInstance(value, Page)
        self.assertEqual(value.object_list, expected)

    def _test_form_context(self, response, ClassForm):
        self.assertIn(
            'form',
            response.context,
            ViewsTest.key_error_message.format(key='form')
        )
        form = response.context.get('form')
        self.assertIsInstance(form, ClassForm)
        for name, type in ViewsTest.form_fields.get(ClassForm).items():
            with self.subTest(field_name=name):
                self.assertIsInstance(form.fields.get(name), type)

    def test_index_page_show_correct_context(self):
        expected = list(Post.objects.all()[:LIMIT])
        response = self.client.get(ViewsTest.paths.get('index'))
        self._test_page_obj_context(response, expected)

    def test_group_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('group_list'))
        expected = list(ViewsTest.group.posts.all()[:LIMIT])
        self._test_page_obj_context(response, expected)
        self.assertIn(
            'group',
            response.context,
            ViewsTest.key_error_message.format(key='group')
        )
        self.assertEqual(response.context.get('group'), ViewsTest.group)

    def test_profile_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('profile'))
        self._test_page_obj_context(
            response,
            list(ViewsTest.user.posts.all()[:LIMIT])
        )
        self.assertIn(
            'author',
            response.context,
            ViewsTest.key_error_message.format(key='author')
        )
        self.assertEqual(response.context.get('author'), ViewsTest.user)

    def test_post_detail_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('post_detail'))
        self.assertIn(
            'post',
            response.context,
            ViewsTest.key_error_message.format(key='post')
        )
        self.assertEqual(response.context.get('post'), ViewsTest.post)
        self._test_form_context(response, CommentForm)
        self.assertIn(
            'comments',
            response.context,
            ViewsTest.key_error_message.format(key='comments')
        )
        self.assertEqual(
            list(response.context.get('comments')),
            list(Comment.objects.filter(post=ViewsTest.post))
        )

    def test_create_post_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('post_create'))
        self._test_form_context(response, PostForm)

    def test_post_edit_page_show_correct_context(self):
        response = self.client.get(ViewsTest.paths.get('post_edit'))
        self._test_form_context(response, PostForm)
        self.assertIn(
            'is_edit',
            response.context,
            ViewsTest.key_error_message.format(key='is_edit')
        )
        self.assertTrue(response.context.get('is_edit'))

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

    def test_comment_show_on_post(self):
        expected = Comment.objects.filter(post=ViewsTest.post).first()
        response = self.client.get(ViewsTest.paths.get('post_detail'))
        self.assertEqual(response.context['comments'][0], expected)

    def test_comment_noshow_on_other_post(self):
        expected = Comment.objects.filter(post=ViewsTest.other_post).first()
        response = self.client.get(
            reverse('posts:post_detail', args=[ViewsTest.other_post.pk]),
        )
        self.assertEqual(response.context['comments'].first(), expected)
