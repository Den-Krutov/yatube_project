from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User
from users.forms import CreationForm


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authUser')
        cls.path_names = [
            'login',
            'signup',
            'password_change',
            'password_change_done',
            'password_reset',
            'password_reset_done',
            'password_reset_complete',
            'logout',
        ]

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(ViewsTest.user)

    def test_urls_responce_correct_templates(self):
        template_paths = {
            path: f'users/{path}.html' for path in ViewsTest.path_names
        }
        for path_name, template in template_paths.items():
            with self.subTest(url=reverse(f'users:{path_name}')):
                responce = self.auth_client.get(
                    reverse(f'users:{path_name}')
                )
                self.assertTemplateUsed(responce, template)

    def test_signup_uses_correct_context(self):
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        responce = self.client.get(reverse('users:signup'))
        self.assertIn('form', responce.context)
        form = responce.context.get('form')
        self.assertIsInstance(form, CreationForm)
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)
