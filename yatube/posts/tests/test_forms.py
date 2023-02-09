import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FormsTest(TestCase):
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
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client.force_login(FormsTest.user)
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
        self.post_form_data = {
            'text': 'New post',
            'group': FormsTest.group.pk,
            'image': uploaded,
        }
        self.comment_form_data = {
            'text': 'New comment',
        }

    def test_comment_form_creates_comment(self):
        post = FormsTest.post
        comments_count = Comment.objects.filter(post=post).count()
        response = self.client.post(
            reverse('posts:add_comment', args=[post.pk]),
            data=self.comment_form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[post.pk])
        )
        self.assertEqual(
            Comment.objects.filter(post=post).count(),
            comments_count + 1
        )

    def test_post_form_valid_data_creates_post(self):
        posts_count = Post.objects.count()
        response = self.client.post(
            reverse('posts:post_create'),
            data=self.post_form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', args=[FormsTest.user.username])
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_post_form_novalid_data_nocreates_post(self):
        posts_count = Post.objects.count()
        form_novalid_datas = {
            'Пост слишком большой':
                {'text': 'New post' * 1000, 'group': FormsTest.group.pk},
            'В записи присутствует слишком большое слово':
                {'text': 'Newpost' * 100, 'group': FormsTest.group.pk},
        }
        for error_str, form_novalid_data in form_novalid_datas.items():
            with self.subTest():
                response = self.client.post(
                    reverse('posts:post_create'),
                    data=form_novalid_data,
                    follow=True
                )
                self.assertEqual(Post.objects.count(), posts_count)
                self.assertFormError(
                    response,
                    'form',
                    'text',
                    error_str,
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit(self):
        response = self.client.post(
            reverse('posts:post_edit', args=[FormsTest.post.pk]),
            data=self.post_form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[FormsTest.post.pk])
        )
        self.assertNotEqual(response.context['post'].text, FormsTest.post.text)
        expected = Post.objects.get(id=FormsTest.post.pk)
        self.assertEqual(response.context['post'].text, expected.text)
