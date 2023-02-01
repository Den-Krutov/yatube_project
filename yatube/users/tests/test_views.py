from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User


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

    def test_signup(self):
        self.assertTrue(False)
