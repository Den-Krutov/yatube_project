from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


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
            group=cls.group
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(FormsTest.user)

    def test_form_valid_data_creates_post(self):
        posts_count = Post.objects.count()
        form_valid_data = {
            'text': 'New post',
            'group': FormsTest.group.pk,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_valid_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', args=[FormsTest.user.username])
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_form_novalid_data_nocreates_post(self):
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
        form_valid_data = {
            'text': 'New post',
            'group': FormsTest.group.pk,
        }
        response = self.client.post(
            reverse('posts:post_edit', args=[FormsTest.post.pk]),
            data=form_valid_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', args=[FormsTest.post.pk])
        )
        self.assertNotEqual(response.context['post'].text, FormsTest.post.text)
        expected = Post.objects.get(id=FormsTest.post.pk)
        self.assertEqual(response.context['post'].text, expected.text)
